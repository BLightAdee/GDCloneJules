import unittest
from geometry_dash.player import Player
from geometry_dash.constants import SCREEN_HEIGHT, JUMP_STRENGTH

class TestBuffering(unittest.TestCase):
    def test_buffer_set(self):
        player = Player()
        # Move to air
        player.y = player.ground_level - 100
        player.rect.y = int(player.y)
        player.on_ground = False

        player.buffer_jump()
        self.assertEqual(player.jump_buffer_timer, 10)
        self.assertFalse(player.is_jumping)

    def test_buffer_expires(self):
        player = Player()
        # Move to air
        player.y = player.ground_level - 100
        player.rect.y = int(player.y)
        player.on_ground = False

        player.buffer_jump()

        # Simulate 11 frames
        for _ in range(11):
            player.update()

        self.assertEqual(player.jump_buffer_timer, 0)

        # Now land
        player.y = player.ground_level
        player.rect.bottom = player.ground_level
        # Ensure velocity is downward so it hits
        player.velocity_y = 10

        player.update()

        # Should NOT jump
        self.assertFalse(player.is_jumping)

    def test_buffer_triggers_jump(self):
        player = Player()
        # Move to air
        player.y = player.ground_level - 100
        player.rect.y = int(player.y)
        player.on_ground = False

        player.buffer_jump()

        # Simulate 5 frames (buffer still active)
        for _ in range(5):
            player.update()

        self.assertGreater(player.jump_buffer_timer, 0)

        # Land
        # We need to position it so update() sees it hit the ground
        player.velocity_y = 10
        player.y = player.ground_level + 5 # Slightly below ground
        player.rect.y = int(player.y)

        player.update()

        # Should have jumped
        self.assertTrue(player.is_jumping)
        self.assertEqual(player.velocity_y, JUMP_STRENGTH)
        self.assertEqual(player.jump_buffer_timer, 0)

    def test_rotation(self):
        player = Player()
        # Start in air to rotate
        player.y = player.ground_level - 100
        player.rect.y = int(player.y)
        player.on_ground = False

        player.jump() # Actually jump just sets velocity, doesn't change pos immediately
        # But we are already in air

        initial_rotation = player.rotation # 0

        player.update()
        self.assertNotEqual(player.rotation, initial_rotation)

        # Land
        player.y = player.ground_level
        player.rect.bottom = player.ground_level
        player.velocity_y = 10

        player.update()

        # Rotation should snap (0 is nearest to -5)
        self.assertEqual(player.rotation, 0)

if __name__ == '__main__':
    unittest.main()
