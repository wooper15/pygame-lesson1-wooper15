import asyncio
import random
import pygame
# add a coldown to the shooting, add levels, add multiple enemys, change player's speed, add enemy movement
# Start Pygame so its display, drawing, and input features are ready to use.
pygame.init()

WIDTH = 800
HEIGHT = 600

PLAYER_SIZE = 50    
# Make the projectile one third as wide and tall as the player square.
PROJECTILE_ONE_SIZE = PLAYER_SIZE // 3
SPEED = 7
VELOCITY = 15

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
    global x, y, target_x, target_y, score, active_projectiles

    # Use Pygame's default font at size 36 for the score display.
    font = pygame.font.Font(None, 36)
    start_text = font.render("START", True, (255, 255, 255))
    game_over_text = font.render("GAME OVER", True, (255, 255, 255))
    restart_text = font.render("RESTART", True, (255, 255, 255))
    start_button_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    restart_button_rect = restart_text.get_rect(
        center=(WIDTH // 2, game_over_rect.bottom + 20)
    )
    started = False
    timer_start = None
    time_remaining = 30
    running = True

    def restart_game():
        nonlocal timer_start, time_remaining
        global x, y, target_x, target_y, score, active_projectiles

        score = 0
        active_projectiles = []
        x = WIDTH // 2 - PLAYER_SIZE // 2
        y = HEIGHT - PLAYER_SIZE
        target_x = WIDTH // 2
        target_y = TARGET_RADIUS
        timer_start = pygame.time.get_ticks()
        time_remaining = 30

    while running:

        # EVENTS
        # Read all pending window events, such as a request to close the game.
        for event in pygame.event.get():
            # Stop the loop when the window's close button is pressed.
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if started:
                    projectile = projectile_template.copy()
                    projectile.centerx = x + PLAYER_SIZE // 2
                    projectile.bottom = y - 5
                    active_projectiles.append(projectile)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not started and start_button_rect.collidepoint(event.pos):
                    started = True
                    timer_start = pygame.time.get_ticks()
                elif time_remaining == 0 and restart_button_rect.collidepoint(event.pos):
                    restart_game()

        if started:
            time_remaining = max(0, 30 - (pygame.time.get_ticks() - timer_start) // 1000)
        game_active = started and time_remaining > 0

        # INPUT
        # Check which keyboard keys are currently held down.
        keys = pygame.key.get_pressed()

        if game_active:
            # Move the player a few pixels for each frame while an arrow key is held.
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                x -= SPEED

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                x += SPEED

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                y -= SPEED

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
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
        if game_active:
            for projectile in active_projectiles:
                projectile.y -= VELOCITY
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

        if not started:
            screen.blit(start_text, start_button_rect)
        elif time_remaining == 0:
            screen.blit(game_over_text, game_over_rect)
            screen.blit(restart_text, restart_button_rect)

        # Convert the score text into a drawable Pygame surface.
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        # Anchor the score's top-right corner inside the window.
        score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
        # Copy the rendered text onto the window at the selected position.
        screen.blit(score_text, score_rect)

        timer_text = font.render(f"Time: {time_remaining}", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(topleft=(10, 10))
        screen.blit(timer_text, timer_rect)

        coordinates_text = font.render(f"X: {x}, Y: {y}", True, (255, 255, 255))
        coordinates_rect = coordinates_text.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))
        screen.blit(coordinates_text, coordinates_rect)

        # Show the completed frame on the screen.
        pygame.display.flip()

        # Required for running Pygame in the browser
        # Yield control briefly so the browser can continue updating the game.
        await asyncio.sleep(0)

    pygame.quit()


# Start the asynchronous game loop.
asyncio.run(main())