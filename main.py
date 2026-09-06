import asyncio
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

PLAYER_SIZE = 50    
SPEED = 6

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Game")

x = 375
y = 275

TARGET_RADIUS = 25
target_x = 650
target_y = 300


async def main():
    global x, y

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

        # Subtract PLAYER_SIZE so the whole square stays inside the window.
        x = max(0, min(x, WIDTH - PLAYER_SIZE))
        y = max(0, min(y, HEIGHT - PLAYER_SIZE))

        # DRAW
        screen.fill((30, 30, 60))

        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (target_x, target_y),
            TARGET_RADIUS
        )

        pygame.draw.rect(
            screen,
            (255, 200, 50),
            (x, y, PLAYER_SIZE, PLAYER_SIZE)
        )

        pygame.display.flip()

        # Required for running Pygame in the browser
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())