import collections
from enum import Enum
import creeps

Map = collections.namedtuple('Map', 'row, col, type')
Point = collections.namedtuple('Point', 'row, col')


class Type(Enum):
    Grass = 1
    Path = 2
    Portal = 3
    Castle = 4


class Game:
    def __init__(self):
        self.field = self.get_field()
        self.portal = Point(10, 0)
        self.castle = Point(10, 39)
        self.end = False
        self.gold = 100
        creeps.get_path(self.portal, self.castle, self.field)

    @staticmethod
    def get_field():
        field = [[Map(0, 0, Type.Grass)] * 40 for f in range(21)]
        string_field = ["GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
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
        types = {'G': Type.Grass,
                 ' ': Type.Path,
                 'P': Type.Portal,
                 'C': Type.Castle}
        for row in range(len(string_field)):
            for col in range(len(string_field[0])):
                field[row][col] = Map(row, col, types[string_field[row][col]])
        return field

    def place_unit(self, row, col, unit_type):
        self.field[row][col] = unit_type(row, col)
