import collections
import game_logic
import creeps

Point = collections.namedtuple('Point', 'row, col')


class Tower:
    def __init__(self, row, col, damage, attack_range, attack_speed, attack_color):
        self.row = row
        self.col = col
        self.damage = damage
        self.attack_range = attack_range
        self.attack_speed = attack_speed
        self.attack_color = attack_color

    def attack(self, field):
        enemies = [creeps.Peon, creeps.Grunt, creeps.Raider]
        for row in range(
                        self.row-self.attack_range,
                        self.row+self.attack_range+1):
            for col in range(self.col-self.attack_range,
                             self.col+self.attack_range+1):
                if not game_logic.in_field(field, Point(row, col)):
                    continue
                if not type(field[row][col]) in enemies:
                    continue
                field[row][col].take_hit(self.damage)
                return field[row][col]


class Arcane_Tower(Tower):
    def __init__(self, row, col):
        super().__init__(row, col, 15, 3, 5, 'red')


class Guard_Tower(Tower):
    def __init__(self, row, col):
        super().__init__(row, col, 25, 2, 5, 'brown')


class Canon_Tower(Tower):
    def __init__(self, row, col):
        super().__init__(row, col, 35, 1, 3, 'black')
