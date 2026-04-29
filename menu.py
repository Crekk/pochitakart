from ursina import *
from ursina.prefabs.button import Button
import json
import subprocess
import os


app = Ursina()
window.title = "Pochita Kart"

selected_mode = None
selected_character = None
selected_track = None
state = 'main_menu'
background_music = Audio("/snd/menu.mp3", loop=True, autoplay=True, volume=0.5)

# --- UI Elements ---
main_menu_buttons = []
character_buttons = []
track_buttons = []
all_texts = []
character_models = []
back_buttons = []
default_unlocks = {
    "characters": [True, False, False, False, False]
}
button_selected = 0
key_held_last_frame = False

# Characters and tracks
characters = ['Pochita', 'Hatsune Miku', 'Ghost of Parasect', 'Big Chungus', 'Rat']
tracks = ['Pochita Circuit', 'Baby Gronk Park', 'Chungled Ruins', 'Hellscape Escape']

if not os.path.exists('unlock_status.json'):
    with open('unlock_status.json', 'w') as f:
        json.dump(default_unlocks, f)

BEST_TIMES_FILE = 'best_times.json'
try:
    with open(BEST_TIMES_FILE) as f:
        best_times = json.load(f)
except FileNotFoundError:
    best_times = {}


# ----- Functions -----
def higlight_selected_button(buttons):
    global button_selected
    for i, btn in enumerate(buttons):
        if i == button_selected:
            btn.color = color.azure
        else:
            btn.color = color.black

def go_to_character_select(mode):
    global state, selected_mode
    selected_mode = mode
    state = 'character_select'
    show_character_select()

def select_character(index):
    global selected_character, state
    selected_character = characters[index]
    state = 'track_select'
    show_track_select()

def select_track(index):
    global selected_track
    global state
    selected_track = index + 1

    # Save to file
    with open('savefile.json', 'w') as f:
        json.dump({
            'mode': selected_mode,
            'character': selected_character,
            'track': selected_track
        }, f)

    print(f"Launching race with mode={selected_mode}, character={selected_character}, track={selected_track}")
    # Always go back to main menu immediately before launching
    state = 'main_menu'
    show_main_menu()

    subprocess.Popen(['python', 'g5.py'])
    invoke(application.quit, delay=1)



def exit_game():
    application.quit()

def back_to_main_menu():
    global state
    state = 'main_menu'
    show_main_menu()

def back_to_character_select():
    global state
    state = 'character_select'
    show_character_select()

# ----- UI Display Functions -----
def show_main_menu():
    global button_selected
    button_selected = 0
    destroy_all_ui()
    destroy_all_models()

    # Add Pochita Kart logo at top
    all_texts.append(Entity(
        parent=camera.ui,
        model='quad',
        texture='img/logo.png',
        scale=(1.5, 0.4),
        y=0.35
    ))

    # Add a spinning Pochita model in the center
    pochita_display = Entity(
        model='mdl/pochita.obj',
        texture='mdl/pochita.png',
        scale=5,
        y=-2.4
    )
    character_models.append(pochita_display)

    def spin():
        pochita_display.rotation_y += 30 * time.dt

    pochita_display.update = spin

    # Layout: left to right instead of vertical
    positions = [-0.4, 0.0, 0.4]
    labels = ['Grand Prix', 'Time Trials', 'Exit']
    actions = [
        lambda: go_to_character_select('grand_prix'),
        lambda: go_to_character_select('time_trials'),
        exit_game
    ]

    for i in range(3):
        main_menu_buttons.append(Button(
            text=labels[i],
            scale=(.3, .1),
            x=positions[i],
            y=-0.4,
            on_click=actions[i]
        ))


# Add unlock flags (last character locked)

