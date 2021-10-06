import pygame as py
import random

vec = py.math.Vector2
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106,55,5)

# game settings
WIDTH = 1376  # or 1,376
HEIGHT = 100 * 9 # or 900
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
# player settings
PLAYER_HEALTH = 100
PLAYER_HIT_RECT = py.Rect(0, 0, 64, 64)
PLAYER_ENERY = 100
PLAYERSPEED = 200
PLAYER_ROT_SPEED = 180
PLAYER_IMG = 'survivor1_gun.png'
# Effects
ALPHA_DAMAGE = [i for i in range(0,255,35)]
NIGHT_COLOR = (25,25,25)
LIGHT_RADIUS = (600,600)
LIGHT_MASK = 'light_350_med.png'
MUZZLE_FLASHES = ['whitePuff15.png','whitePuff16.png','whitePuff17.png','whitePuff18.png']
# bullet settings
BULLET_IMG = 'bullet_tile.png'
WEOPENS = {}
WEOPENS['pistol'] = {'bullet_speed' : 500,
                     'bullet_lifetime' : 1000,
                     'rate' : 250,
                     'kickback' : 200,
                     'damage' : 20,
                     'spread' : 5,
                     'bullet_size' : 'lg',
                     'bullet_count' : 1
                     }

WEOPENS['shotgun'] = {'bullet_speed' : 500,
                     'bullet_lifetime' : 2000,
                     'rate' : 900,
                     'kickback' : 300,
                     'damage' : 50,
                     'spread' : 20,
                     'bullet_size' : 'sm',
                     'bullet_count' : 2
                     }


BULLET_OFFSET = vec(30 , 10)

# mob settings
ZOMBIE_IMG = 'zoimbie1_hold.png'
ZOMBIE_SPEED = [100,132,98,110,160]
MOB_HIT_RECT = py.Rect(0,0,35,43)
MOB_KNOCKBACK = 40
AVOID_RADIUS = 80

# bobbing motion settings
BOB_RANGE = 20
BOB_SPEED = 0.6

# hope you like it