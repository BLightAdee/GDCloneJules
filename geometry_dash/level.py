import pygame
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
        self.generate_level()

    def generate_level(self):
        # Create a simple level layout
        # Blocks and spikes
        import random
        
        current_x = SCREEN_WIDTH + 200 # Start generating off-screen
        
        for _ in range(20): # Generate 20 obstacles for now
            obstacle_type = random.choice(['block', 'spike', 'spike'])
            
            if obstacle_type == 'block':
                width = 50
                height = 50
                y = self.ground_level - height
                obstacle = Obstacle(current_x, y, width, height, 'block')
                self.obstacles.add(obstacle)
                current_x += 200 # Gap after block
            elif obstacle_type == 'spike':
                width = 40
                height = 40
                y = self.ground_level - height
                obstacle = Obstacle(current_x, y, width, height, 'spike')
                self.obstacles.add(obstacle)
                current_x += 150 # Gap after spike

    def update(self, speed):
        self.obstacles.update(speed)
        
        # Remove obstacles that have gone off screen
        for obstacle in self.obstacles:
            if obstacle.rect.right < 0:
                obstacle.kill()

    def draw(self, surface):
        for obstacle in self.obstacles:
            obstacle.draw(surface)
