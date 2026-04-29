from ursina import *
import math
from ursina.lights import DirectionalLight
from ursina import AmbientLight
from ursina.shaders import lit_with_shadows_shader
from random import sample
from random import choice
from ursina.sequence import Sequence, Func
import os
import json
import random
import tracks
import importlib
import subprocess


# declarations
app = Ursina()
window.title = 'Pochita Kart'
window.fps_counter.enabled = True
camera_yaw = 0
base_fov = 50
max_fov = 60
chainsaw_timer = 0
bombs_per_second = 18
kart_was_stunned_last_frame = False
race_started = False
countdown_done = False
countdown_text = Text(text='', scale=5, origin=(0,0), background=True)
results_shown = False
walls = []
item_boxes = []
debug_floor = Entity(model='plane', scale=100, y=-20, color=color.black33, collider='box')
items = ['jump', 'boost', 'gun', 'chainsaw', 'reze', 'monkima']
spawn_position = Vec3(0, 1, 0)
track_id = "g5"
god_mode = False
tile_texture = None
current_game_mode = 'grand_prix'  # or 'time_trials'
BEST_TIMES_FILE = 'best_times.json'
try:
    with open(BEST_TIMES_FILE) as f:
        best_times = json.load(f)
except FileNotFoundError:
    best_times = {}


# ----- AI Character Models -----
AI_CHARACTER_MODELS = {
    'Pochita': {
        'model': 'mdl/pochita.obj',
        'texture': 'mdl/pochita.png',
        'scale': 1,
        'rotation_y': 0
    },
    'Hatsune Miku': {
        'model': 'mdl/hatsune_miku.glb',
        'scale': 0.4,
        'rotation_y': 180
    },
    'Ghost of Parasect': {
        'model': 'mdl/parasect.glb',
        'scale': 0.01325,
        'rotation_y': 180
    },
    'Big Chungus': {
        'model': 'mdl/big_chungus.glb',
        'scale': 0.2,
        'rotation_y': 225,
        'y_offset': 1.15
    },
    'Rat': {
        'model': 'cube',
        'texture': 'img/rat.jpg',
        'scale': (1, 1, 1),
        'billboard': True
    }
}

# ----- Sounds -----
item_sounds = {
    'jump': Audio('snd/jump.mp3', autoplay=False),
    'boost': Audio('snd/boost.mp3', autoplay=False),
    'gun': Audio('snd/gun.mp3', autoplay=False),
    'chainsaw': Audio('snd/chainsaw.mp3', autoplay=False),
    'reze': Audio('snd/reze.mp3', autoplay=False),
    'monkima': Audio('snd/monkima.mp3', autoplay=False)
}
engine_sound_file = 'snd/engine_loop.mp3'
drift_sound = Audio('snd/drift.mp3', loop=True, autoplay=False, volume=0)

# ----- function definitions -----

# add track tile 
def add_track_tile(x, z, rotation=0, vrotation=0, y=0, x_size=10, z_size=10):
    tile = Entity(
        model='cube',
        texture=tile_texture,
        shader=lit_with_shadows_shader,
        position=(x, y, z),
        scale=(x_size, 0.1, z_size),
        collider='box'
    )
    tile.rotation_y = rotation
    tile.rotation_x = vrotation
    return tile
def add_big_tile(x, z, rotation=0, vrotation=0, y=0, x_size=25, z_size=25):
    tile = Entity(
        model='cube',
        texture=tile_texture,
        shader=lit_with_shadows_shader,
        position=(x, y, z),
        scale=(x_size, 0.1, z_size),
        collider='box'
    )
    tile.rotation_y = rotation
    tile.rotation_x = vrotation
    return tile
# spawn reze explosion
def spawn_explosion(position):
    explosion = Entity(
        model='sphere',
        color=color.red,
        position=position,
        scale=10,
        shader=lit_with_shadows_shader
    )
    explosion.animate_scale(20, duration=0.3, curve=curve.linear)
    explosion.fade_out(duration=0.3)
    destroy(explosion, delay=0.3)
# drop random bobms
def drop_random_bomb():
    # Random XZ across a large area centered around the whole track
    x = random.uniform(-500, 500)
    z = random.uniform(-100, 900)
    y = 40  # high in the sky
    bomb = Entity(
        model='sphere',
        color=color.black,
        scale=1,
        position=Vec3(x, y, z),
        shader=lit_with_shadows_shader
    )

    def explode():
        spawn_explosion(bomb.position)
        for k in [kart] + ai_karts:
            if distance(bomb.position, k.position) < 10:
                print(f"[BOMB] {getattr(k, 'assigned_character', 'Player')} hit by falling bomb!")
                k.speed = 0
                k.stun_timer = 2
        destroy(bomb)

    bomb.animate_y(0, duration=2, curve=curve.linear)  # fall straight down
    invoke(explode, delay=2)

# create item box
def create_item_box(position):
    box = Entity(
        model='cube',
        color=color.orange,
        position=position,
        scale=(1, 1, 1),
        collider='box',
        rotation_y=0
    )
    box.respawn_timer = 0
    return box

# create chungus orb
def create_chungus_orb(position, orb_id):
    orb = Entity(
        model='sphere',
        position=position,
        scale=(10, 10, 10),
        collider='box',
        rotation_y=0,
        texture ='img/road3.jpg',
    )
    orb.respawn_timer = 0
    orb.orb_id = orb_id  # <-- Assign unique ID
    return orb

# ----- Create Track Block -----
with open('savefile.json') as f:
    savefile = json.load(f)

current_track = savefile.get('track', 1)
current_game_mode = savefile.get('mode', 'grand_prix')

if current_game_mode == 'grand_prix':
    track_id = f"g{current_track}"
if current_game_mode == 'time_trials':
    track_id = f"t{current_track}"
if current_track == 1:
        #object used
        ai_waypoints = tracks.track1.ai_waypoints
        item_box_positions = tracks.track1.item_box_positions
        skybox_texture = tracks.track1.skybox_texture
        tile_texture = tracks.track1.tile_texture
        background_music = Audio(tracks.track1.ost, loop=True, autoplay=True, volume=0.5)
        #function used
        start_tile, middle_tile = tracks.create_track1(add_track_tile, walls, add_big_tile)
        tracks.create_track1(add_track_tile,walls,add_big_tile) 
