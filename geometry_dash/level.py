import pygame
import random
from .constants import SCREEN_HEIGHT, SCREEN_WIDTH, BLUE, WHITE

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, obstacle_type):
        super().__init__()
        self.obstacle_type = obstacle_type
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLUE if obstacle_type == 'block' else WHITE

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, surface):
        if self.obstacle_type == 'block':
            pygame.draw.rect(surface, self.color, self.rect)
        elif self.obstacle_type == 'spike':
            # Draw a triangle for spike
            points = [
                (self.rect.left, self.rect.bottom),
                (self.rect.right, self.rect.bottom),
                (self.rect.centerx, self.rect.top)
            ]
            pygame.draw.polygon(surface, self.color, points)

class Level:
    def __init__(self):
        self.obstacles = pygame.sprite.Group()
        self.ground_level = SCREEN_HEIGHT - 100
        self.next_x = SCREEN_WIDTH + 200 # Start generating off-screen
        self.generate_chunk(self.next_x)

    def generate_chunk(self, start_x):
        # Generate a pattern of obstacles
        patterns = [
            'single_spike',
            'double_spike',
            'triple_spike',
            'block',
            'block_jump',
            'spike_gap_spike'
        ]
        
        pattern = random.choice(patterns)
        current_x = start_x
        
        if pattern == 'single_spike':
            self.add_spike(current_x)
            current_x += 300
        elif pattern == 'double_spike':
            self.add_spike(current_x)
            self.add_spike(current_x + 40)
            current_x += 350
        elif pattern == 'triple_spike':
            self.add_spike(current_x)
            self.add_spike(current_x + 40)
            self.add_spike(current_x + 80)
            current_x += 400
        elif pattern == 'block':
            self.add_block(current_x)
            current_x += 300
        elif pattern == 'block_jump':
            self.add_block(current_x)
            self.add_spike(current_x + 200)
            current_x += 400
        elif pattern == 'spike_gap_spike':
            self.add_spike(current_x)
            self.add_spike(current_x + 200)
            current_x += 300
            
        self.next_x = current_x

    def add_spike(self, x):
        width = 40
        height = 40
        y = self.ground_level - height
        obstacle = Obstacle(x, y, width, height, 'spike')
        self.obstacles.add(obstacle)

    def add_block(self, x):
        width = 50
        height = 50
        y = self.ground_level - height
        obstacle = Obstacle(x, y, width, height, 'block')
        self.obstacles.add(obstacle)

    def update(self, speed):
        self.obstacles.update(speed)
        self.next_x -= speed # Update the generation cursor relative to screen

        # Generate new chunks if needed
        if self.next_x < SCREEN_WIDTH + 200:
             self.generate_chunk(self.next_x)

        # Remove obstacles that have gone off screen
        for obstacle in self.obstacles:
            if obstacle.rect.right < 0:
                obstacle.kill()

    def draw(self, surface):
        for obstacle in self.obstacles:
            obstacle.draw(surface)
