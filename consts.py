import math
import collections

CreepsConsts = collections.namedtuple(
    'CreepsConsts', 'health, speed, reward')
TowersConsts = collections.namedtuple(
    'TowersConsts', 'damage, range, speed, price')
Point = collections.namedtuple('Point', 'row, col')


UNITS = {'creeps': {'Peon': CreepsConsts(50, 20, 10),
                    'Grunt': CreepsConsts(100, 15, 15),
                    'Raider': CreepsConsts(80, 25, 20)},
         'towers': {'ArcaneTower': TowersConsts(15, 3, 5, 10),
                    'GuardTower': TowersConsts(25, 2, 5, 15),
                    'CanonTower': TowersConsts(35, 1.5, 3, 20)}}

MAX_HEALTH = {'Peon': 50,
              'Grunt': 100,
              'Raider': 80}

TITLE = 'Tower Defense'
START_GOLD = 100
ENEMIES_ALLOWED = 5
PORTAL = Point(10, 0)
CASTLE = Point(10, 39)

DEFAULT_MAP = ['GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG',
               'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG',
               'GGGGGGGGG       GGGGGGGGGGGGGGGGGGGGGGGG',
               'GGGGGGGGG GGGGG GGGG      GGGGGGGGGGGGGG',
               'GGGGGGGGG GGGGG GGGG GGGG GGG     GGGGGG',
               'GGGGGGGGG GGGGG GGGG GGGG GGG GGG GGGGGG',
               'GGGGGGGGG GGGGG GGGG GGGG GGG GGG GGGGGG',
               'GGGGGGGGG GGGGG GGGG GGGG GGG GGG GGGGGG',
               'GGGGGGGGG GGGGG GGGG GGGG GGG GGG GGGGGG',
               'GGGGGGGGG GGGGG GGGG GGGG GGG GGG GGGGGG',
               'P   GGGGG GGGGG GGGG GGGG GGG GGG GG   C',
               'GGG GGGGG GGGGG GGGG GGGG GGG GGG GG GGG',
               'GGG GGGGG GGGGG GGGG GGGG GGG GGG GG GGG',
               'GGG GGGGG GGGGG GGGG GGGG GGG GGG GG GGG',
               'GGG GGGGG GGGGG GGGG GGGG GGG GGG GG GGG',
               'GGG GGGGG GGGGG GGGG GGGG GGG GGG    GGG',
               'GGG GGGGG GGGGG GGGG GGGG     GGGGGGGGGG',
               'GGG GGGGG GGGGG      GGGGGGGGGGGGGGGGGGG',
               'GGG       GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG',
               'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG',
               'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG']

TOWERS_NAMES = ['ArcaneTower', 'CanonTower', 'GuardTower']
MAGIC_NAMES = ['LightningMagic', 'SwordMagic']
CONTROL_NAMES = ['Reset', 'Play', 'Pause', 'Slower', 'Faster', 'Restart']

LABEL_NAMES = ['Gold', 'Enemies']

TEXTURES_FOLDER = 'Field'
ICON_PATH = '{}/Icon.png'.format(TEXTURES_FOLDER)
LOGO_PATH = '{}/Logo.png'.format(TEXTURES_FOLDER)
CURSOR_PATH = '{}/Cursor.png'.format(TEXTURES_FOLDER)
BORDER_PATH = '{}/Border.png'.format(TEXTURES_FOLDER)

PROCESS_NAME = 'python tower_defense.py'

UVS = [1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0]
INDICES = [0, 1, 2, 1, 2, 3]

REDRAW_TIME = math.ceil(1000 / 60)
SPAWN_WAVE_TIME = 30000
SPAWN_CREEP_TIME = 15000
MOVE_CREEP_TIME = 5000
TOWER_ATTACK_TIME = 5000
ATTACK_DELETE_TIME = 200
