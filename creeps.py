import collections
import copy
import game_logic
import consts

Point = collections.namedtuple('Point', 'row, col')
Map = collections.namedtuple('Map', 'row, col, type')


def find_path(start_point, end_point, field):
    points = collections.deque()
    points.append(start_point)
    deltas = [Point(0, 1), Point(1, 0), Point(-1, 0)]
    track = {start_point: None}
    temp_field = copy.deepcopy(field)
    grass = game_logic.Type.Grass
    while len(points) != 0:
        point = points.popleft()
        temp_field[point.row][point.col] = True
        for delta in deltas:
            new_point = Point(point.row + delta.row, point.col + delta.col)
            if (not game_logic.in_field(temp_field, new_point) or
                    temp_field[new_point.row][new_point.col] is True or
                    temp_field[new_point.row][new_point.col].type == grass and
                    new_point != start_point):
                continue
            points.append(new_point)
            track[new_point] = point
    path_item = end_point
    path = []
    while path_item is not None:
        path.append(path_item)
        path_item = track[path_item]
    path.reverse()
    return path


def get_path(start_point, end_point, field):
    global PATH
    PATH = find_path(start_point, end_point, field)


PATH = []


class Creep:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.health = 0
        self._id = 0
        self.dead = False

    def move(self, field, game):
        global PATH
        self._id += 1
        if self._id == len(PATH) - 1 or self.dead:
            if self._id == len(PATH) - 1:
                game.enemies_left -= 1
                if game.enemies_left < 0:
                    game.game_over()
            field[self.row][self.col] = Map(
                self.row, self.col, game_logic.Type.Path)
            return True
        next_cell = PATH[self._id]
        field[next_cell.row][next_cell.col] = self
        field[self.row][self.col] = Map(
            self.row, self.col, game_logic.Type.Path)
        self.row = next_cell.row
        self.col = next_cell.col

    def take_hit(self, damage, state):
        self.health -= damage
        if self.health <= 0:
            self.dead = True
            state.gold += self.reward


class Peon(Creep):
    def __init__(self, row, col):
        super().__init__(row, col)
        name = 'Peon'
        creep_consts = consts.UNITS['creeps'][name]
        self.health, self.speed, self.reward = creep_consts


class Grunt(Creep):
    def __init__(self, row, col):
        super().__init__(row, col)
        name = 'Grunt'
        creep_consts = consts.UNITS['creeps'][name]
        self.health, self.speed, self.reward = creep_consts


class Raider(Creep):
    def __init__(self, row, col):
        super().__init__(row, col)
        name = 'Raider'
        creep_consts = consts.UNITS['creeps'][name]
        self.health, self.speed, self.reward = creep_consts
