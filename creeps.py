import collections
import copy
import game

Point = collections.namedtuple('Point', 'row, col')


def in_field(field, point):
    return 0 <= point.row < len(field) and 0 <= point.col < len(field[0])


def find_path(start_point, end_point, field):
    points = collections.deque()
    points.append(start_point)
    deltas = [Point(0, 1), Point(1, 0), Point(-1, 0)]
    track = {start_point: None}
    temp_field = copy.deepcopy(field)
    while len(points) != 0:
        point = points.popleft()
        temp_field[point.row][point.col] = True
        for delta in deltas:
            new_point = Point(point.row + delta.row, point.col + delta.col)
            if (not in_field(temp_field, new_point) or
                    temp_field[new_point.row][new_point.col] is True or
                    temp_field[new_point.row][new_point.col].type == game.Type.Grass and
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
    global _path
    _path = find_path(start_point, end_point, field)


_path = []


class Creep:
    def __init__(self, row, col, health, speed):
        self.row = row
        self.col = col
        self.health = 0
        self._id = 0
        self.dead = False
        self.health = health
        self.speed = speed

    def move(self, field):
        global _path
        self._id += 1
        if self._id == len(_path) - 1 or self.dead:
            field[self.row][self.col] = game.Map(self.row, self.col, game.Type.Path)
            return True
        next_cell = _path[self._id]
        field[next_cell.row][next_cell.col] = self
        field[self.row][self.col] = game.Map(self.row, self.col, game.Type.Path)
        self.row = next_cell.row
        self.col = next_cell.col

    def take_hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.dead = True


class Peon(Creep):
    def __init__(self, row, col):
        super().__init__(row, col, 50, 20)


class Grunt(Creep):
    def __init__(self, row, col):
        super().__init__(row, col, 100, 15)


class Raider(Creep):
    def __init__(self, row, col):
        super().__init__(row, col, 80, 25)