import unittest
import game
import towers
import creeps


class TestTower(unittest.TestCase):
    def test_gold_arcane(self):
        test_game = game.Game()
        test_game.place_unit(0, 0, towers.ArcaneTower)
        self.assertEqual(90, test_game.gold)

    def test_gold_guard(self):
        test_game = game.Game()
        test_game.place_unit(0, 0, towers.GuardTower)
        self.assertEqual(85, test_game.gold)

    def test_gold_canon(self):
        test_game = game.Game()
        test_game.place_unit(0, 0, towers.CanonTower)
        self.assertEqual(80, test_game.gold)

    def test_damage_arcane(self):
        test_game = game.Game()
        test_game.place_unit(0, 0, towers.ArcaneTower)
        test_game.place_unit(0, 1, creeps.Peon)
        test_game.field[0][0].attack(test_game)
        self.assertEqual(35, test_game.field[0][1].health)

    def test_damage_guard(self):
        test_game = game.Game()
        test_game.place_unit(0, 0, towers.GuardTower)
        test_game.place_unit(0, 1, creeps.Peon)
        test_game.field[0][0].attack(test_game)
        self.assertEqual(25, test_game.field[0][1].health)

    def test_damage_canon(self):
        test_game = game.Game()
        test_game.place_unit(0, 0, towers.CanonTower)
        test_game.place_unit(0, 1, creeps.Peon)
        test_game.field[0][0].attack(test_game)
        self.assertEqual(15, test_game.field[0][1].health)

    def test_range_arcane(self):
        test_game = game.Game()
        test_game.place_unit(0, 0, towers.ArcaneTower)
        test_game.place_unit(0, 4, creeps.Peon)
        test_game.field[0][0].attack(test_game)
        self.assertEqual(50, test_game.field[0][4].health)

    def test_range_guard(self):
        test_game = game.Game()
        test_game.place_unit(0, 0, towers.GuardTower)
        test_game.place_unit(0, 3, creeps.Peon)
        test_game.field[0][0].attack(test_game)
        self.assertEqual(50, test_game.field[0][3].health)

    def test_range_canon(self):
        test_game = game.Game()
        test_game.place_unit(0, 0, towers.CanonTower)
        test_game.place_unit(0, 2, creeps.Peon)
        test_game.field[0][0].attack(test_game)
        self.assertEqual(50, test_game.field[0][2].health)

if __name__ == '__main__':
    unittest.main()