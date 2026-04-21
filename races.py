import pygame
import random
import sys

pygame.init()

# -------------------- SETTINGS --------------------
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
YELLOW = (255, 215, 0)
BLUE = (50, 120, 255)

# Road settings
ROAD_LEFT = 80
ROAD_RIGHT = 320
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

# Game variables
enemy_speed = 6
coin_count = 0
score = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 40)

# Event for increasing difficulty
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 5000)


# -------------------- CLASSES --------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create player car as a simple rectangle surface
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
        pygame.draw.rect(self.image, BLUE, (0, 0, 40, 70), border_radius=8)
        pygame.draw.rect(self.image, BLACK, (5, 8, 30, 15), border_radius=4)
        pygame.draw.circle(self.image, BLACK, (8, 12), 5)
        pygame.draw.circle(self.image, BLACK, (32, 12), 5)
        pygame.draw.circle(self.image, BLACK, (8, 58), 5)
        pygame.draw.circle(self.image, BLACK, (32, 58), 5)

        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)

    def move(self):
        keys = pygame.key.get_pressed()

        # Move left/right inside the road only
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.move_ip(-6, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.move_ip(6, 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create enemy car
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RED, (0, 0, 40, 70), border_radius=8)
        pygame.draw.rect(self.image, BLACK, (5, 8, 30, 15), border_radius=4)
        pygame.draw.circle(self.image, BLACK, (8, 12), 5)
        pygame.draw.circle(self.image, BLACK, (32, 12), 5)
        pygame.draw.circle(self.image, BLACK, (8, 58), 5)
        pygame.draw.circle(self.image, BLACK, (32, 58), 5)

        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        # Random x position inside the road
        x = random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 20)
        self.rect.center = (x, -50)

    def move(self):
        global score
        self.rect.move_ip(0, enemy_speed)

        # If enemy leaves screen, move it back to top and increase score
        if self.rect.top > SCREEN_HEIGHT:
            score += 1
            self.reset_position()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Coin surface
        self.image = pygame.Surface((22, 22), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (11, 11), 10)
        pygame.draw.circle(self.image, BLACK, (11, 11), 10, 2)

        self.rect = self.image.get_rect()
        self.active = False
        self.spawn_delay = random.randint(40, 120)

    def spawn(self):
        # Spawn coin at random road position
        x = random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 20)
        y = random.randint(-300, -50)
        self.rect.center = (x, y)
        self.active = True

    def move(self):
        # Randomly make the coin appear
        if not self.active:
            self.spawn_delay -= 1
            if self.spawn_delay <= 0:
                self.spawn()
            return

        self.rect.move_ip(0, enemy_speed)

        # If coin leaves screen, deactivate and prepare next spawn
        if self.rect.top > SCREEN_HEIGHT:
            self.active = False
            self.spawn_delay = random.randint(40, 120)


# -------------------- FUNCTIONS --------------------
def draw_road():
    # Fill background with grass
    screen.fill(GREEN)

    # Draw road
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

    # Draw side lines
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, SCREEN_HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_HEIGHT), 4)

    # Draw center dashed line
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 5, y, 10, 25))


def game_over_screen():
    text1 = font_big.render("Game Over", True, WHITE)
    text2 = font_small.render("Press R to restart or Q to quit", True, WHITE)

    screen.fill(RED)
    screen.blit(text1, (100, 220))
    screen.blit(text2, (55, 280))
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
                if event.key == pygame.K_r:
                    return


def reset_game():
    global enemy_speed, coin_count, score
    enemy_speed = 6
    coin_count = 0
    score = 0
    player.rect.center = (200, 520)
    enemy.reset_position()
    coin.active = False
    coin.spawn_delay = random.randint(40, 120)


# -------------------- OBJECTS --------------------
player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy)

# -------------------- MAIN LOOP --------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Increase speed over time
        if event.type == INC_SPEED:
            enemy_speed += 0.5

    # Move player and game objects
    player.move()
    enemy.move()
    coin.move()

    # Check coin collection
    if coin.active and player.rect.colliderect(coin.rect):
        coin_count += 1
        coin.active = False
        coin.spawn_delay = random.randint(40, 120)

    # Check collision with enemy
    if player.rect.colliderect(enemy.rect):
        game_over_screen()
        reset_game()

    # Draw everything
    draw_road()

    # Draw sprites
    screen.blit(enemy.image, enemy.rect)
    if coin.active:
        screen.blit(coin.image, coin.rect)
    screen.blit(player.image, player.rect)

    # Draw score at top left
    score_text = font_small.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Draw coin counter at top right
    coin_text = font_small.render(f"Coins: {coin_count}", True, BLACK)
    coin_rect = coin_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    screen.blit(coin_text, coin_rect)

    pygame.display.update()
    clock.tick(FPS)