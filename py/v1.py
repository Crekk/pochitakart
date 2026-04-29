from ursina import *
import math

app = Ursina()

window.title = 'Kart Clone'
window.borderless = False
window.fullscreen = False
window.fullscreen = False
window.fps_counter.enabled = True

# Ground
track = Entity(model='plane', scale=(50, 1, 50), color=color.gray, collider='box', texture='white_cube')
track.y = -0.01

# Walls
walls = []
def create_wall(x, z, scale_x, scale_z):
    wall = Entity(model='cube', color=color.dark_gray, collider='box',
                  position=(x, 1, z), scale=(scale_x, 2, scale_z))
    walls.append(wall)

create_wall(0, -25, 50, 1)
create_wall(0, 25, 50, 1)
create_wall(-25, 0, 1, 50)
create_wall(25, 0, 1, 50)

# Kart
kart = Entity(model='cube', color=color.azure, scale=(1, 0.5, 2), collider='box')
kart.position = (0, 0.25, 0)

# Movement
speed = 0
max_speed = 10
acceleration = 0.2
turn_speed = 90
friction = 0.94

def update():
    global speed

    # Input
    forward_input = held_keys['w'] - held_keys['s']
    turn_input = held_keys['d'] - held_keys['a']

    # Accelerate
    if forward_input:
        speed += acceleration * forward_input
    else:
        speed *= friction

    speed = clamp(speed, -max_speed, max_speed)

    # Turn
    if turn_input:
        kart.rotation_y += turn_speed * time.dt * turn_input

    # Move
    rad = math.radians(kart.rotation_y)
    forward = Vec3(math.sin(rad), 0, math.cos(rad))
    move = forward * speed * time.dt

    old_pos = kart.position
    kart.position += move

    for wall in walls:
        if kart.intersects(wall).hit:
            kart.position = old_pos
            speed *= -0.2
            break

    kart.y = 0.25

    # 🎥 Clean 3rd-person camera, manually rotated (no flipping)
    cam_distance = 16
    cam_height = 7

    rad = math.radians(kart.rotation_y)
    behind = Vec3(-math.sin(rad), 0, -math.cos(rad)) * cam_distance
    camera.position = kart.position + behind + Vec3(0, cam_height, 0)

    # Manually set rotation to look forward (no roll, no flip)
    camera.rotation_x = 15       # Tilt down slightly
    camera.rotation_y = kart.rotation_y
    camera.rotation_z = 0



Sky()
app.run()
