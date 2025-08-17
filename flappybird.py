import pygame
import random

# Initialize Pygame
pygame.init()
gravity = 250
counter = 0
frame_counter = 0
score = 0

# Set up display
WIDTH, HEIGHT = 1024, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
pipe_img = pygame.image.load("pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (100, 350))
flipped_pipe = pygame.transform.flip(pipe_img, False, True)
  
bird_img = pygame.image.load("flappy.png")
bird_img = pygame.transform.scale(bird_img, (40, 40))

# Font for score
font = pygame.font.SysFont(None, 48)

# Pipe settings
PIPE_WIDTH = 100
PIPE_HEIGHT = 350
PIPE_GAP = 200
PIPE_SPEED = 7.5 
pipes = []

# Set up the clock (for frame rate)
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    frame_counter += 1  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                counter = 20  # Animate for 20 frames

    # Animate jump over 20 frames
    if counter > 0:
        gravity -= 4
        counter -= 1

    # Gravity (falling)
    gravity += 2

    if frame_counter % 60   == 0:
        pipes.append({
            "x": WIDTH + 100,
            "top_y": random.randint(-300, -150),
            "passed": False
        })

    # Draw background
    screen.fill((135, 206, 235))

    # Draw bird
    bird_rect = pygame.Rect(100, gravity, 75, 75)
    screen.blit(bird_img, bird_rect)

    # Stop game if bird flies off screen
    if gravity > HEIGHT or gravity < 0:
        running = False

    # Update and draw pipes
    new_pipes = []
    for pipe in pipes:
        pipe["x"] -= PIPE_SPEED
        x = pipe["x"]
        top_y = pipe["top_y"]
        bottom_y = top_y + PIPE_HEIGHT + PIPE_GAP

        top_rect = pygame.Rect(x, top_y, PIPE_WIDTH, PIPE_HEIGHT)
        bottom_rect = pygame.Rect(x, bottom_y, PIPE_WIDTH, PIPE_HEIGHT)

        # Draw pipes
        screen.blit(flipped_pipe, (x, top_y))
        screen.blit(pipe_img, (x, bottom_y))

        # Collision detection
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            running = False

        # Scoring
        if not pipe["passed"] and x + PIPE_WIDTH < 100:
            pipe["passed"] = True
            score += 1

        # Keep pipe if still on screen
        if x + PIPE_WIDTH > 0:
            new_pipes.append(pipe)
    pipes = new_pipes

    # Draw score
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    # Update display and tick clock
    pygame.display.flip()
    clock.tick(60) 