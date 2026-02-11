import pygame
import sys
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, FPS, WHITE, RED, GREEN, PLAYER_SPEED
from .player import Player
from .level import Level

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Geometry Dash Prototype")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    def reset_game():
        player = Player()
        level = Level()
        return player, level, False, False, 0 # game_over, victory, score

    player, level, game_over, victory, score = reset_game()
    
    # Ground rect for visualization
    ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)

    running = True
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if not game_over:
                        player.buffer_jump()
                    else:
                        player, level, game_over, victory, score = reset_game()
                if event.key == pygame.K_r:
                    player, level, game_over, victory, score = reset_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not game_over:
                        player.buffer_jump()
                    else:
                        player, level, game_over, victory, score = reset_game()
        
        if not game_over:
            # Update
            player.update()
            level.update(PLAYER_SPEED)
            score += PLAYER_SPEED
            
            # Check Victory
            if score >= 5000:
                game_over = True
                victory = True

            # Collision Detection
            collided_obstacles = pygame.sprite.spritecollide(player, level.obstacles, False)
            for obstacle in collided_obstacles:
                if obstacle.obstacle_type == 'spike':
                    game_over = True
                elif obstacle.obstacle_type == 'block':
                    overlap_rect = player.rect.clip(obstacle.rect)
                    
                    if overlap_rect.width < overlap_rect.height:
                        # Horizontal collision -> Side hit -> Game Over
                        game_over = True
                    else:
                        # Vertical collision
                        if player.velocity_y > 0:
                            # Falling down onto block
                            player.rect.bottom = obstacle.rect.top
                            player.y = player.rect.y
                            player.velocity_y = 0
                            player.on_ground = True
                            player.is_jumping = False
                        elif player.velocity_y < 0:
                            # Hitting head on bottom of block
                            player.rect.top = obstacle.rect.bottom
                            player.y = player.rect.y
                            player.velocity_y = 0

        
        # Draw
        screen.fill(BLACK)
        
        # Draw ground
        pygame.draw.rect(screen, WHITE, ground_rect)
        
        # Draw level
        level.draw(screen)
        
        # Draw player
        player.draw(screen)
        
        # Draw Score
        score_text = font.render(f"Score: {int(score)}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            if victory:
                text = font.render("You Win! Press SPACE/R to Restart", True, GREEN)
            else:
                text = font.render("Game Over! Press SPACE/R to Restart", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
