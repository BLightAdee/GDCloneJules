import unittest
from geometry_dash.player import Player
from geometry_dash.constants import SCREEN_HEIGHT, GRAVITY, JUMP_STRENGTH

class TestPlayer(unittest.TestCase):
    def test_initial_state(self):
        player = Player()
        self.assertEqual(player.velocity_y, 0)
        self.assertTrue(player.on_ground)
        # Player starts on ground (SCREEN_HEIGHT - 100)
        self.assertEqual(player.rect.bottom, SCREEN_HEIGHT - 100)

    def test_jump(self):
        player = Player()
        # Ensure player is on ground before jumping
        player.on_ground = True
        player.jump()
        self.assertEqual(player.velocity_y, JUMP_STRENGTH)
        self.assertTrue(player.is_jumping)
        self.assertFalse(player.on_ground)

    def test_gravity(self):
        player = Player()
        player.rect.y = 100 # Put player in air
        player.y = 100
        player.velocity_y = 0
        player.on_ground = False # Manually set not on ground for test context if needed, but update handles it
        
        player.update()
        
        # Velocity should increase by gravity
        self.assertEqual(player.velocity_y, GRAVITY)
        # Y position should increase by velocity
        self.assertEqual(player.y, 100 + GRAVITY)

    def test_ground_collision(self):
        player = Player()
        player.rect.y = SCREEN_HEIGHT - 100 - player.height + 50 # Below ground (simulate falling fast)
        player.y = player.rect.y
        player.velocity_y = 10
        
        player.update()
        
        # Should snap to ground
        self.assertEqual(player.rect.bottom, SCREEN_HEIGHT - 100)
        self.assertEqual(player.velocity_y, 0)
        self.assertTrue(player.on_ground)

if __name__ == '__main__':
    unittest.main()
