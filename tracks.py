# tracks.py
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

class Track():
    def __init__(self, ai_waypoints, item_box_positions, skybox_texture, tile_texture, ost):
        self.ai_waypoints = ai_waypoints if ai_waypoints else []
        self.item_box_positions = item_box_positions if item_box_positions else []
        self.skybox_texture = skybox_texture
        self.tile_texture = tile_texture
        self.ost = ost

# ----- Track 1: Pochita Circuit -----
track1 = Track(
    #first 2 unchanged for now change later pleaseee
    ai_waypoints = [
    Vec3(0, 0, 100),
    Vec3(70, 0, 188),
    Vec3(177, 0, 200),
    Vec3(250, 0, 276),
    Vec3(253, 0, 366),
    Vec3(150, 0, 287),
    Vec3(-40, 0, 274),
    Vec3(-50, 0, -90),
    Vec3(-5, 0, -90),
    Vec3(0, 0, 0)],

    item_box_positions = [
        Vec3(0, 1, 103),
        Vec3(-5, 1, 103),
        Vec3(5, 1, 103),

        Vec3(108, 1, 200),
        Vec3(108, 1, 205),
        Vec3(108, 1, 195),
        Vec3(108, 1, 190),
        Vec3(108, 1, 210),

        Vec3(115, 1, 280),
        Vec3(115, 1, 285),
        Vec3(115, 1, 275),
        Vec3(115, 1, 270),
        Vec3(115, 1, 290),

        Vec3(-25, 1, -100),
        Vec3(-25, 1, -105),
        Vec3(-25, 1, -95),
        Vec3(-25, 1, -90),
        Vec3(-25, 1, -110),


    ],
    skybox_texture= 'img/skybox1.jpg',
    tile_texture = 'img/road1.jpg',
    ost = 'snd/ost1.mp3'
)
# def add_track_tile(x, z, rotation=0, vrotation=0, y=0, x_size=10, z_size=10):
def create_track1(add_track_tile,walls_list,add_big_tile):
    global start_tile, middle_tile

    start_tile = add_big_tile(0, 0, 0, 0, 0)
    start_tile.color = color.green  

    middle_tile = add_big_tile(50,280, 0, 0, 0.1) #change pos later
    middle_tile.color = color.azure

    # Move forward along Z

    add_big_tile(x=0, z=-25, rotation=0, vrotation=0, y=0)
    add_big_tile(x=0, z=-50, rotation=0, vrotation=0, y=0)
    add_big_tile(x=0, z=-75, rotation=0, vrotation=0, y=0)
    add_big_tile(x=0, z=-100, rotation=0, vrotation=0, y=0)

    add_big_tile(x=0, z=25, rotation=0, vrotation=0, y=0)
    add_big_tile(x=0, z=50, rotation=0, vrotation=0, y=0)
    add_big_tile(x=0, z=75, rotation=0, vrotation=0, y=0)
    add_big_tile(x=0, z=100, rotation=0, vrotation=0, y=0)

    for i in range(0, 5, 1):
        add_big_tile(x=17*i, z=120+17*i, rotation=45, vrotation=0, y=0)

    for i in range(0, 5, 1):
        add_big_tile(x=75+25*i, z=200, rotation=0, vrotation=0, y=0)

    for i in range(0, 5, 1):
        add_big_tile(x=185+17*i, z=200+17*i, rotation=45, vrotation=0, y=0)

    for i in range(0, 5, 1):
        add_big_tile(x=260, z=275+25*i, rotation=0, vrotation=0, y=0)

    for i in range(0, 7, 1):
        add_big_tile(x=260-17*i, z=390-17*i, rotation=45, vrotation=0, y=0)
    
    for i in range(0, 9, 1):
        add_big_tile(x=150-25*i, z=280, rotation=0, vrotation=0, y=0)

    for i in range(0, 16, 1):
        add_big_tile(x=-50, z=280-25*i, rotation=0, vrotation=0, y=0)

    for i in range(1, 6, 1):
        add_big_tile(x=-50, z=250-50*i, rotation=0, vrotation=8*i, y=2)

    add_big_tile(x=-25, z=-100, rotation=0, vrotation=0, y=0)

    return start_tile, middle_tile

