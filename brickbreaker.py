import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
PADDLE_SPEED = 5

# Ball settings
BALL_RADIUS = 10
BALL_SPEED = 3

# Brick settings
BRICK_WIDTH, BRICK_HEIGHT = 75, 20
BRICK_COLORS = [RED, GREEN, BLUE, YELLOW]

# Game variables
lives = 3
score = 0
level = 1
max_level = 10

# Font
font = pygame.font.Font(None, 36)

# Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = PADDLE_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def reset(self):
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2
        self.speed_x = BALL_SPEED
        self.speed_y = -BALL_SPEED

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0:
            self.speed_y = -self.speed_y
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x

    def reset(self):
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2
        self.speed_x = BALL_SPEED
        self.speed_y = -BALL_SPEED

# Brick class
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Powerup class
class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        if type == "expand":
            self.image = pygame.Surface((20, 20))
            self.image.fill(GREEN)
        elif type == "shrink":
            self.image = pygame.Surface((20, 20))
            self.image.fill(RED)
        elif type == "fast":
            self.image = pygame.Surface((20, 20))
            self.image.fill(BLUE)
        elif type == "slow":
            self.image = pygame.Surface((20, 20))
            self.image.fill(YELLOW)
        elif type == "tri-ball":
            self.image = pygame.Surface((20, 20))
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = 3

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Create game objects
paddle = Paddle()
ball = Ball()

all_sprites.add(paddle)
all_sprites.add(ball)

# Function to create bricks for a level
def create_bricks():
    brick_x = 10
    brick_y = 50
    for _ in range(8):
        for _ in range(10):
            brick_color = random.choice(BRICK_COLORS)
            brick = Brick(brick_x, brick_y, brick_color)
            all_sprites.add(brick)
            bricks.add(brick)
            brick_x += BRICK_WIDTH + 10
        brick_x = 10
        brick_y += BRICK_HEIGHT + 5

