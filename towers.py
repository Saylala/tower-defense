import math
import collections
import game_field
import creeps
import consts
import unit

Point = collections.namedtuple('Point', 'row, col')


class Tower(unit.Unit):
    def __init__(self, row, col, name):
        super().__init__(row, col, unit.UnitType.Tower, name)

    def attack(self, state):
        enemies = state.enemies
        for enemy in enemies:
                distance = game_field.get_distance(enemy, self)
                if distance > self.range:
                    continue
                enemy.take_hit(self.damage, state)
                return enemy


class ArcaneTower(Tower):
    def __init__(self, row, col):
        name = 'ArcaneTower'
        super().__init__(row, col, name)
        tower_consts = consts.UNITS['towers'][self.name]
        self.damage, self.range, self.speed, self.price = tower_consts


class GuardTower(Tower):
    def __init__(self, row, col):
        name = 'GuardTower'
        super().__init__(row, col, name)
        tower_consts = consts.UNITS['towers'][self.name]
        self.damage, self.range, self.speed, self.price = tower_consts


class CanonTower(Tower):
    def __init__(self, row, col):
        name = 'CanonTower'
        super().__init__(row, col, name)
        tower_consts = consts.UNITS['towers'][self.name]
        self.damage, self.range, self.speed, self.price = tower_consts

    def attack(self, state):
        enemy = super().attack(state)
        if not enemy:
            return
        neighbors = state.enemies
        for neighbor in neighbors:
            distance = game_field.get_distance(enemy, neighbor)
            if distance > self.range or neighbor == enemy:
                continue
            neighbor.take_hit(self.damage, state)
        return enemy