# ----- Track 2: Baby Gronk Park -----
track2 = Track(
    #first 2 unchanged for now change later pleaseee
    ai_waypoints = [
        Vec3(0, 20.3, 140),
        Vec3(28, 20.3, 172),
        Vec3(100, 20.3, 173),
        Vec3(130, 20.3, 145),
        Vec3(130, 20.3, -130),
        Vec3(17, 58.9, -135),
        Vec3(15, 72, -100),
        Vec3(0, 0, -0)],

    item_box_positions = [
        Vec3(0, 21.5, 110),
        Vec3(0, 21.5, 120),
        Vec3(0, 21.5, 130),

        Vec3(-3, 21.5, 110),
        Vec3(-3, 21.5, 120),
        Vec3(-3, 21.5, 130),

        Vec3(3, 21.5, 110),
        Vec3(3, 21.5, 120),
        Vec3(3, 21.5, 130),

        Vec3(60, 21.5, 175),
        Vec3(60, 21.5, 173),
        Vec3(60, 21.5, 177),

        Vec3(130, 4.5, -15),
        Vec3(130, 4.5, -25),
        Vec3(130, 4.5, -35),
        Vec3(130, 4.5, -45),
        Vec3(130, 4.5, -55),
        Vec3(130, 4.5, -65),
        Vec3(130, 4.5, -75),
        Vec3(130, 4.5, -85),
        Vec3(130, 4.5, -95),
        Vec3(130, 4.5, -105),
        Vec3(130, 4.5, -115),
        Vec3(130, 4.5, -125),

        Vec3(14.7, 73.5, -103.5),

    ],
    skybox_texture= 'img/skybox2.jpg',
    tile_texture = 'img/road2.png',
    ost = 'snd/ost2.mp3'
)
# def add_track_tile(x, z, rotation=0, vrotation=0, y=0, x_size=10, z_size=10):
def create_track2(add_track_tile,walls_list):
    global start_tile, middle_tile

    start_tile = add_track_tile(0, 120, 0, 0, 20.4)
    start_tile.color = color.green  

    middle_tile = add_track_tile(40,-134, 0, 0, 52.31) #change pos later
    middle_tile.color = color.azure

    for z in range(-50, 60, 10):
        add_track_tile(0, z)

    add_track_tile(0, 70, 180, 30, 10, 10, 40)

    for z in range(95, 145, 10):
        add_track_tile(0, z, 0, 0, 20)

    for i in range(0, 30, 7):
        add_track_tile(i, 145 + i, 45, 0, 20)

    for x in range(30,100,10):
        add_track_tile(x, 175, 0, 0, 20)

    for i in range(0, 30, 7):
        add_track_tile(100 + i, 175 - i, 135, 0, 20)

    for z in range(145, 95, -10):
        add_track_tile(130, z, 180, 0, 20)

    add_track_tile(130, 85, 0, -10, 17.5, 10, 40)
    add_track_tile(130, 65, 0, -10, 14, 10, 40)
    add_track_tile(130, 45, 0, -10, 10.5, 10, 40)
    add_track_tile(130, 25, 0, -10, 7, 10, 40)

    for i in range(5,-135,-10):
        add_track_tile(x=130, z=i, rotation=0, vrotation=0, y=3.5)

    for i in range(130, 100, -10):
        add_track_tile(x=i, z=-135, rotation=0, vrotation=0, y=3.5)

    for i in range(0, 49, 7):
        add_track_tile(x=100-i,z=-135,rotation=90,vrotation=45,y=6.5+i)
    
    add_track_tile(x=50, z=-135, rotation=0, vrotation=0, y=52)
    add_track_tile(x=40, z=-135, rotation=0, vrotation=0, y=52)
    add_track_tile(x=30, z=-135, rotation=0, vrotation=0, y=52)

    add_track_tile(x=23, z=-135, rotation=90, vrotation=45, y=55)
    add_track_tile(x=15, z=-135, rotation=90, vrotation=0, y=58.5)
    add_track_tile(x=15, z=-128, rotation=0, vrotation=-45, y=62.0)
    add_track_tile(x=15, z=-120, rotation=0, vrotation=0, y=65.5)
    add_track_tile(x=15, z=-112, rotation=0, vrotation=-45, y=69.0)
    add_track_tile(x=15, z=-104, rotation=0, vrotation=0, y=72.5)



    return start_tile, middle_tile

