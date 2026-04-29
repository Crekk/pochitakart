from ursina import *
import math
from ursina.lights import DirectionalLight
from ursina import AmbientLight
from ursina.shaders import lit_with_shadows_shader
from random import sample
from random import choice


app = Ursina()
window.title = 'Pochita Kart'
window.fps_counter.enabled = True
camera_yaw = 0
base_fov = 35
max_fov = base_fov + 25
chainsaw_timer = 0
kart_was_stunned_last_frame = False

# ----- Sounds -----
item_sounds = {
    'jump': Audio('jump.mp3', autoplay=False),
    'boost': Audio('boost.mp3', autoplay=False),
    'gun': Audio('gun.mp3', autoplay=False),
    'chainsaw': Audio('chainsaw.mp3', autoplay=False),
    'reze': Audio('reze.mp3', autoplay=False),
    'monkima': Audio('monkima.mp3', autoplay=False)
}
engine_sound_file = 'engine_loop.mp3'
drift_sound = Audio('drift.mp3', loop=True, autoplay=False, volume=0)
background_music = Audio('bg_music.mp3', loop=True, autoplay=True, volume=0.5)



# ----- Track Tile Function -----
def add_track_tile(x, z, rotation=0, vrotation=0, y=0, texture=None):
    tile = Entity(
        model='cube',
        texture='road.jpg',
        shader=lit_with_shadows_shader,
        position=(x, y, z),
        scale=(10, 0.1, 10),
        collider='box'
    )
    tile.rotation_y = rotation
    tile.rotation_x = vrotation
    return tile

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


# ===== Balanced Long Track with Variety (≈100 tiles, 1–2 min lap) =====

# Straight start (north)

add_track_tile(0, -10, 0)  # Start tile

start_tile = add_track_tile(0, 0, 0, 0, 0.1)
start_tile.color = color.green  # visually distinct

middle_tile = add_track_tile(-20, 185, 270, 0, 2.01)
middle_tile.color = color.azure

for z in range(10, 60, 10):
    add_track_tile(0, z)

for i in range(0, 30, 5): 
    add_track_tile(i, 55+i, 45)

for y in range(85, 135, 10):
    add_track_tile(25, y, 180)

for x in range(20, -10, -10):
    add_track_tile(x, 125, 270)

for y in range(115, 75, -10):
    add_track_tile(0, y, 0)

for x in range(10, 10, 10):
    add_track_tile(x, 85, 90)

add_track_tile(8, 85, 90, -35, 3)
add_track_tile(16, 85, 90, -35, 8)

for x in range (30, 130, 10):
    add_track_tile(x, 85, 90, 0, 4)

for i in range(0, 30, 5):
    add_track_tile(120 + i, 85 + i, 135, -20, 4 - i * 0.1)

for i in range(0, 30, 5):
    add_track_tile(150 - i, 115 + i, 225, 20, 1 - i * 0.1)

for z in range(155, 205, 10):
    add_track_tile(120, z, 180, 0 , -5)

for i in range(0, 30, 5):
    add_track_tile(120 + i, 195 + i, 135, 0, -5)

for i in range(0, 50, 10):
    add_track_tile(150 + i, 225 + i, 225, 30, -5 + i * 0.3)

for x in range(200, 100, -10):
    add_track_tile(x, 275, 270, 0, 0)

# --- Ramps with jumps west ---
for i in range(0, 50, 10):
    add_track_tile(100 - i, 275, 270, -15, i * 0.2)

# Flat landing after ramps
for x in range(50, 0, -10):
    add_track_tile(x, 275, 270, 0, 1)

# --- Northward ramps toward start ---
for i in range(0, 50, 10):
    add_track_tile(0, 275 - i, 0, 45, 1 + i * 0.2)

# Flat north section to finish
for z in range(225, 175, -10):
    add_track_tile(0, z, 0, 0, 2)

# Turn left (west) along x-
for x in range(0, -50, -10):
    add_track_tile(x, 185, 270, 0, 2)