elif current_track == 2:
        #object used
        ai_waypoints = tracks.track2.ai_waypoints
        item_box_positions = tracks.track2.item_box_positions
        skybox_texture = tracks.track2.skybox_texture
        tile_texture = tracks.track2.tile_texture
        background_music = Audio(tracks.track2.ost, loop=True, autoplay=True, volume=0.5)
        #function used
        start_tile, middle_tile = tracks.create_track2(add_track_tile, walls)
        tracks.create_track2(add_track_tile,walls)
elif current_track == 3:
        #object used
        ai_waypoints = tracks.track3.ai_waypoints
        item_box_positions = tracks.track3.item_box_positions
        skybox_texture = tracks.track3.skybox_texture
        tile_texture = tracks.track3.tile_texture
        background_music = Audio(tracks.track3.ost, loop=True, autoplay=True, volume=0.5)
        #function used
        start_tile, middle_tile = tracks.create_track3(add_track_tile, walls, add_big_tile)
        tracks.create_track3(add_track_tile,walls,add_big_tile)
        #chungus orbs
        chungus_orbs = []
        if current_track == 3:
            chungus_orb_positions = [
                Vec3(0, 35, 230),
                Vec3(-300, 35, 200),
                Vec3(-110, 35, 700),
                Vec3(-300, 35, 100),
                Vec3(200, 35, 300),
                Vec3(300, 35, 600)
            ]
            for i, pos in enumerate(chungus_orb_positions):
                chungus_orbs.append(create_chungus_orb(pos, i))

elif current_track == 4:
        #object used
        ai_waypoints = tracks.track4.ai_waypoints
        item_box_positions = tracks.track4.item_box_positions
        skybox_texture = tracks.track4.skybox_texture
        tile_texture = tracks.track4.tile_texture
        background_music = Audio(tracks.track4.ost, loop=True, autoplay=True, volume=0.5)
        #function used
        start_tile, middle_tile = tracks.create_track4(add_track_tile, walls)
        tracks.create_track4(add_track_tile,walls)
elif current_track == 5:
        #object used
        ai_waypoints = tracks.track5.ai_waypoints
        item_box_positions = tracks.track5.item_box_positions
        skybox_texture = tracks.track5.skybox_texture
        tile_texture = tracks.track5.tile_texture
        background_music = Audio(tracks.track5.ost, loop=True, autoplay=True, volume=0.5)
        #function used
        start_tile, middle_tile = tracks.create_track5(add_track_tile, walls)
        tracks.create_track5(add_track_tile,walls) 
# create item boxes
if current_game_mode == 'grand_prix':
    for pos in item_box_positions:
        item_boxes.append(create_item_box(pos))

# ----- Player Kart -----
with open('savefile.json') as f:
    savefile = json.load(f)

current_character = savefile.get('character', 'Pochita')
kart = Entity(
    position=spawn_position,
    collider='box',
    scale=1.5
)

if current_character == 'Pochita':
    model_entity = Entity(
        parent=kart,
        model='mdl/pochita.obj',
        texture='mdl/pochita.png',
        scale=1
    )
elif current_character == 'Hatsune Miku':
    model_entity = Entity(
        parent=kart,
        model='mdl/hatsune_miku.glb',
        scale=0.4,
        rotation_y=180
    )
elif current_character == 'Ghost of Parasect':
    model_entity = Entity(
        parent=kart,
        model='mdl/parasect.glb',
        scale=0.01325,
        rotation_y=180
    )
elif current_character == 'Big Chungus':
    model_entity = Entity(
        parent=kart,
        model='mdl/big_chungus.glb',
        scale=0.2,
        y=1.15,
        rotation_y=270-45
    )
elif current_character == 'Rat':
    model_entity = Entity(
        parent=kart,
        model='cube',
        texture='img/rat.jpg',
        scale=(1, 1, 1),
        billboard=True
    )

kart.position = spawn_position
kart.gravity = 9
kart.vertical_speed = 0
kart.air_timer = 0
kart.passed_middle = False
kart.collider = BoxCollider(kart, center=(0,0.25,0), size=(1, 0.5, 2))
kart.held_item = None 
kart.stun_timer = 0  # Timer for stun effect
kart.on_ground = False  # Track if kart is on the ground
kart.engine_audio = Audio(engine_sound_file, loop=True, autoplay=True, volume=0)
kart.current_friction = 0
kart.speed = 0
# movement vars
if current_character == 'Pochita':
    kart.max_speed = 27
    kart.acceleration = 0.5
    kart.turn_speed = 60*0.75
    kart.friction = 0.9998
    kart.drift_friction = 0.9995
    kart.brake_power = 10
elif current_character == 'Hatsune Miku':
    kart.max_speed = 32
    kart.acceleration = 0.4
    kart.turn_speed = 50*0.75
    kart.friction = 0.9998
    kart.drift_friction = 0.9995
    kart.brake_power = 8
elif current_character == 'Ghost of Parasect':
    kart.max_speed = 24
    kart.acceleration = 0.5
    kart.turn_speed = 80*0.75
    kart.friction = 0.9998
    kart.drift_friction = 0.9995
    kart.brake_power = 20
elif current_character == 'Big Chungus':
    kart.max_speed = 50
    kart.acceleration = 0.25
    kart.turn_speed = 40*0.75
    kart.friction = 0.9998
    kart.drift_friction = 0.9995
    kart.brake_power = 15
elif current_character == 'Rat':
    kart.max_speed = 50
    kart.acceleration = 1
    kart.turn_speed = 40*0.75
    kart.friction = 0.9998
    kart.drift_friction = 0.9995
    kart.brake_power = 5
# kart hitbox
kart.kart_hitbox = Entity(
    parent=kart,
    model='cube',
    scale=(1, 1, 2),
    collider='box',
    position=(0,0.25,0),  # match your offset
    visible=False
)

# ----- Big Chungus -----
if current_track == 3:
    giant_chungus = Entity(
        model='mdl/big_chungus.glb',
        scale=Vec3(10, 10, 10),
        position=Vec3(-600, 50, -100),  # starting off-screen
        rotation_y=90,
        collider='box',
        shader=lit_with_shadows_shader
    )
    giant_chungus.direction = Vec3(1, 0, 1).normalized()  # diagonal march
    giant_chungus.speed = 100  # adjust for drama
    giant_chungus.change_dir_timer = 0
    giant_chungus.target_direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()


