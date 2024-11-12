import pygame
import random
import sys
import os


# Initialize Pygame
pygame.init()

try:
    pygame.mixer.init()  # Initialize mixer for sound
except pygame.error:
    print("No audio device detected; sound disabled.")
    pygame.mixer = None  # Disable mixer if no audio device is available

# Load background music
audio_file = "C:/Users/mayar/Desktop/JeuGraphique/dammi_falastini.mp3"
if os.path.isfile(audio_file):
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play(-1)
else:
    print(f"Audio file {audio_file} not found.")

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu 2D - Free Palestine")

# Colors
BLUE_SKY = (135, 206, 250)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)

# Fonts
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)
font_victory = pygame.font.Font(None, 50)

# Player (triangle) properties
triangle_pos = [WIDTH // 2, HEIGHT - 40]
triangle_size = 20
lives = 3
score = 0

# Bomb properties
bomb_radius = 15
bombs = [[random.randint(bomb_radius, WIDTH - bomb_radius), random.randint(-HEIGHT, HEIGHT // 2)] for _ in range(5)]
bomb_speed = 4

# City names for victory messages
cities = ["Khan Younis", "Rafah", "Deir-Elbalah", "Jabalia", "Bait Lahia", "Gaza"]

# Game state variables
game_over = False
victory_message = ""
victory_timer = 0  # Timer to display victory messages

# Clock for frame rate control
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Game logic
    if not game_over:
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and triangle_pos[0] > triangle_size:
            triangle_pos[0] -= 5
        if keys[pygame.K_RIGHT] and triangle_pos[0] < WIDTH - triangle_size:
            triangle_pos[0] += 5

        # Draw background and score
        screen.fill(BLUE_SKY)
        score_surface = font_small.render(f'Score: {score}', True, BLACK)
        screen.blit(score_surface, (10, 10))
        lives_surface = font_small.render(f'Lives: {lives}', True, BLACK)
        screen.blit(lives_surface, (WIDTH - 100, 10))

        # Draw player triangle
        pygame.draw.polygon(screen, RED, [
            (triangle_pos[0], triangle_pos[1] - triangle_size),
            (triangle_pos[0] - triangle_size, triangle_pos[1] + triangle_size),
            (triangle_pos[0] + triangle_size, triangle_pos[1] + triangle_size),
        ])

        # Draw bombs and handle bomb movement and collision
        for bomb in bombs:
            pygame.draw.circle(screen, BLACK, (bomb[0], bomb[1]), bomb_radius)
            pygame.draw.circle(screen, RED, (bomb[0], bomb[1]), bomb_radius // 2)

            bomb[1] += bomb_speed  # Move bomb downwards

            # Check for bomb reaching the player
            if bomb[1] + bomb_radius > triangle_pos[1] and abs(bomb[0] - triangle_pos[0]) < triangle_size:
                lives -= 1
                bomb[1] = random.randint(-HEIGHT, -bomb_radius)
                if lives <= 0:
                    game_over = True

            # Reset bombs that fall off the screen
            if bomb[1] > HEIGHT:
                bomb[0] = random.randint(bomb_radius, WIDTH - bomb_radius)
                bomb[1] = random.randint(-HEIGHT, HEIGHT // 2)

        # Shoot line and update score on hitting bombs
        if keys[pygame.K_SPACE]:
            pygame.draw.line(screen, BLACK, (triangle_pos[0], triangle_pos[1]), (triangle_pos[0], 0), 2)

            for bomb in bombs:
                if abs(bomb[0] - triangle_pos[0]) < bomb_radius:
                    bomb[0] = random.randint(bomb_radius, WIDTH - bomb_radius)
                    bomb[1] = random.randint(-HEIGHT, HEIGHT // 2)
                    score += 1

                    # Display victory message at certain scores
                    if score % 25 == 0:
                        city_index = min(score // 25 - 1, len(cities) - 1)
                        victory_message = f"You liberated {cities[city_index]}!"
                        victory_timer = 120  # Display message for 2 seconds

        # Display victory message if timer is active
        if victory_timer > 0:
            victory_surface = font_victory.render(victory_message, True, BLACK)
            screen.blit(victory_surface, (WIDTH // 2 - victory_surface.get_width() // 2, HEIGHT // 2))
            victory_timer -= 1

    else:
        # Display Game Over screen with Restart and Quit buttons
        game_over_surface = font_large.render("Game Over", True, RED)
        screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - 50))

        # Restart and Quit buttons
        restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 50)
        quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)

        pygame.draw.rect(screen, GREEN, restart_button)
        pygame.draw.rect(screen, RED, quit_button)

        # Render text for buttons
        restart_text = font_small.render("Restart", True, WHITE)
        quit_text = font_small.render("Quit", True, WHITE)
        screen.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width()) // 2,
                                   restart_button.y + (restart_button.height - restart_text.get_height()) // 2))
        screen.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2,
                                quit_button.y + (quit_button.height - quit_text.get_height()) // 2))

        # Button functionality
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(mouse_x, mouse_y):
                lives = 3
                score = 0
                bombs = [[random.randint(bomb_radius, WIDTH - bomb_radius), random.randint(-HEIGHT, HEIGHT // 2)] for _ in range(5)]
                game_over = False
            elif quit_button.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                sys.exit()

    # Update display and maintain frame rate
    pygame.display.flip()
    clock.tick(60)