# --- Final interesting segment heading north (-z) ---

# Ramp-up north
for i in range(0, 50, 10):
    add_track_tile(-40, 185 - i, 0, 10, 2 + i * 0.2)

# Flat north stretch
for z in range(135, 85, -10):
    add_track_tile(-40, z, 0, 0, 3)


# Zig right
for i in range(0, 15, 5):
    add_track_tile(-40 + i, 95 - i, 45, 0, 3)

# Zig right
for i in range(0, 30, 5):
    add_track_tile(-40 + i, 85 - i, 45, 0, 3)

# Zig left
for i in range(0, 30, 5):
    add_track_tile(-10 - i, 55 - i, 315, 0, 3)

# Zig right again
for i in range(0, 10, 5):
    add_track_tile(-40 + i, 25 - i, 45, 0, 3)
# Zig left
for i in range(0, 20, 5):
    add_track_tile(-30 - i, 15 - i, 315, 0, 3)

# Zig right
for i in range(0, 20, 5):
    add_track_tile(-50 + i, -5 - i, 45, 0, 3)

# --- Harsh turn back toward 0,0 ---

# Sharp west swing
for x in range(-30, -70, -10):
    add_track_tile(x, -25, 270, 0, 3)

# North leg
for z in range(-25, -75, -10):
    add_track_tile(-70, z, 0, 0, 3)

# East return
for x in range(-60, 10, 10):
    add_track_tile(x, -65, 90, 0, 3)

# Final north back home
for z in range(-65, -15, 10):
    add_track_tile(0, z, 0, 0, 3)

walls = []

walls.append(Entity(
    model='cube',
    color=color.dark_gray,
    position=(-13.5, 4, 44.5),
    scale=(0.5, 2, 30),
    rotation_y=45,
    collider='box'
))
walls.append(Entity(
    model='cube',
    color=color.dark_gray,
    position=(-12.5, 4, 64.5),
    scale=(30, 2, 0.5),
    rotation_y=45,
    collider='box'
))


# ----- Debug Floor -----
debug_floor = Entity(model='plane', scale=100, y=-20, color=color.black33, collider='box')

# ----- Kart -----
spawn_position = Vec3(0, 1, 0)
kart = Entity(
    model='pochita.obj',
    texture='pochita.png',
    scale=1.5,
    collider='box',
    position=spawn_position,
)

kart.position = spawn_position
kart.gravity = 9
kart.vertical_speed = 0
kart.air_timer = 0
kart.passed_middle = False
kart.collider = BoxCollider(kart, center=(0,0.25,0), size=(1, 0.5, 2))
kart.held_item = None #testing
kart.stun_timer = 0  # Timer for stun effect
kart.on_ground = False  # Track if kart is on the ground
kart.engine_audio = Audio(engine_sound_file, loop=True, autoplay=True, volume=0)


kart_hitbox = Entity(
    parent=kart,
    model='cube',
    scale=(1, 1, 2),
    collider='box',
    position=(0,0.25,0),  # match your offset
    visible=False
)


# ----- Movement Vars -----
speed = 0
max_speed = 27
acceleration = 0.5
turn_speed = 60
friction = 0.9998
drift_friction = 0.995  # Friction when drifting

