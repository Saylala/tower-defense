import collections
import unittest
import game
import creeps
import game_field

Map = collections.namedtuple('Map', 'row, col, type')
Point = collections.namedtuple('Point', 'row, col')


class TestPath(unittest.TestCase):
    def test_simple_field1(self):
        path = game_field.CellType.Path
        field = [[Map(0, 0, path), Map(0, 1, path), Map(0, 2, path)]]
        result = set(creeps.find_path(Point(0, 0), Point(0, 0), field))
        expected = {Point(0, 0)}
        self.assertEqual(expected, result)

    def test_simple_field2(self):
        path = game_field.CellType.Path
        field = [[Map(0, 0, path), Map(0, 1, path), Map(0, 2, path)]]
        result = set(creeps.find_path(Point(0, 0), Point(0, 1), field))
        expected = {Point(0, 0), Point(0, 1)}
        self.assertEqual(expected, result)

    def test_simple_field3(self):
        path = game_field.CellType.Path
        field = [[Map(0, 0, path), Map(0, 1, path), Map(0, 2, path)]]
        result = set(creeps.find_path(Point(0, 0), Point(0, 2), field))
        expected = {Point(0, 0), Point(0, 1), Point(0, 2)}
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()