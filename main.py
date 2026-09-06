import asyncio
import random
import pygame

# Start Pygame so its display, drawing, and input features are ready to use.
pygame.init()

WIDTH = 800
HEIGHT = 600

PLAYER_SIZE = 50    
# Make the projectile one third as wide and tall as the player square.
PROJECTILE_ONE_SIZE = PLAYER_SIZE // 3
SPEED = 3

# Create the window using the width and height chosen above.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Set the text shown in the window's title bar.
pygame.display.set_caption("My Pygame Game")

# Place the player's left edge at the horizontal center of the window.
x = WIDTH // 2 - PLAYER_SIZE // 2
# Start the player at the bottom, accounting for its height.
y = HEIGHT - PLAYER_SIZE

TARGET_RADIUS = 25
# A circle's x and y values describe its center, not its top-left corner.
target_x = WIDTH // 2
target_y = TARGET_RADIUS

# Place the projectile in the bottom-left corner of the window.
projectile_one_x = 0
projectile_one_y = HEIGHT - PROJECTILE_ONE_SIZE
projectile_template = pygame.Rect(
    projectile_one_x,
    projectile_one_y,
    PROJECTILE_ONE_SIZE,
    PROJECTILE_ONE_SIZE
)
active_projectiles = []
score = 0


async def main():
    # These global values are changed while the game loop is running.
    global x, y, target_x, score, active_projectiles

    # Use Pygame's default font at size 36 for the score display.
    font = pygame.font.Font(None, 36)
    running = True

    while running:

        # EVENTS
        # Read all pending window events, such as a request to close the game.
        for event in pygame.event.get():
            # Stop the loop when the window's close button is pressed.
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                projectile = projectile_template.copy()
                projectile.centerx = x + PLAYER_SIZE // 2
                projectile.bottom = y - 5
                active_projectiles.append(projectile)

        # INPUT
        # Check which keyboard keys are currently held down.
        keys = pygame.key.get_pressed()

        # Move the player a few pixels for each frame while an arrow key is held.
        if keys[pygame.K_LEFT]:
            x -= SPEED

        if keys[pygame.K_RIGHT]:
            x += SPEED

        if keys[pygame.K_UP]:
            y -= SPEED

        if keys[pygame.K_DOWN]:
            y += SPEED

        # Keep the square's top edge at or below the screen midpoint.
        # max() and min() keep the player's position within both boundaries.
        x = max(0, min(x, WIDTH - PLAYER_SIZE))
        y = max(HEIGHT // 2, min(y, HEIGHT - PLAYER_SIZE))

        # DRAW
        # Paint over the previous frame with the background color.
        screen.fill((30, 30, 60))

        # Use the circle's bounding box for pygame's rectangle collision check.
        target_rect = pygame.Rect(
            target_x - TARGET_RADIUS,
            target_y - TARGET_RADIUS,
            TARGET_RADIUS * 2,
            TARGET_RADIUS * 2
        )
        target_hit = False
        remaining_projectiles = []
        for projectile in active_projectiles:
            projectile.y -= SPEED
            if projectile.colliderect(target_rect):
                target_hit = True
                score += 1
                target_x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
            elif projectile.bottom > 0:
                remaining_projectiles.append(projectile)
        active_projectiles = remaining_projectiles

        # Draw the target; green indicates a hit and red means no hit this frame.
        pygame.draw.circle(
            screen,
            (0, 255, 0) if target_hit else (255, 0, 0),
            (target_x, target_y),
            TARGET_RADIUS
        )

        # Draw the player square using its current position.
        pygame.draw.rect(
            screen,
            (255, 200, 50),
            (x, y, PLAYER_SIZE, PLAYER_SIZE)
        )

        for projectile in active_projectiles:
            pygame.draw.rect(screen, (80, 220, 255), projectile)

        # Convert the score text into a drawable Pygame surface.
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        # Anchor the score's top-right corner inside the window.
        score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
        # Copy the rendered text onto the window at the selected position.
        screen.blit(score_text, score_rect)

        # Show the completed frame on the screen.
        pygame.display.flip()

        # Required for running Pygame in the browser
        # Yield control briefly so the browser can continue updating the game.
        await asyncio.sleep(0)

    pygame.quit()


# Start the asynchronous game loop.
asyncio.run(main())