# ----- AI Waypoints -----
ai_waypoints = [
    Vec3(0, 0, 52),
    Vec3(24, 0, 79),
    Vec3(24, 0, 122),
    Vec3(3, 0, 124),
    Vec3(1, 0, 86),
    Vec3(119, 0, 84),
    Vec3(148, 0, 112),
    Vec3(123, 0, 143),
    Vec3(121, 0, 195),
    Vec3(198, 0, 273),
    Vec3(135, 0, 274),
    Vec3(8, 0, 278),
    Vec3(-2, 0, 277),
    Vec3(0, 0, 186),
    Vec3(-39, 0, 185), 
    Vec3(-39, 0, 100),
    Vec3(-35, 0, 86),
    Vec3(-11, 0, 56),
    Vec3(-39, 0, 25),
    Vec3(-30, 0, 15),
    Vec3(-50, 0, -4),
    Vec3(-34, 0, -22),
    Vec3(-67, 0, -24),
    Vec3(-69, 0, -65),
    Vec3(0, 0, -64),
    Vec3(0, 0, 0),
]
# ----- Item Boxes -----
item_box_positions = [
    Vec3(21, 1, 93),
    Vec3(23, 1, 93),
    Vec3(25, 1, 93),

    Vec3(80, 5, 85),
    Vec3(80, 5, 83),
    Vec3(80, 5, 87),

    Vec3(120, 1, 274),
    Vec3(120, 1, 272),
    Vec3(120, 1, 276),

    Vec3(-20, 3, 185),
    Vec3(-20, 3, 183),
    Vec3(-20, 3, 187),
    
    Vec3(-35, 4, -23),
    Vec3(-40, 4, -20),
    Vec3(-30, 4, -27),

    Vec3(0, 4, -24),
    Vec3(-2, 4, -24),
    Vec3(2, 4, -24),
]

# ---- Item Box Entities ----
item_boxes = []
for pos in item_box_positions:
    box = Entity(
        model='cube',
        color=color.orange,
        position=pos,
        scale=(1, 1, 1),
        collider='box',
        rotation_y=0
    )
    box.respawn_timer = 0
    item_boxes.append(box)

# ----- Items -----
#items = ['jump', 'boost', 'gun', 'chainsaw', 'reze', 'monkima']
items = ['gun']

# ----- AI Karts -----
ai_karts = []
ai_textures = ['pochita_green.png', 'pochita_blue.png', 'pochita_purple.png']

for i in range(3):
    offset = Vec3((i - 1) * 3, 0, 5)
    ai_kart = Entity(
        model='pochita.obj',
        texture=ai_textures[i],
        scale=1.5,
        collider='box',
        position=spawn_position + offset,
    )
    ai_kart.gravity = 9
    ai_kart.vertical_speed = 0
    ai_kart.ai_speed = 0
    ai_kart.waypoint_index = 0
    ai_kart.held_item = None
    ai_kart.stun_timer = 0
    ai_kart.engine_audio = Audio(engine_sound_file, loop=True, autoplay=True, volume=0)

    # AI personality
    if i == 0:      # green pocher
        ai_kart.ai_max_speed = 60
        ai_kart.ai_acceleration = 0.6
        ai_kart.ai_turn_speed = 100
    elif i == 1:    # blue pocher
        ai_kart.ai_max_speed = 40
        ai_kart.ai_acceleration = 20
        ai_kart.ai_turn_speed = 110
    else:           # purple pocher
        ai_kart.ai_max_speed = 50
        ai_kart.ai_acceleration = 1
        ai_kart.ai_turn_speed = 1000

    ai_kart.waypoints = ai_waypoints

    # 🏁 Add lap-tracking variables for AI
    ai_kart.laps = 0
    ai_kart.passed_middle = False
    ai_kart.has_crossed = False

    ai_karts.append(ai_kart)


# ----- Lap Counter -----
lap_count = 0
race_time = 0
lap_times = []
current_lap_time = 0
race_time_text = Text(text=f"Total: 0.00s", position=(0.60, 0.40), scale=2, origin=(0,0), background=True)
current_lap_text = Text(text=f"Lap Time: 0.00s", position=(0.60, 0.35), scale=2, origin=(0,0), background=True)
lap_times_text = Text(text=f"Laps:", position=(0.60, 0.25), scale=2, origin=(0,0), background=True)
lap_text = Text(text=f"Lap {lap_count+1}", position=(-0.70, 0.40), scale=2, origin=(0, 0), background=True)
coords = Text(text=f"x: {kart.position.x}, y: {kart.position.y}, z: {kart.position.z}", position=(-0.60, 0.30), scale=2, origin=(0, 0), background=True) # remove later debug
middle_text = Text(
    text=f"Checkpoint: {kart.passed_middle}",
    position=(-0.70, 0.20),
    scale=2,
    origin=(0, 0),
    background=True
)

