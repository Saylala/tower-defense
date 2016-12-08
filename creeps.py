import collections
import consts
import unit
import game_field
import random

Point = collections.namedtuple('Point', 'row, col')
Map = collections.namedtuple('Map', 'row, col, type')


class Creep(unit.Unit):
    def __init__(self, row, col, name, game):
        super().__init__(row, col, unit.UnitType.Creep, name)
        creep_consts = consts.UNITS['creeps'][self.name]
        self.health, self.speed, self.reward, self.power = creep_consts
        self._id = 0
        self.dead = False
        self.normal_path = random.choice(game.paths)
        self.path = []
        self.allies = game.enemies
        self.enemies = game.allies
        self.radius = 3
        self.attack_radius = 1.5
        self.last_point = Point(row, col)

    def move(self, game):
        if self.dead:
            return True
        response = self.attack(game)
        if response is True:
            return
        self._id += 1
        if self._id == len(self.normal_path) - 1 or self.dead:
            if self._id == len(self.normal_path) - 1:
                game.enemies_left -= 1
                if game.enemies_left < 0:
                    game.game_over()
            return True
        next_cell = self.normal_path[self._id]
        self.row = next_cell.row
        self.col = next_cell.col
        self.last_point = next_cell

    def attack(self, game):
        if self.dead:
            return
        enemy = self.find_enemy()
        if not enemy:
            if Point(self.row, self.col) != self.last_point:
                self.path = game_field.Path.find_shortest_path(
                    Point(self.row, self.col),
                    self.last_point,
                    game.field)
                next_cell = self.path[1]
                self.row = next_cell.row
                self.col = next_cell.col
                return True
            return False
        if game_field.get_distance(self, enemy) <= self.attack_radius:
            enemy.take_hit(self.power, game)
            return
        self.path = game_field.Path.find_shortest_path(
            Point(self.row, self.col),
            Point(enemy.row, enemy.col),
            game.field)
        next_cell = self.path[1]
        self.row = next_cell.row
        self.col = next_cell.col
        return True

    def take_hit(self, damage, state):
        self.health -= damage
        if self.health <= 0:
            self.dead = True
            self.allies.remove(self)
            state.gold += self.reward

    def find_enemy(self):
        enemies_around = []
        for enemy in self.enemies:
            if game_field.get_distance(self, enemy) > self.radius or enemy.dead:
                continue
            enemies_around.append(enemy)
        if len(enemies_around) == 0:
            return
        return random.choice(enemies_around)


class Peon(Creep):
    def __init__(self, row, col, game):
        name = 'Peon'
        super().__init__(row, col, name, game)


class Grunt(Creep):
    def __init__(self, row, col, game):
        name = 'Grunt'
        super().__init__(row, col, name, game)


class Raider(Creep):
    def __init__(self, row, col, game):
        name = 'Raider'
        super().__init__(row, col, name, game)


class Blademaster(Creep):
    def __init__(self, row, col, game):
        name = 'Blademaster'
        super().__init__(row, col, name, game)


class Shaman(Creep):
    def __init__(self, row, col, game):
        name = 'Shaman'
        super().__init__(row, col, name, game)
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


class Footman(Creep):
    def __init__(self, row, col, game):
        name = 'Footman'
        super().__init__(row, col, name, game)
        self.last_point = Point(row, col)
        self.allies = game.allies
        self.enemies = game.enemies
        self.path = []

    def move(self, game):
        if self.dead:
            return True
        self.attack(game)
