import collections
import game_field
import consts
import unit
import random

Map = collections.namedtuple('Map', 'row, col, name')
Point = collections.namedtuple('Point', 'row, col')


class Game:
    def __init__(self):
        self.field = self.get_field()
        self.portal = consts.PORTAL
        self.castle = consts.CASTLE
        self.end = False
        self.gold = consts.START_GOLD
        self.enemies_left = consts.ENEMIES_ALLOWED
        self.enemies = []
        self.allies = []
        self.debuffed_enemies = {}
        self.paths = game_field.Path(self.portal, self.castle, self.field).paths

    @staticmethod
    def get_field():
        string_field = random.choice(consts.LEVELS)
        width = len(string_field)
        height = len(string_field[0])
        field = [[Map(0, 0, game_field.CellType.Grass)] * height for f in range(width)]
        types = {'G': game_field.CellType.Grass,
                 ' ': game_field.CellType.Path,
                 'P': game_field.CellType.Portal,
                 'C': game_field.CellType.Castle}
        for row, str_field in enumerate(string_field):
            for col, element in enumerate(str_field):
                field[row][col] = Map(row, col, types[element])
        return field

    def place_unit(self, row, col, unit_type):
        unit_to_place = unit_type(row, col, self)
        if unit_to_place.unit_type == unit.UnitType.Tower:
            price = consts.UNITS['towers'][unit_type.__name__].price
            if self.gold < price:
                return True
            self.gold -= price
        if unit_to_place.unit_type == unit.UnitType.Tower:
            self.field[row][col] = unit_to_place
        else:
            self.enemies.append(unit_to_place)
            return unit_to_place

    def place_ally(self, tower, ally, unit_type):
        unit_to_place = unit_type(ally.row, ally.col, self)
        self.allies.append(unit_to_place)
        tower.creeps.append(unit_to_place)
        return unit_to_place

    def get_gold_number(self):
        return self.gold

    def get_remaining_enemies(self):
        return self.enemies_left

    def game_over(self):
        self.end = True

    def cast_fire(self):
        if self.gold < consts.FIRE_PRICE or len(self.enemies) == 0:
            return False
        self.gold -= consts.FIRE_PRICE
        target = random.choice(self.enemies)
        for enemy in self.enemies:
            distance = game_field.get_distance(target, enemy)
            if distance > consts.FIRE_RADIUS:
                continue
            enemy.take_hit(consts.FIRE_DAMAGE, self)
        return target

    def cast_ice(self):
        if self.gold < consts.ICE_PRICE or len(self.enemies) == 0:
            return False
        self.gold -= consts.ICE_PRICE
        target = random.choice(self.enemies)
        for enemy in self.enemies:
            distance = game_field.get_distance(target, enemy)
            if (distance > consts.ICE_RADIUS
                or enemy.speed <= consts.ICE_SLOWDOWN):
                continue
            self.debuffed_enemies[enemy] = enemy.speed
            enemy.speed -= consts.ICE_SLOWDOWN
        return target

    def disable_ice_debuff(self):
        for enemy in self.debuffed_enemies:
            enemy.speed = self.debuffed_enemies[enemy]
        self.debuffed_enemies = {}
