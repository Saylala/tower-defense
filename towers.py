import collections
import game_logic
import creeps
import consts

Point = collections.namedtuple('Point', 'row, col')


class Tower:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def attack(self, state):
        enemies = [creeps.Peon, creeps.Grunt, creeps.Raider]
        field = state.field
        for row in range(self.row-self.range, self.row+self.range+1):
            for col in range(self.col-self.range, self.col+self.range+1):
                if not game_logic.in_field(field, Point(row, col)):
                    continue
                if type(field[row][col]) not in enemies:
                    continue
                field[row][col].take_hit(self.damage, state)
                return field[row][col]


class ArcaneTower(Tower):
    def __init__(self, row, col):
        super().__init__(row, col)
        name = 'ArcaneTower'
        tower_consts = consts.UNITS['towers'][name]
        self.damage, self.range, self.speed, self.price = tower_consts


class GuardTower(Tower):
    def __init__(self, row, col):
        super().__init__(row, col)
        name = 'GuardTower'
        tower_consts = consts.UNITS['towers'][name]
        self.damage, self.range, self.speed, self.price = tower_consts


class CanonTower(Tower):
    def __init__(self, row, col):
        super().__init__(row, col)
        name = 'CanonTower'
        tower_consts = consts.UNITS['towers'][name]
        self.damage, self.range, self.speed, self.price = tower_consts