# ----- AI Karts -----
ai_karts = []
if current_track == 1:
    ai_characters_assigned = ['Hatsune Miku', 'Pochita', 'Pochita', 'Pochita', 'Pochita', 'Pochita', 'Pochita', 'Pochita']
elif current_track == 2:
    ai_characters_assigned = ['Pochita', 'Hatsune Miku', 'Ghost of Parasect', 'Pochita', 'Pochita', 'Pochita', 'Pochita', 'Pochita']
elif current_track == 3:
    ai_characters_assigned = ['Big Chungus', 'Big Chungus', 'Big Chungus', 'Big Chungus', 'Big Chungus', 'Big Chungus', 'Big Chungus', 'Big Chungus']
elif current_track == 4:
    ai_characters_assigned = ['Pochita', 'Hatsune Miku', 'Ghost of Parasect', 'Big Chungus', 'Rat', 'Pochita', 'Pochita', 'Pochita']
elif current_track == 5:
    ai_characters_assigned = ['Pochita', 'Hatsune Miku', 'Ghost of Parasect', 'Big Chungus', 'Rat', 'Rat', 'Pochita', 'Pochita']
random.shuffle(ai_characters_assigned)
if current_game_mode == 'grand_prix':
    ai_spawn_offsets = [
        Vec3(-2, 0, -5),  # front left
        Vec3( 0, 0, -5),  # front center
        Vec3( 2, 0, -5),  # front right

        Vec3(-4, 0, 0),   # left side
        Vec3( 4, 0, 0),   # right side


        Vec3(-2, 0, 5),   # back left
        Vec3( 0, 0, 5),   # back center
        Vec3( 2, 0, 5)    # back right
    ]
elif current_game_mode == 'time_trials':
    ai_spawn_offsets = [
        Vec3(-2, -100, -5),  # front left
        Vec3( 0, -100, -5),  # front center
        Vec3( 2, -100, -5),  # front right

        Vec3(-4, -100, 0),   # left side
        Vec3( 4, -100, 0),   # right side

        Vec3(-2, -100, 5),   # back left
        Vec3( 0, -100, 5),   # back center
        Vec3( 2, -100, 5)    # back right
    ]


for i in range(8):
    offset = ai_spawn_offsets[i]
    character_name = ai_characters_assigned[i]
    model_data = AI_CHARACTER_MODELS[character_name]

    ai_kart = Entity(
        position=spawn_position + offset,
        collider='box',
        gravity=9,
        scale=1.5
    )

    # Attach chosen character model to this AI kart
    Entity(
        parent=ai_kart,
        model=model_data['model'],
        texture=model_data.get('texture'),
        scale=model_data['scale'],
        rotation_y=model_data.get('rotation_y', 0),
        billboard=model_data.get('billboard', False),
        y=model_data.get('y_offset', 0)
    )

    # Keep your existing AI personalities
    if i == 0:
        ai_kart.ai_max_speed = 50 * (0.6+current_track/10)
        ai_kart.ai_acceleration = 0.6 * (0.6+current_track/10)
        ai_kart.ai_turn_speed = 100 * (0.6+current_track/10)
    elif i == 1:
        ai_kart.ai_max_speed = 30 * (0.6+current_track/10)
        ai_kart.ai_acceleration = 5 * (0.6+current_track/10)
        ai_kart.ai_turn_speed = 110 * (0.6+current_track/10)
    elif i == 2:
        ai_kart.ai_max_speed = 40 * (0.6+current_track/10)
        ai_kart.ai_acceleration = 1 * (0.6+current_track/10)
        ai_kart.ai_turn_speed = 1000 * (0.6+current_track/10)
    elif i == 3:
        ai_kart.ai_max_speed = 45 * (0.6+current_track/10)
        ai_kart.ai_acceleration = 1.5 * (0.6+current_track/10)
        ai_kart.ai_turn_speed = 200 * (0.6+current_track/10)
    elif i == 4:
        ai_kart.ai_max_speed = 42 * (0.6+current_track/10)
        ai_kart.ai_acceleration = 2.0 * (0.6+current_track/10)
        ai_kart.ai_turn_speed = 250 * (0.6+current_track/10)
    elif i == 5:
        ai_kart.ai_max_speed = 38 * (0.6+current_track/10)
        ai_kart.ai_acceleration = 1.8 * (0.6+current_track/10)
        ai_kart.ai_turn_speed = 180 * (0.6+current_track/10)
    elif i == 6:
        ai_kart.ai_max_speed = 40 * (0.6+current_track/10)
        ai_kart.ai_acceleration = 2.2 * (0.6+current_track/10)
        ai_kart.ai_turn_speed = 220 * (0.6+current_track/10)
    elif i == 7:
        ai_kart.ai_max_speed = 36 * (0.6+current_track/10)
        ai_kart.ai_acceleration = 1.2 * (0.6+current_track/10)
        ai_kart.ai_turn_speed = 150 * (0.6+current_track/10)

    # Setup remaining properties
    ai_kart.waypoints = ai_waypoints
    ai_kart.waypoint_index = 0
    ai_kart.vertical_speed = 0
    ai_kart.held_item = None
    ai_kart.stun_timer = 0
    ai_kart.engine_audio = Audio(engine_sound_file, loop=True, autoplay=True, volume=0)
    ai_kart.ai_speed = 0
    ai_kart.laps = 0
    ai_kart.passed_middle = False
    ai_kart.has_crossed = False
    ai_kart.assigned_character = character_name

    ai_karts.append(ai_kart)


# ----- Lap Counter -----
lap_count = 0
player_collected_orbs = set()
required_orb_count = 6
finish_order = []
race_time = 0
lap_times = []
current_lap_time = 0
race_time_text = Text(text=f"Total: 0.00s", position=(0.60, 0.40), scale=2, origin=(0,0), background=True)
current_lap_text = Text(text=f"Lap Time: 0.00s", position=(0.60, 0.35), scale=2, origin=(0,0), background=True)
lap_times_text = Text(text=f"Laps:", position=(0.60, 0.25), scale=2, origin=(0,0), background=True)
lap_text = Text(text=f"Lap {lap_count+1}", position=(-0.70, 0.40), scale=2, origin=(0, 0), background=True)
if current_track == 3:
    orb_count_text = Text(text='Chungus Orbs: 0/6', position=(-0.0, 0.40), scale=2, origin=(0,0), background=True)

