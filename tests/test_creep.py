import collections
import unittest
import game
import towers
import creeps
import game_field

Point = collections.namedtuple('Point', 'row, col')
Map = collections.namedtuple('Map', 'row, col, type')


class TestCreep(unittest.TestCase):
    def test_move_peon(self):
        test_game = game.Game()
        entrance = test_game.portal
        test_game.place_unit(entrance.row, entrance.col, creeps.Peon)
        creep = test_game.field[entrance.row][entrance.col]
        creep.move(test_game.field, test_game)
        self.assertEqual(Point(entrance.row, entrance.col+1), Point(creep.row, creep.col))

    def test_move_grunt(self):
        test_game = game.Game()
        entrance = test_game.portal
        test_game.place_unit(entrance.row, entrance.col, creeps.Grunt)
        creep = test_game.field[entrance.row][entrance.col]
        creep.move(test_game.field, test_game)
        self.assertEqual(Point(entrance.row, entrance.col+1), Point(creep.row, creep.col))

    def test_move_raider(self):
        test_game = game.Game()
        entrance = test_game.portal
        test_game.place_unit(entrance.row, entrance.col, creeps.Raider)
        creep = test_game.field[entrance.row][entrance.col]
        creep.move(test_game.field, test_game)
        self.assertEqual(Point(entrance.row, entrance.col+1), Point(creep.row, creep.col))

    def test_death_peon(self):
        test_game = game.Game()
        entrance = test_game.portal
        test_game.place_unit(entrance.row, entrance.col, creeps.Peon)
        creep = test_game.field[entrance.row][entrance.col]
        creep.take_hit(60, test_game)
        creep.move(test_game.field, test_game)
        self.assertEqual(
            test_game.field[entrance.row][entrance.col],
            Map(entrance.row, entrance.col, game_field.CellType.Path))

    def test_death_grunt(self):
        test_game = game.Game()
        entrance = test_game.portal
        test_game.place_unit(entrance.row, entrance.col, creeps.Grunt)
        creep = test_game.field[entrance.row][entrance.col]
        creep.take_hit(110, test_game)
        creep.move(test_game.field, test_game)
        self.assertEqual(
            test_game.field[entrance.row][entrance.col],
            Map(entrance.row, entrance.col, game_field.CellType.Path))

    def test_death_raider(self):
        test_game = game.Game()
        entrance = test_game.portal
        test_game.place_unit(entrance.row, entrance.col, creeps.Raider)
        creep = test_game.field[entrance.row][entrance.col]
        creep.take_hit(90, test_game)
        creep.move(test_game.field, test_game)
        self.assertEqual(
            test_game.field[entrance.row][entrance.col],
            Map(entrance.row, entrance.col, game_field.CellType.Path))

    def test_reward_peon(self):
        test_game = game.Game()
        entrance = test_game.portal
        test_game.place_unit(entrance.row, entrance.col, creeps.Peon)
        creep = test_game.field[entrance.row][entrance.col]
        creep.take_hit(60, test_game)
        self.assertEqual(test_game.gold, 110)

    def test_reward_grunt(self):
        test_game = game.Game()
        entrance = test_game.portal
        test_game.place_unit(entrance.row, entrance.col, creeps.Grunt)
        creep = test_game.field[entrance.row][entrance.col]
        creep.take_hit(110, test_game)
        self.assertEqual(test_game.gold, 115)

    def test_reward_raider(self):
        test_game = game.Game()
        entrance = test_game.portal
        test_game.place_unit(entrance.row, entrance.col, creeps.Raider)
        creep = test_game.field[entrance.row][entrance.col]
        creep.take_hit(90, test_game)
        self.assertEqual(test_game.gold, 120)

if __name__ == '__main__':
    unittest.main()