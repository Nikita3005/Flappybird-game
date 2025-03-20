import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 600
BIRD_SIZE = 20
COLUMN_WIDTH = 60
COLUMN_GAP = 150  # Space between pipes
GRAVITY = 0.4  # Lower gravity for smooth jump
JUMP_STRENGTH = -6  # Reduced jump power
SPEED = 3  # Slower speed for balanced gameplay
GROUND_HEIGHT = 120

# Colors
WHITE = (255, 255, 255)
CYAN = (135, 206, 250)
ORANGE = (255, 165, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load bird image
bird_img = pygame.image.load("bird.png")  # Ensure the file is in the same folder
bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE * 2, BIRD_SIZE * 2))  # Resize it

# Bird properties
bird = pygame.Rect(WIDTH // 3, HEIGHT // 2, BIRD_SIZE, BIRD_SIZE)
y_motion = 0
score = 0
game_over = False
started = False

# Columns
columns = []
scored_pipes = []  # Track pipes for scoring

def add_column():
    """Add a new pipe pair with a gap"""
    gap_y = random.randint(100, HEIGHT - COLUMN_GAP - GROUND_HEIGHT - 100)
    bottom_column = pygame.Rect(WIDTH, gap_y + COLUMN_GAP, COLUMN_WIDTH, HEIGHT - gap_y - COLUMN_GAP - GROUND_HEIGHT)
    top_column = pygame.Rect(WIDTH, 0, COLUMN_WIDTH, gap_y)
    columns.append((top_column, bottom_column))  # Store as pairs
    scored_pipes.append(False)  # Track if passed for scoring

# Initialize columns
for _ in range(1):
    add_column()

def reset_game():
    """Reset the game state"""
    global bird, y_motion, columns, score, game_over, started, scored_pipes
    bird = pygame.Rect(WIDTH // 3, HEIGHT // 2, BIRD_SIZE, BIRD_SIZE)
    y_motion = 0
    score = 0
    game_over = False
    started = False
    columns.clear()
    scored_pipes.clear()
    for _ in range(1):
        add_column()

def jump():
    """Make the bird jump"""
    global y_motion, started, game_over
    if game_over:
        reset_game()
    else:
        started = True
        y_motion = JUMP_STRENGTH  # Apply jump force

running = True
while running:
    screen.fill(CYAN)  # Background color
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            jump()
        if event.type == pygame.MOUSEBUTTONDOWN:
            jump()

    if started:
        # Apply gravity
        y_motion += GRAVITY
        bird.y += y_motion
        
        # Move columns
        for i in range(len(columns)):
            columns[i] = (columns[i][0].move(-SPEED, 0), columns[i][1].move(-SPEED, 0))  # Move both pipes in pair
        
        # Remove off-screen columns & add new ones
        if columns and columns[0][0].x + COLUMN_WIDTH < 0:
            columns.pop(0)
            scored_pipes.pop(0)
            add_column()

        # Collision Detection
        for top_pipe, bottom_pipe in columns:
            pygame.draw.rect(screen, GREEN, top_pipe)
            pygame.draw.rect(screen, GREEN, bottom_pipe)
            if bird.colliderect(top_pipe) or bird.colliderect(bottom_pipe):
                game_over = True
                started = False

        # Score Counting
        for i in range(len(columns)):
            top_pipe = columns[i][0]
            if top_pipe.x + COLUMN_WIDTH < bird.x and not scored_pipes[i]:
                score += 1  # Only increase score once per pipe pair
                scored_pipes[i] = True  # Mark as scored

        # Check ground & ceiling collision
        if bird.y >= HEIGHT - GROUND_HEIGHT - BIRD_SIZE or bird.y <= 0:
            game_over = True
            started = False

    # Draw ground
    pygame.draw.rect(screen, ORANGE, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))


   # Rotate the bird based on y_motion
    rotated_bird = pygame.transform.rotate(bird_img, -y_motion * 2)  # Tilts upwards when jumping
    screen.blit(rotated_bird, (bird.x, bird.y))

    
    # Display text
    font = pygame.font.SysFont("Arial", 40)
    if not started:
        message = font.render("Click to Start", True, WHITE)
        screen.blit(message, (WIDTH // 4, HEIGHT // 2))
    elif game_over:
        message = font.render("Game Over", True, WHITE)
        screen.blit(message, (WIDTH // 4, HEIGHT // 2))
    else:
        score_text = font.render(str(score), True, WHITE)
        screen.blit(score_text, (WIDTH // 2, 50))
    
    pygame.display.flip()
    clock.tick(30)  # Maintain frame rate

pygame.quit()
