from ursina import *
import math

app = Ursina()
window.title = 'Pochita Kart'
window.fps_counter.enabled = True

# ----- Track Tile Function -----
def add_track_tile(x, z, rotation=0, vrotation=0, y=0):
    tile = Entity(
        model='cube',
        color=color.gray,
        position=(x, y, z),
        scale=(10, 0.1, 10),
        collider='box'
    )
    tile.rotation_y = rotation      # horizontal (yaw)
    tile.rotation_x = vrotation     # vertical tilt (pitch)
    return tile


# ===== Balanced Long Track with Variety (≈100 tiles, 1–2 min lap) =====

# Straight start (north)
start_tile = add_track_tile(0, 0, 0, 0, 0.1)
start_tile.color = color.green  # visually distinct

middle_tile = add_track_tile(0, 185, 270, 0, 2.01)
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


# ----- Debug Floor -----
debug_floor = Entity(model='plane', scale=100, y=-20, color=color.black33, collider='box')

# ----- Kart -----
spawn_position = Vec3(0, 5, 0)
kart = Entity(model='cube', color=color.orange, scale=(1, 0.5, 2), collider='box')
kart.position = spawn_position
kart.gravity = 9
kart.vertical_speed = 0
kart.passed_middle = False

# ----- Movement Vars -----
speed = 0
max_speed = 20
acceleration = 0.5
turn_speed = 90
friction = 0.95

# ----- Lap Counter -----
lap_count = 0
lap_text = Text(text=f"Lap {lap_count+1}", position=(-0.70, 0.40), scale=2, origin=(0, 0), background=True)
coords = Text(text=f"x: {kart.position.x}, z: {kart.position.z}", position=(-0.70, 0.30), scale=2, origin=(0, 0), background=True) # remove later debug
middle_text = Text(
    text=f"Checkpoint: {kart.passed_middle}",
    position=(-0.70, 0.20),
    scale=2,
    origin=(0, 0),
    background=True
)

has_crossed = False  # Prevent double counting per lap

lap_trigger = Entity(
    position=start_tile.position + Vec3(0, 0.1, 0),
    scale=(10, 0.2, 10),
    collider='box',
    visible=False
)

middle_trigger = Entity(
    position=middle_tile.position + Vec3(0, 0.1, 0),
    scale=(10, 0.2, 10),
    collider='box',
    visible=False
)


def update():
    global speed, lap_count, has_crossed
    coords.text = f"x: {kart.position.x:.2f}, z: {kart.position.z:.2f}" #remove later debug
    middle_text.text = f"Checkpoint: {kart.passed_middle}" #remove later debug
    forward_input = held_keys['w'] - held_keys['s']
    turn_input = held_keys['d'] - held_keys['a']

    if held_keys['space']:
        kart.y += 0.5


    # Speed control
    if forward_input:
        speed += acceleration * forward_input
    else:
        speed *= friction
    speed = clamp(speed, -max_speed, max_speed)
    

    # Turning
    if turn_input:
        kart.rotation_y += turn_speed * time.dt * turn_input

    # Forward movement
    rad = math.radians(kart.rotation_y)
    forward = Vec3(math.sin(rad), 0, math.cos(rad))
    move = forward * speed * time.dt
    kart.position += move

    # Gravity & Grounding
    ray = raycast(kart.position + Vec3(0, 0.5, 0), Vec3(0, -1, 0), distance=1, ignore=(kart,))
    if ray.hit:
        kart.vertical_speed = 0
        kart.y = ray.world_point.y + 0.25
    else:
        kart.vertical_speed -= kart.gravity * time.dt
        kart.y += kart.vertical_speed * time.dt

    # Fall reset if hits debug floor
    if kart.y < -19:
        kart.position = spawn_position
        kart.vertical_speed = 0
        speed = 0
        kart.passed_middle = False  # Reset checkpoint state

    # Lap counting
    global lap_count, has_crossed
    if lap_trigger.intersects(kart).hit:
        if not has_crossed and speed > 2 and kart.passed_middle:
            lap_count += 1
            lap_text.text = f"Lap {lap_count+1}"
            has_crossed = True
            kart.passed_middle = False  # Reset for next lap
    else:
        has_crossed = False


    # Middle checkpoint
    if middle_trigger.intersects(kart).hit:
        kart.passed_middle = True

    # 🎥 Camera
    cam_distance = 20
    cam_height = 7
    behind = Vec3(-math.sin(rad), 0, -math.cos(rad)) * cam_distance
    camera.position = kart.position + behind + Vec3(0, cam_height, 0)
    camera.rotation_x = 15
    camera.rotation_y = kart.rotation_y
    camera.rotation_z = 0

def on_game_start():
    print("Game started!")
    #kart.position = Vec3(0, 5, 5)

invoke(on_game_start, delay=1)

Sky()
app.run()


