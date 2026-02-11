import unittest
from geometry_dash.level import Level, Obstacle
from geometry_dash.constants import SCREEN_WIDTH

class TestLevel(unittest.TestCase):
    def test_level_generation(self):
        level = Level()
        self.assertTrue(len(level.obstacles) > 0)
        
        # Check first obstacle is off-screen initially (x > SCREEN_WIDTH)
        first_obstacle = level.obstacles.sprites()[0]
        self.assertTrue(first_obstacle.rect.x > SCREEN_WIDTH)

    def test_level_update(self):
        level = Level()
        first_obstacle = level.obstacles.sprites()[0]
        initial_x = first_obstacle.rect.x
        
        speed = 5
        level.update(speed)
        
        self.assertEqual(first_obstacle.rect.x, initial_x - speed)

if __name__ == '__main__':
    unittest.main()
