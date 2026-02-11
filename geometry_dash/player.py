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

        # Buffering and Rotation
        self.jump_buffer_timer = 0
        self.rotation = 0
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
        self.original_image = self.image.copy()

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

        # Buffering Logic
        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= 1
            if self.on_ground:
                self.jump()
                self.jump_buffer_timer = 0

        # Rotation Logic
        if not self.on_ground:
            self.rotation -= 5 # Rotate counter-clockwise
            self.rotation %= 360
        else:
            # Snap to nearest 90
            nearest_90 = round(self.rotation / 90) * 90
            self.rotation = nearest_90 % 360

    def buffer_jump(self):
        self.jump_buffer_timer = 10 # 10 frames buffer
        if self.on_ground:
            self.jump()
            self.jump_buffer_timer = 0

    def jump(self):
        self.velocity_y = JUMP_STRENGTH
        self.is_jumping = True
        self.on_ground = False

    def draw(self, surface):
        # Rotate image
        rotated_image = pygame.transform.rotate(self.original_image, self.rotation)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, new_rect)
