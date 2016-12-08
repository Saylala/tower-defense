import collections
import consts
import game_field
import unit
import creeps
import random

Point = collections.namedtuple('Point', 'row, col')


class Tower(unit.Unit):
    def __init__(self, row, col, name, game):
        super().__init__(row, col, unit.UnitType.Tower, name)
        self.game = game
        tower_consts = consts.UNITS['towers'][self.name]
        self.damage, self.range, self.speed, self.price = tower_consts

    def attack(self, state):
        enemies = state.enemies
        for enemy in enemies:
                distance = game_field.get_distance(enemy, self)
                if distance > self.range or enemy.name == 'Blademaster':
                    continue
                enemy.take_hit(self.damage, state)
                return enemy


class ArcaneTower(Tower):
    def __init__(self, row, col, game):
        name = 'ArcaneTower'
        super().__init__(row, col, name, game)


class GuardTower(Tower):
    def __init__(self, row, col, game):
        name = 'GuardTower'
        super().__init__(row, col, name, game)


class CanonTower(Tower):
    def __init__(self, row, col, game):
        name = 'CanonTower'
        super().__init__(row, col, name, game)

    def attack(self, state):
        enemy = super().attack(state)
        if not enemy:
            return
        neighbors = state.enemies
        for neighbor in neighbors:
            distance = game_field.get_distance(enemy, neighbor)
            if (distance > self.range or neighbor == enemy or
                    neighbor.name == 'Blademaster'):
                continue
            neighbor.take_hit(self.damage, state)
        return enemy


class MagicTower(Tower):
    def __init__(self, row, col, game):
        name = 'MagicTower'
        super().__init__(row, col, name, game)

    def attack(self, state):
        enemies = state.enemies
        for enemy in enemies:
                distance = game_field.get_distance(enemy, self)
                if distance > self.range or enemy.name != 'Blademaster':
                    continue
                enemy.take_hit(self.damage, state)
                return enemy


class BarracksTower(Tower):
    def __init__(self, row, col, game):
        name = 'BarracksTower'
        super().__init__(row, col, name, game)
        self.creep = creeps.Footman(0, 0, self.game)
        self.max_creep_number = 2
        self.creep_type = [self.creep]
        self.creeps = []
        self.spawn_range = 1

    def attack(self, state):
        for creep in self.creeps:
            if creep.dead:
                self.creeps.remove(creep)
        founded_points = self.find_points(state.field)
        points = []
        for i in range(len(self.creeps), self.max_creep_number):
            points.append(founded_points[i])
        return points

    def find_points(self, field):
        points = []
        for row in range(-self.spawn_range, self.spawn_range + 1):
            for col in range(-self.spawn_range, self.spawn_range + 1):
                if row == 0 and col == 0:
                    continue
                new_point = Point(self.row + row, self.col + col)
                if game_field.in_field(field, new_point):
                    points.append(new_point)
        point1 = random.choice(points)
        points.remove(point1)
        point2 = random.choice(points)
        return [point1, point2]