coords = Text(text=f"x: {kart.position.x}, y: {kart.position.y}, z: {kart.position.z}", position=(-0.60, 0.30), scale=2, origin=(0, 0), background=True) # remove later debug
middle_text = Text(
    text=f"Checkpoint: {kart.passed_middle}",
    position=(-0.70, 0.20),
    scale=2,
    origin=(0, 0),
    background=True
)

results_text = Text(text='', origin=(0,0), scale=2, background=True, enabled=False)


has_crossed = False  # Prevent double counting per lap

# ----- UI -----
item_icons = {
    'boost': 'img/boost_icon.jpg',
    'jump': 'img/jump_icon.jpg',
    'gun': 'img/gun_icon.png',
    'chainsaw': 'img/chainsaw_icon.png',
    'reze': 'img/reze_icon.png',
    'monkima': 'img/monkima_icon.png'
}

item_icon = Entity(
    parent=camera.ui,
    model='quad',
    texture=None,
    scale=(0.2, 0.2),
    position=(-0.75, -0.4),
    enabled=False
)

monkima_overlay = Entity(
    parent=camera.ui,
    model='quad',
    texture='img/monkima.png',
    scale=(1, 1),
    color=color.clear,
    enabled=False
)

# ----- Monkima Overlay -----
def show_monkima_overlay():
    monkima_overlay.enabled = True
    monkima_overlay.scale = (1, 1)
    monkima_overlay.color = color.rgba(255, 255, 255, 200/255)
    monkima_overlay.fade_out(duration=4)
    invoke(lambda: setattr(monkima_overlay, 'enabled', False), delay=4)

# ----- Launch Menu -----
def launch_menu():
    subprocess.Popen(['python', 'menu.py'])

# ----- Show results screen -----

def show_results_screen():
    global results_shown, countdown_done, track_id

    results_shown = True
    countdown_done = False  # stop update movement

    # Unlock characters based on track completion
    if current_game_mode == 'grand_prix':
        unlock_file = 'unlock_status.json'
        if os.path.exists(unlock_file):
            with open(unlock_file, 'r') as f:
                unlock_data = json.load(f)
        else:
            unlock_data = {'characters': [True, False, False, False, False]}

        char_unlock_map = {
            1: 1,  # Track 1 → Character 2 (index 1)
            2: 2,  # Track 2 → Character 3 (index 2)
            3: 3,  # Track 3 → Character 4 (index 3)
            5: 4,  # Track 5 → Character 5 (index 4)
        }

        char_index = char_unlock_map.get(current_track)
        if char_index is not None:
            if not unlock_data['characters'][char_index]:
                print(f"[UNLOCK] Unlocking character {char_index + 1}")
                unlock_data['characters'][char_index] = True
                with open(unlock_file, 'w') as f:
                    json.dump(unlock_data, f, indent=4)

    # Change camera angle
    camera.position = kart.position + Vec3(0, 15, -30)
    camera.look_at(kart)

    player_place = finish_order.index("Player") + 1

    results = f"🏁 RESULTS 🏁\n\n"
    results += f"You finished in {player_place}{ordinal_suffix(player_place)} place!\n\n"
    results += "Finish Order:\n"
    for i, name in enumerate(finish_order, start=1):
        if name == "Player":
            display_name = "Player (" + current_character + ")"
        elif name.startswith("AI "):
            ai_index = int(name.split(" ")[1]) - 1
            display_name = ai_karts[ai_index].assigned_character
        else:
            display_name = name
        results += f"{i}. {display_name}\n"

    results += f"\nTotal Time: {race_time:.2f}s\n\n"
    for i, t in enumerate(lap_times):
        results += f"Lap {i+1}: {t:.2f}s\n"

    results_text.text = results
    results_text.enabled = True

    # Get previous record
    record = best_times.get(track_id, {})

    previous_best_total = record.get("best_total_time", None)
    previous_best_lap = record.get("best_lap_time", None)

    # Find player's best single lap in this race
    player_best_lap = min(lap_times) if lap_times else None

    # Check and update total time
    if previous_best_total is None or race_time < previous_best_total:
        print(f"[BEST] New best total time for track {track_id}: {race_time:.2f}s!")
        record["best_total_time"] = race_time
    else:
        print(f"[BEST] Best total time remains {previous_best_total:.2f}s.")

    # Check and update best single lap
    if player_best_lap is not None and (previous_best_lap is None or player_best_lap < previous_best_lap):
        print(f"[BEST] New best lap time for track {track_id}: {player_best_lap:.2f}s!")
        record["best_lap_time"] = player_best_lap
    else:
        if previous_best_lap is not None:
            print(f"[BEST] Best lap time remains {previous_best_lap:.2f}s.")

    # Save back
    best_times[track_id] = record
    with open(BEST_TIMES_FILE, 'w') as f:
        json.dump(best_times, f, indent=4)

    invoke(launch_menu, delay=5)
    invoke(application.quit, delay=5.1)


def ordinal_suffix(n):
    if 11 <= n % 100 <= 13:
        return 'th'
    else:
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')


# ----- Lap Triggers -----
lap_trigger = Entity(
    position=start_tile.position + Vec3(0, 0.1, 0),
    scale=(25, 100, 25),
    collider='box',
    visible=False
)

