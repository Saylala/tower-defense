import collections
import consts
import unit
import game_field

Point = collections.namedtuple('Point', 'row, col')
Map = collections.namedtuple('Map', 'row, col, type')


class Creep(unit.Unit):
    def __init__(self, row, col, name):
        super().__init__(row, col, unit.UnitType.Creep, name)
        creep_consts = consts.UNITS['creeps'][self.name]
        self.health, self.speed, self.reward = creep_consts
        self._id = 0
        self.dead = False

    def move(self, game):
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


class Grunt(Creep):
    def __init__(self, row, col):
        name = 'Grunt'
        super().__init__(row, col, name)


class Raider(Creep):
    def __init__(self, row, col):
        name = 'Raider'
        super().__init__(row, col, name)


class Blademaster(Creep):
    def __init__(self, row, col):
        name = 'Blademaster'
        super().__init__(row, col, name)


class Shaman(Creep):
    def __init__(self, row, col):
        name = 'Shaman'
        super().__init__(row, col, name)
        self.buffed_allies = {}
        self.aura_radius = 3
        self.heal_buff = 0.25
        self.speed_buff = 5

    def move(self, game):
        self.heal(game)
        self.buff_speed(game)
        dead = super().move(game)
        if dead is True:
            self.debuff_speed()
        return dead

    def heal(self, game):
        allies = game.enemies
        for ally in allies:
            distance = game_field.get_distance(ally, self)
            max_health = consts.MAX_HEALTH[ally.name]
            if distance > self.aura_radius or ally.health == max_health:
                continue
            ally.health += self.heal_buff

    def debuff_speed(self):
        for ally in self.buffed_allies:
            ally.speed = self.buffed_allies[ally]
        self.buffed_allies = {}

    def buff_speed(self, game):
        self.debuff_speed()
        allies = game.enemies
        for ally in allies:
            distance = game_field.get_distance(ally, self)
            if distance > self.aura_radius:
                continue
            self.buffed_allies[ally] = ally.speed
            ally.speed += self.speed_buff
