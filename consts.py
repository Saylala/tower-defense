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
                    'CanonTower': TowersConsts(35, 1, 3, 20)}}

MAX_HEALTH = {'Peon': 50,
              'Grunt': 100,
              'Raider': 80}

START_GOLD = 100
ENEMIES_ALLOWED = 5
PORTAL = Point(10, 0)
CASTLE = Point(10, 39)

DEFAULT_MAP = ["GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
               "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
               "GGGGGGGGG       GGGGGGGGGGGGGGGGGGGGGGGG",
               "GGGGGGGGG GGGGG GGGG      GGGGGGGGGGGGGG",
               "GGGGGGGGG GGGGG GGGG GGGG GGG     GGGGGG",
               "GGGGGGGGG GGGGG GGGG GGGG GGG GGG GGGGGG",
               "GGGGGGGGG GGGGG GGGG GGGG GGG GGG GGGGGG",
               "GGGGGGGGG GGGGG GGGG GGGG GGG GGG GGGGGG",
               "GGGGGGGGG GGGGG GGGG GGGG GGG GGG GGGGGG",
               "GGGGGGGGG GGGGG GGGG GGGG GGG GGG GGGGGG",
               "P   GGGGG GGGGG GGGG GGGG GGG GGG GG   C",
               "GGG GGGGG GGGGG GGGG GGGG GGG GGG GG GGG",
               "GGG GGGGG GGGGG GGGG GGGG GGG GGG GG GGG",
               "GGG GGGGG GGGGG GGGG GGGG GGG GGG GG GGG",
               "GGG GGGGG GGGGG GGGG GGGG GGG GGG GG GGG",
               "GGG GGGGG GGGGG GGGG GGGG GGG GGG    GGG",
               "GGG GGGGG GGGGG GGGG GGGG     GGGGGGGGGG",
               "GGG GGGGG GGGGG      GGGGGGGGGGGGGGGGGGG",
               "GGG       GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
               "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
               "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"]
