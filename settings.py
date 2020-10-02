import pygame as pg

pg.init()

vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
NIGHT_COLOR = (20, 20, 20)
BLUE = (0,0,255)

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "🧟‍R I S E  O F  T H E  Z O M B I E S🧟‍️"

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
GRASS_IMG = "grass.png"

WALL_IMG = 'log.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'player.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)

# Mob settings
MOB_IMG = 'zombie.png'
MOB_SPEED = 100
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
MOB_SPLAT = "splat green.png"
DETECT_RADIUS = 400

# Target
TARGET_IMG = "target.png"

# Spawner
SPAWNER_IMG = "tombstone.png"
SPAWNER_HP = 75
SPAWNER_TIME = 100

# Health Pack
HP_IMG = "health_pack.png"
NUM_HEAL = 50

LIGHT_MASK = "light_350_hard.png"

MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 350,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 30,
                     'bullet_size': 'lg',
                     'bullet_count': 1,
                     'sound': "colt_45-Justin-1313234082.wav"}

WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12,
                      'sound': "Winchester12-RA_The_Sun_God-1722751268.wav"}

WEAPONS['AR'] = {'bullet_speed': 400,
                 'bullet_lifetime': 500,
                 'rate': 50,
                 'kickback': 25,
                 'spread': 10,
                 'damage': 3,
                 'bullet_size': 'sm',
                 'bullet_count': 1,
                 'sound': "M4A1_Single-Kibblesbob-8540445.wav"}
BULLET_IMG = "bullet.png"
GUN_SPREAD = 5

HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 10
BOB_SPEED = 0.3
ZOMBIE_HIT_SOUND = 'bite.wav'
WEAPON_SOUNDS = {
    'pistol': ['pistol.wav'],
    'shotgun': ['shotgun.wav'],
    'AR' : ['AR.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav'}