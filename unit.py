from enum import Enum


class UnitType(Enum):
    Tower = 0
    Creep = 1


class Unit:
    def __init__(self, row, col, unit_type, name):
        self.row = row
        self.col = col
        self.unit_type = unit_type
        self.name = name