def show_character_select():
    global button_selected
    button_selected = 0
    destroy_all_ui()
    destroy_all_models()

    with open('unlock_status.json', 'r') as f:
        unlock_data = json.load(f)

    character_unlocked = unlock_data.get('characters', [True]*len(characters))

    camera.position = (0, 3, -25)
    camera.look_at((0,0,0))

    for i, name in enumerate(characters):
        x_pos = (i - 2) * 3

        if character_unlocked[i]:
            # Normal unlocked characters
            if name == 'Pochita':
                model = Entity(
                    model='mdl/pochita.obj',
                    texture='mdl/pochita.png',
                    scale=2,
                    x=x_pos,
                    y=-0.5
                )
            elif name == 'Hatsune Miku':
                model = Entity(
                    model='mdl/hatsune_miku.glb',
                    scale=0.8,
                    x=x_pos,
                    y=-0.5
                )
            elif name == 'Big Chungus':
                model = Entity(
                    model='mdl/big_chungus.glb',
                    scale=0.4,
                    x=x_pos,
                    y=0.5
                )
            elif name == 'Ghost of Parasect':
                model = Entity(
                    model='mdl/parasect.glb',
                    scale=0.03,
                    x=x_pos,
                    y=0
                )
            elif name == 'Rat':
                model = Entity(
                    model='cube',
                    texture='img/rat.jpg',
                    scale=(2, 2, 2),
                    x=x_pos,
                    y=0,
                    billboard=True
                )                  
            model.name = name
            character_models.append(model)

            # Add selection button only if unlocked!
            btn = Button(
                text=name,
                scale=(.2, .1),
                x=(i - 2) * .3,
                y=-0.2,
                on_click=lambda i=i: select_character(i)
            )
            character_buttons.append(btn)

            # Add stats image under the button
            stats_texture_name = None
            if name == 'Pochita':
                stats_texture_name = 'img/stats_pochita.png'
            elif name == 'Hatsune Miku':
                stats_texture_name = 'img/stats_miku.png'
            elif name == 'Ghost of Parasect':
                stats_texture_name = 'img/stats_parasect.png'
            elif name == 'Big Chungus':
                stats_texture_name = 'img/stats_big_chungus.png'
            elif name == 'Rat':
                stats_texture_name = 'img/stats_rat.png'

            if stats_texture_name:
                stats_image = Entity(
                    parent=camera.ui,
                    model='quad',
                    texture=stats_texture_name,
                    scale=(0.3, 0.13),
                    position=((i - 2) * .3, -0.35)
                )
                all_texts.append(stats_image)


        else:
            # Locked character: just show gray question mark model, no button
            model = Entity(
                model='cube',
                color=color.gray,
                scale=1.5,
                x=x_pos,
                y=0
            )
            model.name = "Secret"
            character_models.append(model)

    all_texts.append(Text(text='Select Your Character', y=0.4, scale=2, origin=(0,0)))




def show_track_select():
    global button_selected
    print("All best_times keys:", list(best_times.keys()))
    button_selected = 0
    destroy_all_ui()
    destroy_all_models()

    camera.position = (0, 3, -20)
    camera.look_at((0,0,0))

    all_texts.append(Text(text='Select Track', y=0.4, scale=2, origin=(0,0)))

    # For icons over tracks
    track_icons = [
        'img/pochita_circuit.png',
        'img/baby_gronk_park.png',
        'img/chungled_ruins.jpg',
        'img/hellscape_escape.jpg'
    ]

    prefix = 'g' if selected_mode == 'grand_prix' else 't'

    for i, track in enumerate(tracks):
        x_pos = (i - 1.5) * 3

        # Track "model"
        track_model = Entity(
            model='cube',
            color=color.dark_gray,
            scale=(2, 0.2, 2),
            x=x_pos,
            y=-0.5
        )
        character_models.append(track_model)

        # Icon
        if i < len(track_icons):
            icon = Entity(
                model='quad',
                texture=track_icons[i],
                scale=(2, 2),
                x=x_pos,
                y=1.5,
                billboard=True
            )
            character_models.append(icon)

        # Button
        btn = Button(
            text=track,
            scale=(.25, .1),
            x=(i - 1.5) * .35,
            y=-0.1,
            on_click=lambda i=i: select_track(i)
        )
        track_buttons.append(btn)

        # Add Best Time Text under button if available
        track_id = f"{prefix}{i+1}"
        record = best_times.get(track_id)
        print(f"Track ID: {track_id}, Record: {record}")
        if record:
            best_total = record.get("best_total_time")
            best_lap = record.get("best_lap_time")
            if best_total is not None or best_lap is not None:
                time_text = "Best Times:"
                if best_total is not None:
                    time_text += f"\nTotal: {best_total:.2f}s"
                if best_lap is not None:
                    time_text += f"\nLap: {best_lap:.2f}s"
                all_texts.append(Text(
                    parent=camera.ui,
                    text=time_text,
                    x=(i - 1.5) * .35,
                    y=-0.25,
                    scale=1,
                    origin=(0,0)
                ))




