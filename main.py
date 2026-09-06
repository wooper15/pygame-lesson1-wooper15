import asyncio
import random
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

PLAYER_SIZE = 50    
PROJECTILE_ONE_SIZE = PLAYER_SIZE // 3
SPEED = 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Game")

x = WIDTH // 2 - PLAYER_SIZE // 2
y = HEIGHT - PLAYER_SIZE

TARGET_RADIUS = 25
target_x = WIDTH // 2
target_y = TARGET_RADIUS

projectile_one_x = WIDTH // 2 - PROJECTILE_ONE_SIZE // 2
projectile_one_y = y - PROJECTILE_ONE_SIZE - 5
score = 0


async def main():
    global x, y, target_x, score

    font = pygame.font.Font(None, 36)
    running = True

    while running:

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # INPUT
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            x -= SPEED

        if keys[pygame.K_RIGHT]:
            x += SPEED

        if keys[pygame.K_UP]:
            y -= SPEED

        if keys[pygame.K_DOWN]:
            y += SPEED

        # Keep the square's top edge at or below the screen midpoint.
        x = max(0, min(x, WIDTH - PLAYER_SIZE))
        y = max(HEIGHT // 2, min(y, HEIGHT - PLAYER_SIZE))

        # DRAW
        screen.fill((30, 30, 60))

        projectile_rect = pygame.Rect(
            projectile_one_x,
            projectile_one_y,
            PROJECTILE_ONE_SIZE,
            PROJECTILE_ONE_SIZE
        )
        # Use the circle's bounding box for pygame's rectangle collision check.
        target_rect = pygame.Rect(
            target_x - TARGET_RADIUS,
            target_y - TARGET_RADIUS,
            TARGET_RADIUS * 2,
            TARGET_RADIUS * 2
        )
        target_hit = projectile_rect.colliderect(target_rect)
        if target_hit:
            score += 1
            # Keep the target's full diameter inside the window.
            target_x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)

        pygame.draw.circle(
            screen,
            (0, 255, 0) if target_hit else (255, 0, 0),
            (target_x, target_y),
            TARGET_RADIUS
        )

        pygame.draw.rect(
            screen,
            (255, 200, 50),
            (x, y, PLAYER_SIZE, PLAYER_SIZE)
        )

        pygame.draw.rect(
            screen,
            (80, 220, 255),
            (
                projectile_one_x,
                projectile_one_y,
                PROJECTILE_ONE_SIZE,
                PROJECTILE_ONE_SIZE
            )
        )

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        # Anchor the score's top-right corner inside the window.
        score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(score_text, score_rect)

        pygame.display.flip()

        # Required for running Pygame in the browser
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())