middle_trigger = Entity(
    position=middle_tile.position + Vec3(0, 0.1, 0),
    scale=(25, 100, 25),
    collider='box',
    visible=False
)
# ----- debug -----
def reload_track1():
    global ai_waypoints, item_box_positions, skybox_texture, tile_texture, background_music
    global start_tile, middle_tile
    global walls, item_boxes
    global sky

    print("[INFO] Reloading tracks module from disk...")
    importlib.reload(tracks)

    print("[INFO] Clearing existing walls and item boxes...")
    for w in walls:
        destroy(w)
    walls.clear()

    for b in item_boxes:
        destroy(b)
    item_boxes.clear()

    if background_music:
        background_music.stop()

    print("[INFO] Reassigning new track1 data...")
    ai_waypoints = tracks.track1.ai_waypoints
    item_box_positions = tracks.track1.item_box_positions
    skybox_texture = tracks.track1.skybox_texture
    tile_texture = tracks.track1.tile_texture

    print("[INFO] Rebuilding walls from new data...")
    start_tile, middle_tile = tracks.create_track1(add_track_tile, walls, add_big_tile)

    print("[INFO] Spawning item boxes from new data...")
    for pos in item_box_positions:
        item_boxes.append(create_item_box(pos))

    print("[INFO] Restarting music...")
    background_music = Audio(tracks.track1.ost, loop=True, autoplay=True, volume=0.5)

    print("[INFO] Updating skybox...")
    destroy(sky)
    sky = Sky(texture=skybox_texture)

    print("[SUCCESS] Track 1 reloaded with edited code and data!")



