import math
import collections
import copy
from enum import Enum

Point = collections.namedtuple('Point', 'row, col')
Map = collections.namedtuple('Map', 'row, col, name')


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
        self.paths = []
        self.crossroads = []
        self.find_paths(start_point, end_point, field)

    def find_paths(self, start_point, end_point, field):
        path = [start_point]
        self.find_path(end_point, field, path)

    def find_path(self, end_point, field, current_path):
        previous = current_path[-1]
        neighbours = self.get_neighbours(previous, field)
        for neighbour in neighbours:
            if neighbour == end_point:
                current_path.append(neighbour)
                self.paths.append(current_path)
                return
            if neighbour in current_path:
                continue
            if len(neighbours) == 1:
                current_path.append(neighbour)
                self.find_path(end_point, field, current_path)
            else:
                new_field = copy.deepcopy(current_path)
                new_field.append(neighbour)
                self.find_path(end_point, field, new_field)

    @staticmethod
    def get_neighbours(point, field):
        neighbours = []
        grass = CellType.Grass
        deltas = [Point(0, 1), Point(1, 0), Point(-1, 0)]
        for delta in deltas:
            new_point = Point(point.row + delta.row, point.col + delta.col)
            if (not in_field(field, new_point) or
                    field[new_point.row][new_point.col].name == grass):
                continue
            neighbours.append(new_point)
        return neighbours

    @staticmethod
    def find_shortest_path(start_point, end_point, field):
        points = collections.deque()
        points.append(start_point)
        deltas = [Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0)]
        track = {start_point: None}
        temp_field = copy.deepcopy(field)
        stop = False
        while len(points) != 0:
            point = points.popleft()
            temp_field[point.row][point.col] = True
            for delta in deltas:
                new_point = Point(point.row + delta.row, point.col + delta.col)
                if (not in_field(temp_field, new_point) or
                        temp_field[new_point.row][new_point.col] is True):
                    continue
                points.append(new_point)
                track[new_point] = point
                if new_point == end_point:
                    stop = True
            if stop:
                break
        path_item = end_point
        path = []
        while path_item is not None:
            path.append(path_item)
            path_item = track[path_item]

        path.reverse()
        return path
