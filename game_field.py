import math
import collections
import copy
from enum import Enum

Point = collections.namedtuple('Point', 'row, col')
Map = collections.namedtuple('Map', 'row, col, type')


class CellType(Enum):
    Grass = 1
    Path = 2
    Portal = 3
    Castle = 4


def in_field(field, point):
    return 0 <= point.row < len(field) and 0 <= point.col < len(field[0])


def get_distance(point1, point2):
    return math.sqrt(math.pow(point1.row - point2.row, 2)
                     + math.pow(point1.col - point2.col, 2))


class Path:
    def __init__(self, start_point, end_point, field):
        self.path = []
        self.find_path(start_point, end_point, field)

    def find_path(self, start_point, end_point, field):
        points = collections.deque()
        points.append(start_point)
        deltas = [Point(0, 1), Point(1, 0), Point(-1, 0)]
        track = {start_point: None}
        temp_field = copy.deepcopy(field)
        grass = CellType.Grass
        while len(points) != 0:
            point = points.popleft()
            temp_field[point.row][point.col] = True
            for delta in deltas:
                new_point = Point(point.row + delta.row, point.col + delta.col)
                if (not in_field(temp_field, new_point) or
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
        self.path = path
