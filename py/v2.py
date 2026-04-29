from ursina import *
import math

app = Ursina()
window.title = 'Pochita Kart'
window.fps_counter.enabled = True

# ----- Track Tile Function -----
def add_track_tile(x, z, rotation=0):
    return Entity(
        model='cube',
        color=color.gray,
        position=(x, 0, z),
        scale=(4, 0.1, 6),
        rotation_y=rotation,
        collider='box'
    )

# ----- Manual Track Layout -----
add_track_tile(0, 0)
add_track_tile(0, 6)
add_track_tile(0, 12)
add_track_tile(4, 12, 90)
add_track_tile(8, 12, 90)
add_track_tile(8, 6, 135)
add_track_tile(6, 4, 180)
add_track_tile(2, 4, 180)
add_track_tile(0, 4, 225)
add_track_tile(-2, 6, 270)
add_track_tile(-2, 12, 270)
add_track_tile(0, 14, 315)

# ----- Debug Floor -----
debug_floor = Entity(model='plane', scale=100, y=-20, color=color.black33, collider='box')

# ----- Kart -----
kart = Entity(model='cube', color=color.azure, scale=(1, 0.5, 2), collider='box')
kart.position = Vec3(0, 5, 0)
kart.gravity = 9
kart.vertical_speed = 0

# ----- Movement Vars -----
speed = 0
max_speed = 10
acceleration = 0.2
turn_speed = 90
friction = 0.95

def update():
    global speed

    forward_input = held_keys['w'] - held_keys['s']
    turn_input = held_keys['d'] - held_keys['a']

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
        kart.position = Vec3(0, 5, 0)
        kart.vertical_speed = 0
        speed = 0

    # 🎥 Camera
    cam_distance = 16
    cam_height = 7
    behind = Vec3(-math.sin(rad), 0, -math.cos(rad)) * cam_distance
    camera.position = kart.position + behind + Vec3(0, cam_height, 0)
    camera.rotation_x = 15
    camera.rotation_y = kart.rotation_y
    camera.rotation_z = 0

Sky()
app.run()
