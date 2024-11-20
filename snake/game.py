"""
game.py

Contains the main logic for the Snake game. Handles player input, updates the game state,
renders the snake and apple, and checks for collisions. The game ends when the snake hits the wall or itself.
"""
import pygame
import random
from settings import (
    FONT_SIZE_SCORE, RES, SCORE_COLOR, SIZE, SNAKE_SPEED, AIM_SCORE,
    HALF_WIDTH, HALF_HEIGHT, FPS, FONT_SIZE_END, END_COLOR
)
from textures import BACKGROUND_IMG, SNAKE_HEAD_IMG, APPLE_IMG, SNAKE_BODY_IMG
from input_handler import handle_direction
def load_highscore():
    """
    Loads the highscore from a file. If the file doesn't exist, returns 0.
    """
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0
def save_highscore(highscore):
    """
    Saves the highscore to a file.
    """
    with open("highscore.txt", "w") as file:
        file.write(str(highscore))
def render_image(screen, snake, apple_pos, score):
    """
    Renders game elements: background, snake, and apple.
    """
    screen.blit(BACKGROUND_IMG, (0, 0))
    font_score = pygame.font.SysFont('Arial', FONT_SIZE_SCORE, bold=True)
    render_score = font_score.render(f'Score: {score}', True, SCORE_COLOR)
    screen.blit(render_score, (5, 5))
    [screen.blit(SNAKE_BODY_IMG, (i + 5, j + 5)) for i, j in snake[:-1]]
    screen.blit(SNAKE_HEAD_IMG, (snake[-1][0] + 5, snake[-1][1] + 5))
    screen.blit(APPLE_IMG, apple_pos)
def display_end_message(screen, message, score, highscore):
    """
    Displays the end game message, score, and highscore.
    """
    font_end = pygame.font.SysFont('Arial', FONT_SIZE_END, bold=True)
    font_score = pygame.font.SysFont('Arial', FONT_SIZE_SCORE, bold=True)

    render_message = font_end.render(message, True, END_COLOR)
    render_score = font_score.render(f'Score: {score}', True, SCORE_COLOR)
    render_highscore = font_score.render(f'Highscore: {highscore}', True,
                                         SCORE_COLOR)
    render_restart = font_score.render('Press SPACE to restart', True,
                                       SCORE_COLOR)
    screen.blit(BACKGROUND_IMG, (0, 0))
    screen.blit(render_message, (RES // 2 - 200, RES // 3))
    screen.blit(render_score, (RES // 2 - 200, RES // 3 + 100))
    screen.blit(render_highscore, (RES // 2 - 200, RES // 3 + 150))
    screen.blit(render_restart, (RES // 2 - 200, RES // 3 + 200))
    pygame.display.flip()
def snake_game(screen):
    """
    Main game loop, handles game state, rendering, and restarts.
    """
    x_position, y_position = random.randrange(SIZE, RES - SIZE, SIZE), random.randrange(SIZE,
                                                                      RES - SIZE,
                                                                      SIZE)
    apple_pos = random.randrange(SIZE, RES - SIZE, SIZE), random.randrange(
        SIZE, RES - SIZE, SIZE)
    length = 1
    snake = [(x_position, y_position)]
    score = 0
    dx, dy = 0, 0
    dirs = {'W': True, 'S': True, 'A': True, 'D': True}
    clock = pygame.time.Clock()
    # Load and initialize highscore
    highscore = load_highscore()
    iterations_counter = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        # Render game elements
        render_image(screen, snake, apple_pos, score)
        # Victory condition
        if score == AIM_SCORE:
            if score > highscore:
                highscore = score
                save_highscore(highscore)
            display_end_message(screen, "YOU WIN", score, highscore)
            return wait_for_restart()
        # Update snake position
        dx, dy, dirs = handle_direction(dx, dy, dirs)
        iterations_counter += 1
        if not iterations_counter % SNAKE_SPEED:
            x_position += dx * SIZE
            y_position += dy * SIZE
            snake.append((x_position, y_position))
            snake = snake[-length:]
        # Check for eating apple
        if snake[-1] == apple_pos:
            apple_pos = (random.randrange(SIZE, RES - SIZE, SIZE),
                         random.randrange(SIZE, RES - SIZE, SIZE))
            length += 1
            score += 1
        # Check for collision
        if x_position < 0 or x_position >= RES or y_position < 0 or y_position >= RES or len(snake) != len(
                set(snake)):
            if score > highscore:
                highscore = score
                save_highscore(highscore)
            display_end_message(screen, "YOU LOSE", score, highscore)
            return wait_for_restart()
        # Update screen
        screen.blit(screen, (HALF_WIDTH - RES // 2, HALF_HEIGHT - RES // 2))
        pygame.display.flip()
        clock.tick(FPS)
def wait_for_restart():
    """
    Waits for the player to press SPACE to restart or exits the game on quit.
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
