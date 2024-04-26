import pygame
import random

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WUMPUS = (255, 0, 0)
GOLD = (255, 215, 0)
PIT = (128, 128, 128)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus World")

# Define grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player_pos = [0, 0]
wumpus_pos = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
pit_pos = [[random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)] for _ in range(3)]
gold_pos = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw grid
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Draw player
    pygame.draw.rect(screen, GREEN, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw wumpus
    pygame.draw.circle(screen, WUMPUS, (wumpus_pos[0] * CELL_SIZE + CELL_SIZE // 2, wumpus_pos[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    # Draw gold
    pygame.draw.circle(screen, GOLD, (gold_pos[0] * CELL_SIZE + CELL_SIZE // 2, gold_pos[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    # Draw pits
    for pit in pit_pos:
        pygame.draw.circle(screen, PIT, (pit[0] * CELL_SIZE + CELL_SIZE // 2, pit[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    pygame.display.flip()

pygame.quit()