# ----- Update Function -----
def update():
    global lap_count, has_crossed, chainsaw_timer
    coords.text = f"x: {kart.position.x:.2f}, y: {kart.position.y:.2f}, z: {kart.position.z:.2f}" #remove later debug
    middle_text.text = f"Checkpoint: {kart.passed_middle}" #remove later debug         

    global race_time, current_lap_time
    if "Player" not in finish_order and countdown_done:
        race_time += time.dt
        current_lap_time += time.dt

    if current_track == 3:
        for orb in chungus_orbs:
            if not orb.enabled:
                continue
            if distance(kart.position, orb.position) < 10:
                if orb.orb_id not in player_collected_orbs:
                    player_collected_orbs.add(orb.orb_id)
                    print(f"[CHUNGUS ORB] Collected orb {orb.orb_id}. Total: {len(player_collected_orbs)}")
                    orb.enabled = False

    race_time_text.text = f"Total: {race_time:.2f}s"
    current_lap_text.text = f"Lap Time: {current_lap_time:.2f}s"

    if current_track == 3:
        orb_count_text.text = f'Chungus Orbs: {len(player_collected_orbs)}/{required_orb_count}'
        orb_count_text.enabled = True


    laps_display = "Laps:"
    for i, t in enumerate(lap_times):
        laps_display += f"\nLap {i+1}: {t:.2f}s"
    lap_times_text.text = laps_display

    if current_track == 3:
        # Update direction every few seconds
        giant_chungus.change_dir_timer -= time.dt
        if giant_chungus.change_dir_timer <= 0:
            giant_chungus.target_direction = Vec3(
                random.uniform(-1, 1),
                0,
                random.uniform(-1, 1)
            ).normalized()
            giant_chungus.change_dir_timer = random.uniform(1, 3)  # new direction every 1–3 seconds

        # Move Chungus
        move_vec = giant_chungus.target_direction * giant_chungus.speed * time.dt
        new_pos = giant_chungus.position + move_vec

        # Clamp to map bounds
        new_pos.x = clamp(new_pos.x, -500, 500)
        new_pos.z = clamp(new_pos.z, -100, 900)

        # If he hit a wall, bounce back
        if new_pos.x in (-500, 500) or new_pos.z in (-100, 900):
            giant_chungus.target_direction *= -1
            giant_chungus.change_dir_timer = 0.1  # react fast

        giant_chungus.position = new_pos

        # Rotate for visual drama
        giant_chungus.rotation_y += 60 * time.dt

        # Collide with player
        if giant_chungus.intersects(kart.kart_hitbox).hit:
            print("[CHUNGUS COLLISION] You were body-slammed by Giant Chungus!")
            kart.speed = 0
            kart.stun_timer = 2



    if not hasattr(kart, 'slide_angle'):
        kart.slide_angle = kart.rotation_y


    # Update held item icon
    if kart.held_item:
        item_icon.texture = item_icons.get(kart.held_item)
        item_icon.enabled = True
    else:
        item_icon.enabled = False
    
    if not countdown_done and "Player" not in finish_order:
        return
    # ----- Combined keyboard + controller input -----
    forward_input = (held_keys['w'] - held_keys['s']) + (held_keys['gamepad a'] - held_keys['gamepad b'])
    turn_input = held_keys['d'] - held_keys['a'] + held_keys['gamepad left stick x']


     # Controller stick turning only
    turn_input += held_keys['gamepad left stick x']

    # ----- Use Item -----
    if (held_keys['q'] or held_keys['gamepad right trigger']) and kart.held_item:
         # Play sound for this item
        if kart.held_item in item_sounds:
            item_sounds[kart.held_item].play()
        print(f"[ITEM USE] Player used item: {kart.held_item}")

        if kart.held_item == 'jump':
            print("[ITEM EFFECT] Jump!")
            kart.vertical_speed = 8

        elif kart.held_item == 'boost':
            print("[ITEM EFFECT] Boost!")
            kart.speed += 20
            if kart.speed > kart.max_speed * 2:
                kart.speed = kart.max_speed * 2

        elif kart.held_item == 'gun':
            print("[ITEM EFFECT] Gun homing attack!")
            # Find nearest AI
            nearest_ai = None
            nearest_dist = 9999
            for ai in ai_karts:
                d = distance(kart.position, ai.position)
                if d < nearest_dist:
                    nearest_ai = ai
                    nearest_dist = d
            if nearest_ai and nearest_dist < 1000:
                print(f"Hit {nearest_ai.assigned_character} AI with gun!")
                nearest_ai.ai_speed = 0
                nearest_ai.stun_timer = 2
            else:
                print("No AI in range to hit!")

        elif kart.held_item == 'reze':
            print("[ITEM EFFECT] Reze explosion!")
            spawn_explosion(kart.position)

            for ai in ai_karts:
                d = distance(kart.position, ai.position)
                if d < 10:
                    print(f"{ai.assigned_character} AI got blasted!")
                    push_vec = (ai.position - kart.position).normalized() * 5
                    ai.position += push_vec
                    ai.ai_speed = 0
                    ai.stun_timer = 2

        elif kart.held_item == 'chainsaw':
            global chainsaw_timer
            print("[ITEM EFFECT] Chainsaw! Reduced friction for 6 seconds!")
            chainsaw_timer = 5

        # monkima skipped

        kart.held_item = None

    if chainsaw_timer > 0:
        chainsaw_timer -= time.dt

        # CHAINSAW MODE SPECIAL HANDLING
        if forward_input > 0:
            kart.speed = kart.max_speed * 1.3
        else:
            kart.speed = 0

        kart.current_friction = 1  # effectively disables friction in chainsaw mode
    else:
        # Normal mode speed handling
        if held_keys['w'] or held_keys['gamepad a'] > 0.5:
            if held_keys['shift'] or held_keys['gamepad left trigger']:
                kart.speed += (kart.acceleration*0.7) * ((kart.max_speed*0.5) - abs(kart.speed)) * time.dt
            else:
                kart.speed += kart.acceleration * (kart.max_speed - abs(kart.speed)) * time.dt

        if held_keys['s'] or held_keys['gamepad b'] > 0.5:
            if kart.speed > 0:
                kart.speed -= kart.brake_power * time.dt
                if kart.speed < 0:
                    kart.speed = 0
            else:
                kart.speed -= 0.5*kart.acceleration * (kart.max_speed - abs(kart.speed)) * time.dt
                if kart.speed < -kart.max_speed:
                    kart.speed = -kart.max_speed

        kart.current_friction = kart.friction


        
    # Always apply ground friction
    if (held_keys['shift'] or held_keys['gamepad left trigger']) and abs(turn_input) > 0.1:
        kart.speed *= kart.drift_friction
    else:
        kart.speed *= kart.current_friction
    # Drift sound control
    if (held_keys['shift'] or held_keys['gamepad left trigger']) and abs(turn_input) > 0.1:
        if not drift_sound.playing:
            drift_sound.play()
        drift_sound.volume = 0.4  # or adjust as desired
    else:
        if drift_sound.playing:
            drift_sound.stop()

    if chainsaw_timer > 0:
        # Perfect grip: lock drift angle to steering
        kart.slide_angle = kart.rotation_y
    else:
        if (held_keys['shift'] or held_keys['gamepad left trigger']) and abs(turn_input) > 0.1:
            kart.slide_angle = lerp_angle(kart.slide_angle, kart.rotation_y, 1.5 * time.dt)
        else:
            kart.slide_angle = lerp_angle(kart.slide_angle, kart.rotation_y, 6 * time.dt)

    old_position = kart.position

    if chainsaw_timer > 0:
        # perfect grip: no drift, direct steering
        facing_rad = math.radians(kart.rotation_y)
        facing_dir = Vec3(math.sin(facing_rad), 0, math.cos(facing_rad))
        kart.position += facing_dir * kart.speed * time.dt
    else:
        # normal drift/sliding
        slide_rad = math.radians(kart.slide_angle)
        slide_dir = Vec3(math.sin(slide_rad), 0, math.cos(slide_rad))
        kart.position += slide_dir * kart.speed * time.dt


    # Turning
    if turn_input:
        if chainsaw_timer > 0:
            # MASSIVELY increased turn speed in chainsaw mode
            kart.rotation_y += 200 * time.dt * turn_input
        else:
            drift_modifier = 1.0
            if held_keys['shift']:
                drift_modifier = 2.0
            kart.rotation_y += kart.turn_speed * drift_modifier * time.dt * turn_input

    
    # Stun handling
    if kart.stun_timer > 0:
        kart.stun_timer -= time.dt
        kart.rotation_y += 360 * time.dt
        kart.speed = 0
        kart_was_stunned_last_frame = True
    else:
        kart_was_stunned_last_frame = False

    # --- AI Movement: Handle stun and normal movement ---
    for ai in ai_karts:
        if not countdown_done:
            continue
        if ai.stun_timer > 0:
            ai.stun_timer -= time.dt
            ai.rotation_y += 360 * time.dt  # Faster spin for effect
            ai.ai_speed = 0
            continue  # Skip normal movement

        # --- AI Item Use: Gun ---
        if ai.held_item == 'gun':
            if random.random() < 0.4 * time.dt:  # ~40% per second chance
                # Find nearest other kart (player or other AI)
                nearest_target = None
                nearest_dist = 9999
                for other in [kart] + [a for a in ai_karts if a != ai]:
                    d = distance(ai.position, other.position)
                    if d < nearest_dist:
                        nearest_target = other
                        nearest_dist = d
                if nearest_target and nearest_dist < 1000:
                    print(f"[AI ITEM] {ai.assigned_character} used gun on {nearest_target.assigned_character if hasattr(nearest_target, 'assigned_character') else 'player'}!")
                    if item_sounds.get('gun'):
                        item_sounds['gun'].play()
                    nearest_target.ai_speed = 0 if hasattr(nearest_target, 'ai_speed') else 0
                    nearest_target.stun_timer = 2
                ai.held_item = None
        # --- AI Item Use: Boost ---
        elif ai.held_item == 'boost':
            if random.random() < 0.4 * time.dt:
                ai.ai_speed += 20
                if ai.ai_speed > ai.ai_max_speed * 2:
                    ai.ai_speed = ai.ai_max_speed * 2
                if item_sounds.get('boost'): item_sounds['boost'].play()
                ai.held_item = None
        # --- AI Item Use: Jump ---
        elif ai.held_item == 'jump':
            if random.random() < 0.4 * time.dt:
                ai.vertical_speed = 8
                if item_sounds.get('jump'): item_sounds['jump'].play()
                ai.held_item = None
        # --- AI Item Use: Chainsaw ---
        elif ai.held_item == 'chainsaw':
            if random.random() < 0.4 * time.dt:
                if item_sounds.get('chainsaw'):
                    item_sounds['chainsaw'].play()
                ai.held_item = None
        # --- AI Item Use: Reze ---
        elif ai.held_item == 'reze':
            # Check if anyone is in blast range
            blast_radius = 10
            targets_in_range = [
                target for target in [kart] + [other_ai for other_ai in ai_karts if other_ai != ai]
                if distance(ai.position, target.position) < blast_radius
            ]

            if targets_in_range or random.random() < 0.2 * time.dt:
                print(f"[AI ITEM] {ai.assigned_character} used reze!")
                if item_sounds.get('reze'):
                    item_sounds['reze'].play()

                spawn_explosion(ai.position)

                # Damage all other karts in radius except self
                for target in targets_in_range:
                    print(f"{getattr(target, 'assigned_character', 'player')} got blasted!")
                    push_vec = (target.position - ai.position).normalized() * 5
                    target.position += push_vec
                    if hasattr(target, 'ai_speed'):
                        target.ai_speed = 0
                        target.stun_timer = 2
                    else:
                        kart.speed = 0
                        kart.stun_timer = 2

                ai.held_item = None
        # --- AI Item Use: Monkima ---
        elif ai.held_item == 'monkima':
            if random.random() < 0.5 * time.dt:
                print(f"[AI ITEM] {ai.assigned_character} used monkima!")
                if item_sounds.get('monkima'):
                    item_sounds['monkima'].play()
                show_monkima_overlay()
                ai.held_item = None



        # Normal AI movement
        target = ai.waypoints[ai.waypoint_index]
        target = Vec3(target.x, ai.y, target.z)

        # Bias toward center line
        ideal_center_wp = ai_waypoints[ai.waypoint_index]
        distance_from_center = distance(ai.position, ideal_center_wp)
        center_weight = clamp(0.1 + 0.02 * distance_from_center, 0.1, 0.4)
        adjusted_target = lerp(target, ideal_center_wp, center_weight)

        dir_vec = Vec3(adjusted_target.x - ai.x, 0, adjusted_target.z - ai.z)

        if dir_vec.length() > 0.1:
            dir_vec = dir_vec.normalized()
            desired_angle = math.degrees(math.atan2(dir_vec.x, dir_vec.z))
            angle_diff = (desired_angle - ai.rotation_y + 540) % 360 - 180

            if abs(angle_diff) > 30:
                ai.ai_speed *= 0.95
            if abs(angle_diff) > 60:
                ai.ai_speed *= 0.85

            ai.rotation_y += clamp(angle_diff, -ai.ai_turn_speed * time.dt, ai.ai_turn_speed * time.dt)

        dist_to_wp = distance(ai.position, target)
        prev_index = (ai.waypoint_index - 1) % len(ai.waypoints)
        previous_wp = Vec3(ai_waypoints[prev_index].x, ai.y, ai_waypoints[prev_index].z)
        dist_to_prev = distance(ai.position, previous_wp)

        combined_dist = min(dist_to_wp, dist_to_prev)
        approach_slowdown = clamp(combined_dist / 20, 0.6, 1)

        speed_cap = ai.ai_max_speed * approach_slowdown
        if ai.ai_speed < speed_cap:
            ai.ai_speed += ai.ai_acceleration * (speed_cap - ai.ai_speed) * time.dt
        else:
            ai.ai_speed *= kart.current_friction

        rad_ai = math.radians(ai.rotation_y)
        forward_ai = Vec3(math.sin(rad_ai), 0, math.cos(rad_ai))
        ai.position += forward_ai * ai.ai_speed * time.dt

        if distance(ai.position, target) < 2:
            ai.waypoint_index = (ai.waypoint_index + 1) % len(ai.waypoints)


    # Player engine sound
    if abs(kart.speed) < 0.5:
        kart.engine_audio.volume = 0
    else:
        kart.engine_audio.volume = clamp(abs(kart.speed) / kart.max_speed, 0, 1)
    kart.engine_audio.pitch = 1.0 + 0.5 * clamp(abs(kart.speed) / kart.max_speed, 0, 1)

    # AI engine sounds
    for ai in ai_karts:
        if abs(ai.ai_speed) < 0.5:
            ai.engine_audio.volume = 0
        else:
            # Basic volume from speed
            base_volume = clamp(abs(ai.ai_speed) / ai.ai_max_speed, 0, 1)

            # Distance factor (hear better when closer)
            dist = distance(kart.position, ai.position)
            dist_factor = clamp(1 - (dist / 50), 0, 1)  # 50 units = fade-out range

            # Final volume
            ai.engine_audio.volume = base_volume * dist_factor

        ai.engine_audio.pitch = 1.0 + 0.5 * clamp(abs(ai.ai_speed) / ai.ai_max_speed, 0, 1)


    all_karts = [kart] + ai_karts

    # Gravity & Grounding
    ignore_list = all_karts + [kart.kart_hitbox]
    ray = raycast(kart.position + Vec3(0, 0.5, 0), Vec3(0, -1, 0), distance=1, ignore=ignore_list)
    if ray.hit and kart.vertical_speed <= 0:
        kart.vertical_speed = 0
        kart.y = ray.world_point.y + 0.25
        kart.air_timer = 0  # Reset air timer on landing
        kart.on_ground = True
    else:
        kart.vertical_speed -= kart.gravity * time.dt
        kart.y += kart.vertical_speed * time.dt
        kart.air_timer += time.dt  # Count air time


    # --- AI Gravity & Grounding ---
    for ai in ai_karts:
        ray = raycast(ai.position + Vec3(0, 0.5, 0), Vec3(0, -1, 0), distance=1, ignore=all_karts)
        if ray.hit:
            ai.vertical_speed = 0
            ai.y = ray.world_point.y + 0.25
        else:
            ai.vertical_speed -= ai.gravity * time.dt
            ai.y += ai.vertical_speed * time.dt

    # Player vs AI simple collision push
    for ai in ai_karts:
        offset = kart.position - ai.position
        offset.y = 0
        dist = offset.length()
        if dist < 1.5 and dist > 0:
            push = offset.normalized() * (1.5 - dist) * 0.5
            kart.position += push
            ai.position -= push

    #AI vs AI simple collision push
    for i in range(len(ai_karts)):
        for j in range(i+1, len(ai_karts)):
            offset = ai_karts[i].position - ai_karts[j].position
            offset.y = 0
            dist = offset.length()
            if dist < 1.5 and dist > 0:
                push = offset.normalized() * (1.5 - dist) * 0.5
                ai_karts[i].position += push
                ai_karts[j].position -= push

    # Kart vs walls simple collision push
    for wall in walls:
        if kart.kart_hitbox.intersects(wall).hit:
            print(f"[WALL COLLISION] Reset to old position, speed zeroed from {kart.speed:.2f}")
            kart.position = old_position
            kart.speed = 0

        limit = 1.5
        if dist < limit:
            # Snap back to old position if collided
            kart.position = old_position
            kart.speed = 0  # optional, stop forward speed

    # Fall reset if hits debug floor
    if kart.y < -19:
        print(f"[FALL RESET] Fell below -19. Y: {kart.y:.2f}, speed was {kart.speed:.2f}")
        kart.position = spawn_position
        kart.rotation_y = 0
        kart.vertical_speed = 0
        kart.speed = 0
        kart.passed_middle = False

    # ----- Item Box Collection -----
    for box in item_boxes:
        if box.respawn_timer > 0:
            box.respawn_timer -= time.dt
            if box.respawn_timer <= 0:
                box.enabled = True
            continue

        # Player collision
        if distance(kart.position, box.position) < 2:
            if kart.held_item is None:
                kart.held_item = choice(items)
                print(f"[ITEM BOX] Player collected item: {kart.held_item}")
            else:
                print("[ITEM BOX] Player hit box but already has item!")
            box.enabled = False
            box.respawn_timer = 2

        # AI collision
        for ai in ai_karts:
            if distance(ai.position, box.position) < 2:
                if ai.held_item is None:
                    ai.held_item = choice(items)
                    print(f"[ITEM BOX] {ai.assigned_character} collected item: {ai.held_item}")
                else:
                    print(f"[ITEM BOX] {ai.assigned_character} hit box but already has item!")
                box.enabled = False
                box.respawn_timer = 2



    # Lap counting
    global lap_count, has_crossed
    if lap_trigger.intersects(kart.kart_hitbox).hit:
        if not has_crossed and kart.speed > 2 and kart.passed_middle:
            if current_track == 3 and len(player_collected_orbs) < required_orb_count:
                countdown_text.text = "COLLECT ALL ORBS!"
                countdown_text.enabled = True
                countdown_text.color = color.red
                invoke(lambda: setattr(countdown_text, 'enabled', False), delay=2)
            else:
                lap_count += 1
                lap_times.append(current_lap_time)
                current_lap_time = 0
                if ((current_track == 3 and lap_count >= 1) or lap_count >= 3) and "Player" not in finish_order:
                    finish_order.append("Player")
                    show_results_screen()
                lap_text.text = f"Lap {lap_count+1}"
                has_crossed = True
                kart.passed_middle = False


    else:
        has_crossed = False
    # AI lap counting
    for ai in ai_karts:
        if lap_trigger.intersects(ai).hit:
            if not ai.has_crossed and ai.ai_speed > 2 and ai.passed_middle:
                ai.laps += 1
                print(f"{ai.assigned_character} AI completed lap {ai.laps}")
                ai.has_crossed = True
                ai.passed_middle = False
                if ai.laps >= 3 and f"AI {ai_karts.index(ai)+1}" not in finish_order:
                    finish_order.append(f"AI {ai_karts.index(ai)+1}")
        else:
            ai.has_crossed = False

        if middle_trigger.intersects(ai).hit:
            ai.passed_middle = True

    # Middle checkpoint
    if middle_trigger.intersects(kart.kart_hitbox).hit:
        kart.passed_middle = True

    # 🎥 Camera
    global camera_yaw

    # If stun just ended this frame
    if kart_was_stunned_last_frame and kart.stun_timer <= 0:
        camera_yaw = kart.rotation_y

    if kart.stun_timer <= 0:
        camera_yaw = lerp(camera_yaw, kart.rotation_y, 3 * time.dt)

    kart_was_stunned_last_frame = kart.stun_timer > 0

    if current_track == 3:
        cam_distance = 50
        cam_height = 20  # raised for dramatic Chungus viewing
    else:
        cam_distance = 20
        cam_height = 7

    # Use lagged camera_yaw instead of kart.rotation_y
    yaw_rad = math.radians(camera_yaw)
    behind = Vec3(-math.sin(yaw_rad), 0, -math.cos(yaw_rad)) * cam_distance

    camera.position = kart.position + behind + Vec3(0, cam_height, 0)
    camera.rotation_x = 15
    camera.rotation_y = camera_yaw
    camera.rotation_z = 0
    if chainsaw_timer > 0:
        shake_amount = 1.1 * math.sin(time.time() * 20)  # rapid oscillation
        camera.fov = 65 + shake_amount  # base higher FOV plus shake
    else:
        speed_ratio = clamp(abs(kart.speed) / kart.max_speed, 0, 1)
        camera.fov = lerp(base_fov, max_fov, speed_ratio)

    if current_track == 3:
        if distance(kart.position, giant_chungus.position) < 100:
            camera.shake(1)


    # --- Spin Item Boxes ---
    for box in item_boxes:
        if box.enabled:
            box.rotation_y += 60 * time.dt

    # --- Spin Item Boxes ---
    if current_track == 3:
        for orb in chungus_orbs:
            if orb.enabled:
                orb.rotation_y += 100 * time.dt


    # ----- debug -----
    if held_keys['f1']:
        reload_track1()

