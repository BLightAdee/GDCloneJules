import pygame
from .constants import SCREEN_HEIGHT, GRAVITY, JUMP_STRENGTH, RED

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 40
        self.x = 100
        self.y = SCREEN_HEIGHT - 100 - self.height  # Start on ground
        self.velocity_y = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_jumping = False
        self.on_ground = True # Assume on ground initially
        self.ground_level = SCREEN_HEIGHT - 100

    def update(self):
        # Apply Gravity
        self.velocity_y += GRAVITY
        
        # Update Y position
        self.y += self.velocity_y
        self.rect.y = int(self.y)

        # Ground Collision (Simple floor at SCREEN_HEIGHT - 100)
        if self.rect.bottom >= self.ground_level:
            self.rect.bottom = self.ground_level
            self.y = self.rect.y
            self.velocity_y = 0
            self.on_ground = True
            self.is_jumping = False
        else:
            self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
            self.on_ground = False

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)
