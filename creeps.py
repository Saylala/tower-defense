import collections
import copy
import game_field
import consts
import unit

Point = collections.namedtuple('Point', 'row, col')
Map = collections.namedtuple('Map', 'row, col, type')


class Creep(unit.Unit):
    def __init__(self, row, col, name):
        super().__init__(row, col, unit.UnitType.Creep, name)
        self.health = 0
        self._id = 0
        self.dead = False

    def move(self, field, game):
        path = game.path
        self._id += 1
        if self._id == len(path) - 1 or self.dead:
            if self._id == len(path) - 1:
                game.enemies_left -= 1
                if game.enemies_left < 0:
                    game.game_over()
            return True
        next_cell = path[self._id]
        self.row = next_cell.row
        self.col = next_cell.col

    def take_hit(self, damage, state):
        self.health -= damage
        if self.health <= 0:
            self.dead = True
            state.enemies.remove(self)
            state.gold += self.reward


class Peon(Creep):
    def __init__(self, row, col):
        name = 'Peon'
        super().__init__(row, col, name)
        creep_consts = consts.UNITS['creeps'][self.name]
        self.health, self.speed, self.reward = creep_consts


class Grunt(Creep):
    def __init__(self, row, col):
        name = 'Grunt'
        super().__init__(row, col, name)
        creep_consts = consts.UNITS['creeps'][self.name]
        self.health, self.speed, self.reward = creep_consts


class Raider(Creep):
    def __init__(self, row, col):
        name = 'Raider'
        super().__init__(row, col, name)
        creep_consts = consts.UNITS['creeps'][self.name]
        self.health, self.speed, self.reward = creep_consts