# Utility
def destroy_all_ui():
    for b in main_menu_buttons + character_buttons + track_buttons + back_buttons:
        destroy(b)
    for t in all_texts:
        destroy(t)

    main_menu_buttons.clear()
    character_buttons.clear()
    track_buttons.clear()
    back_buttons.clear()
    all_texts.clear()

def destroy_all_models():
    for e in character_models:
        destroy(e)
    character_models.clear()

def update():
    global state, button_selected, key_held_last_frame
    
    if state == 'main_menu':
        higlight_selected_button(main_menu_buttons)
        if held_keys['left arrow'] or held_keys['a'] or held_keys['gamepad left stick x'] < -0.5:
            if key_held_last_frame:
                return
            key_held_last_frame = True
            button_selected = (button_selected - 1) % len(main_menu_buttons)
            higlight_selected_button(main_menu_buttons)
        if held_keys['right arrow'] or held_keys['d'] or held_keys['gamepad left stick x'] > 0.5:
            if key_held_last_frame:
                return
            key_held_last_frame = True
            button_selected = (button_selected + 1) % len(main_menu_buttons)
            higlight_selected_button(main_menu_buttons)
        if held_keys['enter'] or held_keys['return'] or held_keys['gamepad a']:
            if key_held_last_frame:
                return
            key_held_last_frame = True
            main_menu_buttons[button_selected].on_click()
    
    if state == 'character_select':
        for m in character_models:
            m.rotation_y += 20 * time.dt
        higlight_selected_button(character_buttons)
        if held_keys['left arrow'] or held_keys['a'] or held_keys['gamepad left stick x'] < -0.5:
            if key_held_last_frame:
                return
            key_held_last_frame = True
            button_selected = (button_selected - 1) % len(character_buttons)
            higlight_selected_button(character_buttons)
        if held_keys['right arrow'] or held_keys['d'] or held_keys['gamepad left stick x'] > 0.5:
            if key_held_last_frame:
                return
            key_held_last_frame = True
            button_selected = (button_selected + 1) % len(character_buttons)
            higlight_selected_button(character_buttons)   
        if held_keys['enter'] or held_keys['return'] or held_keys['gamepad a']:
            if key_held_last_frame:
                return
            key_held_last_frame = True
            if button_selected < len(character_buttons):
                character_buttons[button_selected].on_click()

    if state == 'track_select':
        higlight_selected_button(track_buttons)
        if held_keys['left arrow'] or held_keys['a'] or held_keys['gamepad left stick x'] < -0.5:
            if key_held_last_frame:
                return
            key_held_last_frame = True
            button_selected = (button_selected - 1) % len(track_buttons)
            higlight_selected_button(track_buttons)
        if held_keys['right arrow'] or held_keys['d'] or held_keys['gamepad left stick x'] > 0.5:
            if key_held_last_frame:
                return
            key_held_last_frame = True
            button_selected = (button_selected + 1) % len(track_buttons)
            higlight_selected_button(track_buttons)   
        if held_keys['enter'] or held_keys['return'] or held_keys['gamepad a']:
            if key_held_last_frame:
                return
            key_held_last_frame = True
            if button_selected < len(track_buttons):
                track_buttons[button_selected].on_click()

    # UNIVERSAL BACK HANDLER
    if (held_keys['escape'] or held_keys['gamepad b']) and not key_held_last_frame:
        key_held_last_frame = True
        if state == 'character_select':
            back_to_main_menu()
        elif state == 'track_select':
            back_to_character_select()

    if not (
        held_keys['left arrow'] or held_keys['right arrow'] or 
        held_keys['a'] or held_keys['d'] or 
        held_keys['gamepad left stick x'] or
        held_keys['enter'] or held_keys['return'] or held_keys['gamepad a'] or 
        held_keys['escape'] or held_keys['gamepad b']
    ):
        key_held_last_frame = False


# --- Start on main menu ---
show_main_menu()

app.run()
