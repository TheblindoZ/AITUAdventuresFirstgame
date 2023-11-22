import pygame
import sys
import random
import sqlite3
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Initialize Pygame Mixer
pygame.mixer.init()
# SQLite database setup
conn = sqlite3.connect('game_records.db')
cursor = conn.cursor()

# Create a table to store game records
cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT,
        score INTEGER
    )
''')
conn.commit()

# Ask for the player's name before starting the game
player_name = input("Enter your name: ")

# Insert the player's name into the database
cursor.execute("INSERT INTO game_records (player_name, score) VALUES (?, ?)", (player_name, 0))
conn.commit()
# Define colors
WHITE = (255, 255, 255)

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Create window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AITU ADVENTURES Game")

# Add character images
character_images = [
    pygame.image.load("male_character.png"),
    pygame.image.load("female_character.png"),
]
# Load background music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.1)  # Adjust the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # -1 means play the music indefinitely

# Character selection variables
selected_character = 0  # Index of the selected character
character_selection_font = pygame.font.SysFont(None, 36)

# Text label for character selection
choose_character_font = pygame.font.SysFont(None, 48)

# Function to display the character selection menu
def display_character_selection():
    for i, character_image in enumerate(character_images):
        x = WIDTH // 2 - character_image.get_width() // 2
        y = HEIGHT // 2 - len(character_images) * 25 + i * 150
        window.blit(character_image, (x, y))

        # Highlight the selected character
        if i == selected_character:
            pygame.draw.rect(window, (0, 0, 255), (x - 10, y - 5, character_image.get_width() + 20, character_image.get_height() + 10), 2)

    pygame.display.flip()
background_image = pygame.image.load("Aitu2.png")
background_rect = background_image.get_rect()
# Character selection loop
character_selection = True

while character_selection:
    window.blit(background_image, background_rect)


    # Display "Choose Your Character" text
    choose_character_text = choose_character_font.render("Choose Your Character", True, (255,255,255))
    choose_character_x = WIDTH // 2 - choose_character_text.get_width() // 2
    choose_character_y = 50
    window.blit(choose_character_text, (choose_character_x, choose_character_y))

    display_character_selection()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                selected_character = (selected_character + 1) % len(character_images)
            elif event.key == K_UP:
                selected_character = (selected_character - 1) % len(character_images)
            elif event.key == K_RETURN:
                character_selection = False

# After character selection, proceed with the game loop

# Load selected character's map
if selected_character == 0:
    map_image = pygame.image.load("map1.jpg")
elif selected_character == 1:
    map_image = pygame.image.load("map2.jpg")

map_rect = map_image.get_rect()

# Generate random coordinates for items
item_images = [
    pygame.image.load("apple.png"),
    pygame.image.load("laptop.png"),
    pygame.image.load("book.png"),
    # Add more images as needed
]

item_positions = [(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20)) for _ in range(10)]
item_selected = [False] * len(item_positions)

# Load sounds
click_sound = pygame.mixer.Sound("click.mp3")
score_sound = pygame.mixer.Sound("click.mp3")

# Timer
timer_font = pygame.font.SysFont(None, 36)
time_remaining = 30

# Score
score_font = pygame.font.SysFont(None, 36)
score = 0

# Time tracking variable
last_time = pygame.time.get_ticks()

# Menu variables
menu_font = pygame.font.SysFont(None, 50)
menu_options = ["Start Game", "About Us", "Quit"]  # Add "About Us" option
selected_option = 0  # Index of the selected option

# About Us screen content
about_us_content = [
    "Welcome to the AITU ADVENTURES game!",
    "Rules: Choose your character and compete ",
    "compete with friends for time, find an ",
    "apple, book and laptop by clicking on the map.",
    "Have a good game!",
    "Creator - Omarzhanov Yerassyl",
    "Student of Astana IT University CS-2207",
]

# Define the font size for the menu and About Us
menu_font_size = 50
about_us_font_size = 35

# Function to display the menu or About Us screen
# Function to display the menu or About Us screen
def display_menu_or_about_us():
    window.fill(WHITE)

    if selected_option == 1:  # About Us
        for i, line in enumerate(about_us_content):
            # Increase the value below to shift the text downward
            y_offset = 65
            text = pygame.font.SysFont(None, about_us_font_size).render(line, True, (0, 0, 0))
            x = WIDTH // 2 - text.get_width() // 2
            y = HEIGHT // 2 - len(about_us_content) * 25 + i * about_us_font_size + y_offset
            window.blit(text, (x, y))
    else:  # Display menu
        for i, option in enumerate(menu_options):
            text = pygame.font.SysFont(None, menu_font_size).render(option, True, (0, 0, 0))
            x = WIDTH // 2 - text.get_width() // 2
            y = HEIGHT // 2 - len(menu_options) * 25 + i * menu_font_size
            window.blit(text, (x, y))

            # Highlight the selected option
            if i == selected_option:
                pygame.draw.rect(window, (0, 0, 255), (x - 10, y - 5, text.get_width() + 20, text.get_height() + 10), 2)

    pygame.display.flip()
# Function to display the game-over screen
def display_game_over_screen():
    window.fill(WHITE)

    # Display game-over text
    game_over_font = pygame.font.SysFont(None, 72)
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    game_over_x = WIDTH // 2 - game_over_text.get_width() // 2
    game_over_y = HEIGHT // 2 - game_over_text.get_height() // 2 - 50
    window.blit(game_over_text, (game_over_x, game_over_y))

    # Display final score
    final_score_font = pygame.font.SysFont(None, 48)
    final_score_text = final_score_font.render(f"Final Score: {score}", True, (0, 0, 0))
    final_score_x = WIDTH // 2 - final_score_text.get_width() // 2
    final_score_y = game_over_y + game_over_text.get_height() + 20
    window.blit(final_score_text, (final_score_x, final_score_y))

    # Display options
    options_font = pygame.font.SysFont(None, 36)
    restart_text = options_font.render("Press 'R' to Restart", True, (0, 0, 0))
    menu_text = options_font.render("Press 'M' to Return to Menu", True, (0, 0, 0))
    quit_text = options_font.render("Press 'Q' to Quit", True, (0, 0, 0))

    restart_x = WIDTH // 2 - restart_text.get_width() // 2
    menu_x = WIDTH // 2 - menu_text.get_width() // 2
    quit_x = WIDTH // 2 - quit_text.get_width() // 2

    restart_y = final_score_y + final_score_text.get_height() + 30
    menu_y = restart_y + 40
    quit_y = menu_y + 40

    window.blit(restart_text, (restart_x, restart_y))
    window.blit(menu_text, (menu_x, menu_y))
    window.blit(quit_text, (quit_x, quit_y))

    pygame.display.flip()

# Game state variable
in_menu = True

# Main game loop
clock = pygame.time.Clock()

while True:
    if in_menu:
        display_menu_or_about_us()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == K_RETURN:
                    if selected_option == 0:  # Start Game
                        in_menu = False
                        # Reset game variables
                        time_remaining = 30
                        score = 0
                        last_time = pygame.time.get_ticks()
                        item_positions = [(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20)) for _ in range(10)]
                        item_selected = [False] * len(item_positions)
                    elif selected_option == 1:  # About Us
                        # Display About Us screen
                        # (Note: You can add more information or graphics here)
                        pass
                    elif selected_option == 2:  # Quit
                        pygame.quit()
                        sys.exit()
                elif event.key == K_b:  # Check for 'B' key
                    in_menu = True

    else:
        # Main game loop
        window.fill(WHITE)

        # Draw map
        window.blit(map_image, map_rect)

        # Draw items
        for item_pos, item_image, selected in zip(item_positions, item_images, item_selected):
            if not selected:
                window.blit(item_image, item_pos)

        # Draw timer
        timer_text = timer_font.render(f"Time: {time_remaining}", True, (0, 0, 0))
        window.blit(timer_text, (10, 10))

        # Draw score
        score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
        window.blit(score_text, (10, 40))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # Check if an item was clicked
                for i, (item_pos, item_image) in enumerate(zip(item_positions, item_images)):
                    item_rect = pygame.Rect(item_pos, item_image.get_size())
                    if item_rect.collidepoint(event.pos) and not item_selected[i]:
                        score += 1
                        item_selected[i] = True
                        click_sound.play()  # Play the click sound

                        # Refill the array if the score is a multiple of 3
                        if score % 3 == 0 and score > 0:
                            item_positions = [(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20)) for _ in range(10)]
                            item_selected = [False] * len(item_positions)
                            score_sound.play()  # Play the score sound

        # Decrease the timer every second
        current_time = pygame.time.get_ticks()
        if current_time - last_time >= 1000:
            time_remaining -= 1
            last_time = current_time

        # Check if time is up
        if time_remaining <= 0:
            # When the game is over, update the player's score in the database
            cursor.execute("UPDATE game_records SET score = ? WHERE player_name = ?", (score, player_name))
            conn.commit()

            # Close the database connection
            conn.close()

            display_game_over_screen()
            while True:
                keys = pygame.key.get_pressed()

                if keys[K_r]:  # Restart
                    in_menu = False
                    # Reset game variables
                    time_remaining = 30
                    score = 0
                    last_time = pygame.time.get_ticks()
                    item_positions = [(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20)) for _ in
                                      range(10)]
                    item_selected = [False] * len(item_positions)
                    break  # Exit the loop to restart the game
                elif keys[K_m]:  # Return to menu
                    in_menu = True
                    break  # Exit the loop to return to the menu
                elif keys[K_q]:  # Quit
                    pygame.quit()
                    sys.exit()

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                clock.tick(60)


# Code that runs after the game is over (when time runs out)
print(f"Game over! Score: {score}")

# Quit Pygame
pygame.quit()
sys.exit()
