from enum import Enum


class Type(Enum):
    Grass = 1
    Path = 2
    Portal = 3
    Castle = 4


def in_field(field, point):
    return 0 <= point.row < len(field) and 0 <= point.col < len(field[0])