# ----- Track 3: Chungled Ruins -----
track3 = Track(
    #first 2 unchanged for now change later pleaseee
    ai_waypoints = [
        Vec3(0, 6, 514),
        Vec3(40, 19, 518),
        Vec3(43, 31, 480),
        Vec3(0, 44, 480),
        Vec3(0, 56, 520), 
        Vec3(40, 69, 520),
        Vec3(40, 80, 470),
        Vec3(0, 93, 480),
        Vec3(0, 105, 520),
        Vec3(40, 118, 520),
        Vec3(40, 131, 480),
        Vec3(0, 144, 480),
        Vec3(0, 156, 520),
        Vec3(40, 169, 520),
        Vec3(40, 182, 480),
        Vec3(0, 195, 480),

        Vec3(85, 0, 300),
        Vec3(300, 0, 300),

        Vec3(300, 0, 480),
        Vec3(300, 0, 670),

        Vec3(0, 0, 700),
        Vec3(-200, 0, 700),

        Vec3(0, 0, 0)
        ],

    item_box_positions = [
        Vec3(-480, 1, -80),
        Vec3(-420, 1, 150),
        Vec3(-400, 1, 620),
        Vec3(-350, 1, 240),
        Vec3(-300, 1, 850),
        Vec3(-250, 1, 10),
        Vec3(-200, 1, 400),
        Vec3(-150, 1, 700),
        Vec3(-100, 1, 300),
        Vec3(-60,  1, 120),
        Vec3(-30,  1, 780),
        Vec3(0,    1, 500),
        Vec3(30,   1, 160),
        Vec3(60,   1, 840),
        Vec3(100,  1, 200),
        Vec3(150,  1, 730),
        Vec3(200,  1, 420),
        Vec3(250,  1, -50),
        Vec3(300,  1, 600),
        Vec3(350,  1, 320),
        Vec3(400,  1, 90),
        Vec3(450,  1, 770),
        Vec3(490,  1, 240),
        Vec3(-470, 1, 500),
        Vec3(-370, 1, 660),
        Vec3(-270, 1, 100),
        Vec3(-170, 1, 570),
        Vec3(-70,  1, 360),
        Vec3(70,   1, 690),
        Vec3(170,  1, 30),
        Vec3(270,  1, 480),
        Vec3(370,  1, 810),
        Vec3(470,  1, -30),
        Vec3(400,  1, 500),
        Vec3(0,    1, 0),
        Vec3(0,    1, 900),
    ],
    
    skybox_texture= 'img/skybox3.jpg',
    tile_texture = 'img/road3.jpg',
    ost = 'snd/ost3.flac'
)
# def add_track_tile(x, z, rotation=0, vrotation=0, y=0, x_size=10, z_size=10):
def create_track3(add_track_tile,walls_list, add_big_tile):
    global start_tile, middle_tile

    start_tile = add_big_tile(0, 0, 0, 0, 0.1)
    start_tile.color = color.green  

    middle_tile = add_big_tile(0, 480, 0, 0, 194.1) #change pos later
    middle_tile.color = color.azure

    add_track_tile(x=0, z=400, rotation=0, vrotation=0, y=0, x_size=1000, z_size=1000)

    add_big_tile(x=0, z=100, rotation=0, vrotation=-30, y=0)
    add_big_tile(x=0, z=100+21, rotation=0, vrotation=-30, y=12.5)
    add_big_tile(x=0, z=100+2*21, rotation=0, vrotation=-30, y=2*12.5)
    # Flat Bridge (optional - add 1 or more tiles flat at the top)
    add_big_tile(x=0, z=100+3*21,  rotation=0, vrotation=0,    y=2.5*12.5)
    add_big_tile(x=0, z=100+4*21,  rotation=0, vrotation=0,    y=2.5*12.5)
    add_big_tile(x=0, z=100+5*21,  rotation=0, vrotation=0,    y=2.5*12.5)
    add_big_tile(x=0, z=100+6*21,  rotation=0, vrotation=0,    y=2.5*12.5)

    # Ramp Down (mirrored from ramp up)
    add_big_tile(x=0, z=100+7*21,  rotation=0, vrotation=30,   y=2*12.5)
    add_big_tile(x=0, z=100+8*21,  rotation=0, vrotation=30,   y=12.5)
    add_big_tile(x=0, z=100+9*21,  rotation=0, vrotation=30,   y=0)

    # bridge2
    add_big_tile(x=-400, z=200, rotation=90, vrotation=-30, y=0)
    add_big_tile(x=-400+21, z=200, rotation=90, vrotation=-30, y=12.5)
    add_big_tile(x=-400+2*21, z=200, rotation=90, vrotation=-30, y=2*12.5)
    add_big_tile(x=-400+3*21, z=200, rotation=90, vrotation=0, y=2.5*12.5)
    add_big_tile(x=-400+4*21, z=200, rotation=90, vrotation=0, y=2.5*12.5)
    add_big_tile(x=-400+5*21, z=200, rotation=90, vrotation=0, y=2.5*12.5)
    add_big_tile(x=-400+6*21, z=200, rotation=90, vrotation=0, y=2.5*12.5)
    add_big_tile(x=-400+7*21, z=200, rotation=90, vrotation=30, y=2*12.5)
    add_big_tile(x=-400+8*21, z=200, rotation=90, vrotation=30, y=12.5)
    add_big_tile(x=-400+9*21, z=200, rotation=90, vrotation=30, y=0)

    #bridge 3
    add_big_tile(x=300, z=500, rotation=0, vrotation=-30, y=0)
    add_big_tile(x=300, z=500+21, rotation=0, vrotation=-30, y=12.5)
    add_big_tile(x=300, z=500+2*21, rotation=0, vrotation=-30, y=2*12.5)
    add_big_tile(x=300, z=500+3*21, rotation=0, vrotation=0, y=2.5*12.5)
    add_big_tile(x=300, z=500+4*21, rotation=0, vrotation=0, y=2.5*12.5)
    add_big_tile(x=300, z=500+5*21, rotation=0, vrotation=0, y=2.5*12.5)
    add_big_tile(x=300, z=500+6*21, rotation=0, vrotation=0, y=2.5*12.5)
    add_big_tile(x=300, z=500+7*21, rotation=0, vrotation=30, y=2*12.5)
    add_big_tile(x=300, z=500+8*21, rotation=0, vrotation=30, y=12.5)
    add_big_tile(x=300, z=500+9*21, rotation=0, vrotation=30, y=0)

    add_big_tile(x=-200, z=700, rotation=90, vrotation=-30, y=0)
    add_big_tile(x=-200+21, z=700, rotation=90, vrotation=-30, y=12.5)
    add_big_tile(x=-200+2*21, z=700, rotation=90, vrotation=-30, y=2*12.5)
    add_big_tile(x=-200+3*21, z=700, rotation=90, vrotation=0, y=2.5*12.5)
    add_big_tile(x=-200+4*21, z=700, rotation=90, vrotation=0, y=2.5*12.5)
    add_big_tile(x=-200+5*21, z=700, rotation=90, vrotation=0, y=2.5*12.5)
    add_big_tile(x=-200+6*21, z=700, rotation=90, vrotation=0, y=2.5*12.5)
    add_big_tile(x=-200+7*21, z=700, rotation=90, vrotation=30, y=2*12.5)
    add_big_tile(x=-200+8*21, z=700, rotation=90, vrotation=30, y=12.5)
    add_big_tile(x=-200+9*21, z=700, rotation=90, vrotation=30, y=0)

    add_big_tile(x=-300, z=0, rotation=0, vrotation=-30, y=0)
    add_big_tile(x=-300, z=0+21, rotation=0, vrotation=-30, y=12.5)
    add_big_tile(x=-300, z=0+2*21, rotation=0, vrotation=-30, y=2*12.5)
    add_big_tile(x=-300, z=0+3*21, rotation=0, vrotation=0, y=2.5*12.5)
    add_big_tile(x=-300, z=0+4*21, rotation=0, vrotation=0, y=2.5*12.5)
    add_big_tile(x=-300, z=0+5*21, rotation=0, vrotation=0, y=2.5*12.5)
    add_big_tile(x=-300, z=0+6*21, rotation=0, vrotation=0, y=2.5*12.5)
    add_big_tile(x=-300, z=0+7*21, rotation=0, vrotation=30, y=2*12.5)
    add_big_tile(x=-300, z=0+8*21, rotation=0, vrotation=30, y=12.5)
    add_big_tile(x=-300, z=0+9*21, rotation=0, vrotation=30, y=0)

    add_big_tile(x=100, z=300, rotation=90, vrotation=-30, y=0)
    add_big_tile(x=100+21, z=300, rotation=90, vrotation=-30, y=12.5)
    add_big_tile(x=100+2*21, z=300, rotation=90, vrotation=-30, y=2*12.5)
    add_big_tile(x=100+3*21, z=300, rotation=90, vrotation=0, y=2.5*12.5)
    add_big_tile(x=100+4*21, z=300, rotation=90, vrotation=0, y=2.5*12.5)
    add_big_tile(x=100+5*21, z=300, rotation=90, vrotation=0, y=2.5*12.5)
    add_big_tile(x=100+6*21, z=300, rotation=90, vrotation=0, y=2.5*12.5)
    add_big_tile(x=100+7*21, z=300, rotation=90, vrotation=30, y=2*12.5)
    add_big_tile(x=100+8*21, z=300, rotation=90, vrotation=30, y=12.5)
    add_big_tile(x=100+9*21, z=300, rotation=90, vrotation=30, y=0)

    # Step 0
    add_big_tile(x=0, z=500, rotation=0, vrotation=-30, y=0)
    add_big_tile(x=0, z=521, rotation=0, vrotation=0, y=6.25)

    # Step 1
    add_big_tile(x=21, z=521, rotation=90, vrotation=-30, y=12.5)
    add_big_tile(x=42, z=521, rotation=90, vrotation=0, y=18.75)

    # Step 2
    add_big_tile(x=42, z=500, rotation=180, vrotation=-30, y=25.0)
    add_big_tile(x=42, z=479, rotation=180, vrotation=0, y=31.25)

    # Step 3
    add_big_tile(x=21, z=479, rotation=270, vrotation=-30, y=37.5)
    add_big_tile(x=0, z=479, rotation=270, vrotation=0, y=43.75)

    # Step 4
    add_big_tile(x=0, z=500, rotation=0, vrotation=-30, y=50.0)
    add_big_tile(x=0, z=521, rotation=0, vrotation=0, y=56.25)

    # Step 5
    add_big_tile(x=21, z=521, rotation=90, vrotation=-30, y=62.5)
    add_big_tile(x=42, z=521, rotation=90, vrotation=0, y=68.75)

    # Step 6
    add_big_tile(x=42, z=500, rotation=180, vrotation=-30, y=75.0)
    add_big_tile(x=42, z=479, rotation=180, vrotation=0, y=81.25)

    # Step 7
    add_big_tile(x=21, z=479, rotation=270, vrotation=-30, y=87.5)
    add_big_tile(x=0, z=479, rotation=270, vrotation=0, y=93.75)

    # Step 8
    add_big_tile(x=0, z=500, rotation=0, vrotation=-30, y=100.0)
    add_big_tile(x=0, z=521, rotation=0, vrotation=0, y=106.25)

    # Step 9
    add_big_tile(x=21, z=521, rotation=90, vrotation=-30, y=112.5)
    add_big_tile(x=42, z=521, rotation=90, vrotation=0, y=118.75)

    # Step 10
    add_big_tile(x=42, z=500, rotation=180, vrotation=-30, y=125.0)
    add_big_tile(x=42, z=479, rotation=180, vrotation=0, y=131.25)

    # Step 11
    add_big_tile(x=21, z=479, rotation=270, vrotation=-30, y=137.5)
    add_big_tile(x=0, z=479, rotation=270, vrotation=0, y=143.75)

    # Step 12
    add_big_tile(x=0, z=500, rotation=0, vrotation=-30, y=150.0)
    add_big_tile(x=0, z=521, rotation=0, vrotation=0, y=156.25)

    # Step 13
    add_big_tile(x=21, z=521, rotation=90, vrotation=-30, y=162.5)
    add_big_tile(x=42, z=521, rotation=90, vrotation=0, y=168.75)

    # Step 14
    add_big_tile(x=42, z=500, rotation=180, vrotation=-30, y=175.0)
    add_big_tile(x=42, z=479, rotation=180, vrotation=0, y=181.25)

    # Step 15
    add_big_tile(x=21, z=479, rotation=270, vrotation=-30, y=187.5)
    add_big_tile(x=0, z=479, rotation=270, vrotation=0, y=193.75)


    return start_tile, middle_tile