# Function to show level splash screen
def show_level_splash():
    level_text = font.render(f"Level {level}", True, WHITE)
    level_rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill(BLACK)
    screen.blit(level_text, level_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Function to show game over screen
def show_game_over_screen():
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    enter_name_text = font.render("Enter your name (3 letters):", True, WHITE)
    enter_name_rect = enter_name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    
    name = ""
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if len(name) < 3:
                        name += event.unicode.upper()
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                if event.key == pygame.K_RETURN and len(name) == 3:
                    save_high_score(name, score)
                    return
        
        screen.fill(BLACK)
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(enter_name_text, enter_name_rect)
        
        name_text = font.render(name, True, WHITE)
        name_rect = name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(name_text, name_rect)
        
        pygame.display.flip()

# Function to save high score
def save_high_score(name, score):
    with open("high_scores.txt", "a") as file:
        file.write(f"{name} {score}\n")

# Function to load high scores
def load_high_scores():
    high_scores = []
    try:
        with open("high_scores.txt", "r") as file:
            for line in file:
                name, score = line.strip().split()
                high_scores.append((name, int(score)))
    except FileNotFoundError:
        pass
    return high_scores

# Function to show high scores screen
def show_high_scores_screen():
    high_scores = load_high_scores()
    high_scores.sort(key=lambda x: x[1], reverse=True)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        
        screen.fill(BLACK)
        title_text = font.render("High Scores", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        y = 100
        for name, score in high_scores[:10]:
            score_text = font.render(f"{name}: {score}", True, WHITE)
            score_rect = score_text.get_rect(center=(WIDTH // 2, y))
            screen.blit(score_text, score_rect)
            y += 40
        
        pygame.display.flip()

# Function to show main menu
def show_main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_rect.collidepoint(event.pos):
                    return "new_game"
                elif high_scores_rect.collidepoint(event.pos):
                    show_high_scores_screen()
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()
        
        screen.fill(BLACK)
        title_text = font.render("Breakout Game", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_text, title_rect)
        
        new_game_text = font.render("New Game", True, WHITE)
        new_game_rect = new_game_text.get_rect(center=(WIDTH // 2, 250))
        screen.blit(new_game_text, new_game_rect)
        
        high_scores_text = font.render("High Scores", True, WHITE)
        high_scores_rect = high_scores_text.get_rect(center=(WIDTH // 2, 350))
        screen.blit(high_scores_text, high_scores_rect)
        
        quit_text = font.render("Quit Game", True, WHITE)
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, 450))
        screen.blit(quit_text, quit_rect)
        
        pygame.display.flip()

# Game loop
def game_loop():
    global lives, score, level
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        all_sprites.update()
        
        # Ball collisions
        if pygame.sprite.collide_rect(ball, paddle):
            ball.speed_y = -ball.speed_y
        
        brick_collisions = pygame.sprite.spritecollide(ball, bricks, True)
        for brick in brick_collisions:
            ball.speed_y = -ball.speed_y
            score += 10
            if random.random() < 0.1:
                powerup_type = random.choice(["expand", "shrink", "fast", "slow", "tri-ball"])
                powerup = Powerup(brick.rect.x, brick.rect.y, powerup_type)
                all_sprites.add(powerup)
                powerups.add(powerup)
        
        powerup_collisions = pygame.sprite.spritecollide(paddle, powerups, True)
        for powerup in powerup_collisions:
            if powerup.type == "expand":
                paddle.image = pygame.Surface((PADDLE_WIDTH * 2, PADDLE_HEIGHT))
                paddle.image.fill(WHITE)
                paddle.rect = paddle.image.get_rect(center=paddle.rect.center)
            elif powerup.type == "shrink":
                paddle.image = pygame.Surface((PADDLE_WIDTH // 2, PADDLE_HEIGHT))
                paddle.image.fill(WHITE)
                paddle.rect = paddle.image.get_rect(center=paddle.rect.center)
            elif powerup.type == "fast":
                ball.speed_x *= 2
                ball.speed_y *= 2
            elif powerup.type == "slow":
                ball.speed_x //= 2
                ball.speed_y //= 2
            elif powerup.type == "tri-ball":
                for _ in range(2):
                    new_ball = Ball()
                    new_ball.rect.centerx = ball.rect.centerx
                    new_ball.rect.centery = ball.rect.centery
                    new_ball.speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
                    new_ball.speed_y = -BALL_SPEED
                    all_sprites.add(new_ball)
        
        if ball.rect.bottom >= HEIGHT:
            lives -= 1
            if lives == 0:
                show_game_over_screen()
                lives = 3
                score = 0
                level = 1
                paddle.reset()
                ball.reset()
                for sprite in bricks:
                    sprite.kill()
                for sprite in powerups:
                    sprite.kill()
                if show_main_menu() == "new_game":
                    create_bricks()
                    show_level_splash()
                else:
                    return
            else:
                paddle.reset()
                ball.reset()
        
        if len(bricks) == 0:
            level += 1
            if level > max_level:
                show_game_over_screen()
                lives = 3
                score = 0
                level = 1
                paddle.reset()
                ball.reset()
                if show_main_menu() == "new_game":
                    create_bricks()
                    show_level_splash()
                else:
                    return
            else:
                create_bricks()
                show_level_splash()
        
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # Display lives
        for i in range(lives):
            heart_rect = pygame.Rect(10 + i * 30, 10, 20, 20)
            pygame.draw.rect(screen, RED, heart_rect)
            pygame.draw.polygon(screen, WHITE, [(heart_rect.left, heart_rect.bottom - 5),
                                                (heart_rect.centerx, heart_rect.top + 5),
                                                (heart_rect.right, heart_rect.bottom - 5)])
        
        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH - 150, 10))
        
        pygame.display.flip()
        clock.tick(60)

# Start the game
while True:
    if show_main_menu() == "new_game":
        create_bricks()
        show_level_splash()
        game_loop()
    else:
        break

pygame.quit()