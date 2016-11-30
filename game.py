import collections
import creeps
import towers
import game_field
import consts
import unit

Map = collections.namedtuple('Map', 'row, col, type')
Point = collections.namedtuple('Point', 'row, col')


class Game:
    def __init__(self):
        self.field = self.get_field()
        self.portal = consts.PORTAL
        self.castle = consts.CASTLE
        self.end = False
        self.gold = consts.START_GOLD
        self.enemies_left = consts.ENEMIES_ALLOWED
        self.path = game_field.Path(self.portal, self.castle, self.field).path
        self.enemies = []

    @staticmethod
    def get_field():
        field = [[Map(0, 0, game_field.CellType.Grass)] * 40 for f in range(21)]
        string_field = consts.DEFAULT_MAP
        types = {'G': game_field.CellType.Grass,
                 ' ': game_field.CellType.Path,
                 'P': game_field.CellType.Portal,
                 'C': game_field.CellType.Castle}
        for row, str_field in enumerate(string_field):
            for col, element in enumerate(str_field):
                field[row][col] = Map(row, col, types[element])
        return field

    def place_unit(self, row, col, unit_type):
        unit_to_place = unit_type(row, col)
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

    def get_gold_number(self):
        return self.gold

    def get_remaining_enemies(self):
        return self.enemies_left

    def game_over(self):
        self.end = True
