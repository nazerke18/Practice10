import pygame
import random
import sys

pygame.init()

# -------------------- SETTINGS --------------------
CELL_SIZE = 20
COLS = 30
ROWS = 20
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 40)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
GRAY = (100, 100, 100)
BLUE = (50, 120, 255)

# Initial speed
speed = 8

# Walls (example obstacles)
walls = set()
for x in range(8, 12):
    walls.add((x, 6))
for y in range(10, 14):
    walls.add((18, y))


# -------------------- FUNCTIONS --------------------
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_walls():
    for wall in walls:
        rect = pygame.Rect(wall[0] * CELL_SIZE, wall[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BLUE, rect)


def random_food_position(snake):
    # Generate food position not on snake and not on wall
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake and pos not in walls:
            return pos


def draw_snake(snake):
    for i, part in enumerate(snake):
        rect = pygame.Rect(part[0] * CELL_SIZE, part[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if i == 0:
            pygame.draw.rect(screen, DARK_GREEN, rect)
        else:
            pygame.draw.rect(screen, GREEN, rect)


def draw_food(food):
    rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)


def show_text():
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))


def game_over():
    text1 = big_font.render("Game Over", True, WHITE)
    text2 = font.render("Press R to restart or Q to quit", True, WHITE)

    screen.fill(BLACK)
    screen.blit(text1, (WIDTH // 2 - 110, HEIGHT // 2 - 50))
    screen.blit(text2, (WIDTH // 2 - 150, HEIGHT // 2 + 10))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    return


def reset_game():
    global snake, direction, next_direction, food, score, level, speed
    snake = [(5, 5), (4, 5), (3, 5)]
    direction = (1, 0)
    next_direction = (1, 0)
    food = random_food_position(snake)
    score = 0
    level = 1
    speed = 8


# -------------------- GAME STATE --------------------
snake = [(5, 5), (4, 5), (3, 5)]
direction = (1, 0)
next_direction = (1, 0)

food = random_food_position(snake)
score = 0
level = 1

# -------------------- MAIN LOOP --------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Change direction with keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                next_direction = (1, 0)

    direction = next_direction

    # Calculate new head position
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # Border collision check
    if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
        game_over()
        reset_game()
        continue

    # Wall collision check
    if new_head in walls:
        game_over()
        reset_game()
        continue

    # Self collision check
    if new_head in snake:
        game_over()
        reset_game()
        continue

    # Move snake
    snake.insert(0, new_head)

    # Eat food
    if new_head == food:
        score += 1
        food = random_food_position(snake)

        # Level up every 4 points
        new_level = score // 4 + 1
        if new_level > level:
            level = new_level
            speed += 2
    else:
        snake.pop()

    # Draw everything
    screen.fill(BLACK)
    draw_grid()
    draw_walls()
    draw_snake(snake)
    draw_food(food)
    show_text()

    pygame.display.update()
    clock.tick(speed)