# ----- Track 4: Hellscape Escape -----  
track4 = Track(
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
    ],
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
    ],
    skybox_texture= 'img/skybox4.jpg',
    tile_texture = 'img/road4.jpg',
    ost = 'snd/ost4.mp3'
)
def create_track4(add_track_tile,walls_list):
    global start_tile, middle_tile
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

    for i in range(0, 50, 10):
        add_track_tile(100 - i, 275, 270, -15, i * 0.2)

    for x in range(50, 0, -10):
        add_track_tile(x, 275, 270, 0, 1)

    for i in range(0, 50, 10):
        add_track_tile(0, 275 - i, 0, 45, 1 + i * 0.2)

    for z in range(225, 175, -10):
        add_track_tile(0, z, 0, 0, 2)

    for x in range(0, -50, -10):
        add_track_tile(x, 185, 270, 0, 2)

    for i in range(0, 50, 10):
        add_track_tile(-40, 185 - i, 0, 10, 2 + i * 0.2)

    for z in range(135, 85, -10):
        add_track_tile(-40, z, 0, 0, 3)

    for i in range(0, 15, 5):
        add_track_tile(-40 + i, 95 - i, 45, 0, 3)

    for i in range(0, 30, 5):
        add_track_tile(-40 + i, 85 - i, 45, 0, 3)

    for i in range(0, 30, 5):
        add_track_tile(-10 - i, 55 - i, 315, 0, 3)

    for i in range(0, 10, 5):
        add_track_tile(-40 + i, 25 - i, 45, 0, 3)

    for i in range(0, 20, 5):
        add_track_tile(-30 - i, 15 - i, 315, 0, 3)

    for i in range(0, 20, 5):
        add_track_tile(-50 + i, -5 - i, 45, 0, 3)

    for x in range(-30, -70, -10):
        add_track_tile(x, -25, 270, 0, 3)

    for z in range(-25, -75, -10):
        add_track_tile(-70, z, 0, 0, 3)

    for x in range(-60, 10, 10):
        add_track_tile(x, -65, 90, 0, 3)

    for z in range(-65, -15, 10):
        add_track_tile(0, z, 0, 0, 3)

    walls_list.append(Entity(
        model='cube',
        color=color.dark_gray,
        position=(-13.5, 4, 44.5),
        scale=(0.5, 2, 30),
        rotation_y=45,
        collider='box'
    ))
    walls_list.append(Entity(
        model='cube',
        color=color.dark_gray,
        position=(-12.5, 4, 64.5),
        scale=(30, 2, 0.5),
        rotation_y=45,
        collider='box'
    ))

    return start_tile, middle_tile