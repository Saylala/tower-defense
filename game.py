import collections
import creeps
import towers
import game_logic
import consts

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
        creeps.get_path(self.portal, self.castle, self.field)

    @staticmethod
    def get_field():
        field = [[Map(0, 0, game_logic.Type.Grass)] * 40 for f in range(21)]
        string_field = consts.DEFAULT_MAP
        types = {'G': game_logic.Type.Grass,
                 ' ': game_logic.Type.Path,
                 'P': game_logic.Type.Portal,
                 'C': game_logic.Type.Castle}
        for row, str_field in enumerate(string_field):
            for col, element in enumerate(str_field):
                field[row][col] = Map(row, col, types[element])
        return field

    def place_unit(self, row, col, unit_type):
        if issubclass(unit_type, towers.Tower):
            price = consts.UNITS['towers'][unit_type.__name__].price
            if self.gold < price:
                return True
            self.gold -= price
        self.field[row][col] = unit_type(row, col)

    def get_gold_number(self):
        return self.gold

    def get_remaining_enemies(self):
        return self.enemies_left

    def game_over(self):
        self.end = True