has_crossed = False  # Prevent double counting per lap

# ----- UI -----
item_icons = {
    'boost': 'boost_icon.png',
    'jump': 'jump_icon.png',
    'gun': 'gun_icon.png',
    'chainsaw': 'chainsaw_icon.png',
    'reze': 'reze_icon.png',
    'monkima': 'monkima_icon.png'
}

item_text = Text(
    text="Item: None",
    position=(-0.70, 0.10),
    scale=2,
    origin=(0, 0),
    background=True
)
item_icon = Entity(
    parent=camera.ui,
    model='quad',
    texture=None,
    scale=(0.1, 0.1),
    position=(-0.7, 0.1),
    enabled=False
)



# ----- Lap Triggers -----
lap_trigger = Entity(
    position=start_tile.position + Vec3(0, 0.1, 0),
    scale=(10, 5, 10),
    collider='box',
    visible=False
)

middle_trigger = Entity(
    position=middle_tile.position + Vec3(0, 0.1, 0),
    scale=(10, 5, 10),
    collider='box',
    visible=False
)



# ----- Update Function -----
def update():
    global speed, lap_count, has_crossed, chainsaw_timer
    coords.text = f"x: {kart.position.x:.2f}, y: {kart.position.y:.2f}, z: {kart.position.z:.2f}" #remove later debug
    middle_text.text = f"Checkpoint: {kart.passed_middle}" #remove later debug         

    global race_time, current_lap_time
    race_time += time.dt
    current_lap_time += time.dt

    race_time_text.text = f"Total: {race_time:.2f}s"
    current_lap_text.text = f"Lap Time: {current_lap_time:.2f}s"

    laps_display = "Laps:"
    for i, t in enumerate(lap_times):
        laps_display += f"\nLap {i+1}: {t:.2f}s"
    lap_times_text.text = laps_display


    if not hasattr(kart, 'slide_angle'):
        kart.slide_angle = kart.rotation_y


    # Update held item icon
    if kart.held_item:
        item_icon.texture = item_icons.get(kart.held_item)
        item_icon.enabled = True
    else:
        item_icon.enabled = False

    # Update held item UI
    if kart.held_item:
        item_text.text = f"Item: {kart.held_item}"
    else:
        item_text.text = "Item: None"

    # ----- Combined keyboard + controller input -----
    forward_input = held_keys['w'] - held_keys['s']
    turn_input = held_keys['d'] - held_keys['a']

     # Controller stick turning only
    turn_input += held_keys['gamepad left stick x']
        # Controller buttons for forward/back
    if held_keys['gamepad a']:
        forward_input += 1
    if held_keys['gamepad b']:
        forward_input -= 1



    # ----- Use Item -----
    if held_keys['q'] and kart.held_item:
         # Play sound for this item
        if kart.held_item in item_sounds:
            item_sounds[kart.held_item].play()
        print(f"[ITEM USE] Player used item: {kart.held_item}")

        if kart.held_item == 'jump':
            print("[ITEM EFFECT] Jump!")
            kart.vertical_speed = 12

        elif kart.held_item == 'boost':
            print("[ITEM EFFECT] Boost!")
            speed += 20
            if speed > max_speed * 2:
                speed = max_speed * 2

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
                print(f"Hit {nearest_ai.texture} AI with gun!")
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
                    print(f"{ai.texture} AI got blasted!")
                    push_vec = (ai.position - kart.position).normalized() * 5
                    ai.position += push_vec
                    ai.ai_speed = 0
                    ai.stun_timer = 2

        elif kart.held_item == 'chainsaw':
            global chainsaw_timer
            print("[ITEM EFFECT] Chainsaw! Reduced friction for 5 seconds!")
            chainsaw_timer = 5

        # monkima skipped

        kart.held_item = None


    if held_keys['space']:
        kart.y += 0.5#testing


    if chainsaw_timer > 0:
        chainsaw_timer -= time.dt

        # CHAINSAW MODE SPECIAL HANDLING
        if forward_input > 0:
            speed = max_speed
        else:
            speed = 0

        current_friction = 1  # effectively disables friction in chainsaw mode
    else:
        # Normal mode speed handling
        if held_keys['w']:
            speed += acceleration * (max_speed - abs(speed)) * time.dt

        if held_keys['s']:
            brake_strength = 10
            if speed > 0:
                speed -= brake_strength * time.dt
                if speed < 0:
                    speed = 0
            elif speed < 0:
                speed += brake_strength * time.dt
                if speed > 0:
                    speed = 0

        current_friction = friction


        
    # Always apply ground friction
    if held_keys['shift']:
        speed *= drift_friction
    else:
        speed *= current_friction
    # Drift sound control
    if held_keys['shift']:
        if not drift_sound.playing:
            drift_sound.play()
        drift_sound.volume = 0.7  # or adjust as desired
    else:
        if drift_sound.playing:
            drift_sound.stop()

    if chainsaw_timer > 0:
        # Perfect grip: lock drift angle to steering
        kart.slide_angle = kart.rotation_y
    else:
        if held_keys['shift']:
            kart.slide_angle = lerp_angle(kart.slide_angle, kart.rotation_y, 1.5 * time.dt)
        else:
            kart.slide_angle = lerp_angle(kart.slide_angle, kart.rotation_y, 6 * time.dt)

    old_position = kart.position

    if chainsaw_timer > 0:
        # perfect grip: no drift, direct steering
        facing_rad = math.radians(kart.rotation_y)
        facing_dir = Vec3(math.sin(facing_rad), 0, math.cos(facing_rad))
        kart.position += facing_dir * speed * time.dt
    else:
        # normal drift/sliding
        slide_rad = math.radians(kart.slide_angle)
        slide_dir = Vec3(math.sin(slide_rad), 0, math.cos(slide_rad))
        kart.position += slide_dir * speed * time.dt





            
    #if kart.vertical_speed == 0 and abs(speed) < 0.5:
        #print(f"[FRICTION STOP] Speed dropping below threshold: {speed:.2f}")


    # Turning
    if turn_input:
        if chainsaw_timer > 0:
            # MASSIVELY increased turn speed in chainsaw mode
            kart.rotation_y += 200 * time.dt * turn_input
        else:
            drift_modifier = 1.0
            if held_keys['shift']:
                drift_modifier = 2.0
            kart.rotation_y += turn_speed * drift_modifier * time.dt * turn_input

    
    # Stun handling
    if kart.stun_timer > 0:
        kart.stun_timer -= time.dt
        kart.rotation_y += 360 * time.dt
        speed = 0
        kart_was_stunned_last_frame = True
    else:
        kart_was_stunned_last_frame = False

    # --- AI Movement: Handle stun and normal movement ---
    for ai in ai_karts:
        if ai.stun_timer > 0:
            ai.stun_timer -= time.dt
            ai.rotation_y += 360 * time.dt  # Faster spin for effect
            ai.ai_speed = 0
            continue  # Skip normal movement

        # --- AI Item Use: Gun ---
        if ai.held_item == 'gun':
            if random.random() < 0.2 * time.dt:  # ~20% per second chance
                # Find nearest other kart (player or other AI)
                nearest_target = None
                nearest_dist = 9999
                for other in [kart] + [a for a in ai_karts if a != ai]:
                    d = distance(ai.position, other.position)
                    if d < nearest_dist:
                        nearest_target = other
                        nearest_dist = d
                if nearest_target and nearest_dist < 1000:
                    print(f"[AI ITEM] {ai.texture} used gun on {nearest_target.texture if hasattr(nearest_target, 'texture') else 'player'}!")
                    if item_sounds.get('gun'):
                        item_sounds['gun'].play()
                    nearest_target.ai_speed = 0 if hasattr(nearest_target, 'ai_speed') else 0
                    nearest_target.stun_timer = 2
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
            ai.ai_speed *= current_friction

        rad_ai = math.radians(ai.rotation_y)
        forward_ai = Vec3(math.sin(rad_ai), 0, math.cos(rad_ai))
        ai.position += forward_ai * ai.ai_speed * time.dt

        if distance(ai.position, target) < 2:
            ai.waypoint_index = (ai.waypoint_index + 1) % len(ai.waypoints)


    # Player engine sound
    if abs(speed) < 0.5:
        kart.engine_audio.volume = 0
    else:
        kart.engine_audio.volume = clamp(abs(speed) / max_speed, 0, 1)
    kart.engine_audio.pitch = 1.0 + 0.5 * clamp(abs(speed) / max_speed, 0, 1)

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
    ignore_list = all_karts + [kart_hitbox]
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
        if kart_hitbox.intersects(wall).hit:
            print(f"[WALL COLLISION] Reset to old position, speed zeroed from {speed:.2f}")
            kart.position = old_position
            speed = 0

        limit = 1.5
        if dist < limit:
            # Snap back to old position if collided
            kart.position = old_position
            speed = 0  # optional, stop forward speed

    # Fall reset if hits debug floor
    if kart.y < -19:
        print(f"[FALL RESET] Fell below -19. Y: {kart.y:.2f}, speed was {speed:.2f}")
        kart.position = spawn_position
        kart.rotation_y = 0
        kart.vertical_speed = 0
        speed = 0
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
                    print(f"[ITEM BOX] {ai.texture} collected item: {ai.held_item}")
                else:
                    print(f"[ITEM BOX] {ai.texture} hit box but already has item!")
                box.enabled = False
                box.respawn_timer = 2



    # Lap counting
    global lap_count, has_crossed
    if lap_trigger.intersects(kart_hitbox).hit:
        if not has_crossed and speed > 2 and kart.passed_middle:
            lap_count += 1
            lap_text.text = f"Lap {lap_count+1}"
            has_crossed = True
            kart.passed_middle = False

            # Store this lap's time
            lap_times.append(current_lap_time)
            current_lap_time = 0
    else:
        has_crossed = False
    # AI lap counting
    for ai in ai_karts:
        if lap_trigger.intersects(ai).hit:
            if not ai.has_crossed and ai.ai_speed > 2 and ai.passed_middle:
                ai.laps += 1
                print(f"{ai.texture} AI completed lap {ai.laps}")
                ai.has_crossed = True
                ai.passed_middle = False
        else:
            ai.has_crossed = False

        if middle_trigger.intersects(ai).hit:
            ai.passed_middle = True

    # Middle checkpoint
    if middle_trigger.intersects(kart_hitbox).hit:
        kart.passed_middle = True

    # 🎥 Camera
    global camera_yaw

    # If stun just ended this frame
    if kart_was_stunned_last_frame and kart.stun_timer <= 0:
        camera_yaw = kart.rotation_y

    if kart.stun_timer <= 0:
        camera_yaw = lerp(camera_yaw, kart.rotation_y, 3 * time.dt)

    kart_was_stunned_last_frame = kart.stun_timer > 0




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
        camera.fov = 50  # Fixed FOV in chainsaw mode
    else:
        speed_ratio = clamp(abs(speed) / max_speed, 0, 1)
        camera.fov = lerp(base_fov, max_fov, speed_ratio)


    # --- Spin Item Boxes ---
    for box in item_boxes:
        if box.enabled:
            box.rotation_y += 60 * time.dt


def on_game_start():
    print("Game started!")
    #kart.position = Vec3(0, 5, 5)

invoke(on_game_start, delay=1)


sky = Sky()
sky.color = color.red

app.run()