def on_game_start():
    print("Game started!")
    start_countdown()


def start_countdown():
    global countdown_text, camera_locked_for_countdown

    countdown_text.text = '3'
    camera.position = kart.position + Vec3(12, 8, 5)
    camera.look_at(kart)
    countdown_text.enabled = True

    def cam_view_2():
        camera.position = kart.position + Vec3(-8, 3, -12)
        camera.look_at(kart)

    def cam_view_1():
        camera.position = kart.position + Vec3(5, 10, 5)
        camera.look_at(kart)

    def cam_view_go():
        camera.position = kart.position + Vec3(-15, 12, -5)
        camera.look_at(kart)

    def set_2():
        countdown_text.text = '2'
        cam_view_2()

    def set_1():
        countdown_text.text = '1'
        cam_view_1()

    def set_go():
        countdown_text.text = 'GO!'
        cam_view_go()
        enable_race()  # allow player to start immediately

    def enable_race():
        global countdown_done, race_started, camera_locked_for_countdown
        countdown_done = True
        race_started = True
        camera_locked_for_countdown = False

    def hide_go():
        countdown_text.enabled = False

    Sequence(
        1,
        Func(set_2),
        1,
        Func(set_1),
        1,
        Func(set_go),
        1,
        Func(hide_go)
    ).start()

    if current_track == 3:
        def spawn_bombs_loop():
            drop_random_bomb()
            invoke(spawn_bombs_loop, delay=(1/bombs_per_second))
        spawn_bombs_loop()


invoke(on_game_start, delay=1)


sky = Sky(texture=skybox_texture)

app.run()