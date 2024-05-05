import pygame


# Constants
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

WIDTH, HEIGHT = 960, 640
CELL_SIZE = 80
BOARD_WIDTH, BOARD_HEIGHT = 5, 5

TILE_IMG = pygame.image.load("assets/tile3.jpg")
TILE_IMG = pygame.transform.scale(TILE_IMG, (CELL_SIZE, CELL_SIZE))

CHARACTER_IMG = pygame.image.load("assets/character1-01.png")
CHARACTER_IMG = pygame.transform.scale(CHARACTER_IMG, (CELL_SIZE, CELL_SIZE))

GOLD_IMG = pygame.image.load("assets/gold.png")
GOLD_IMG = pygame.transform.scale(GOLD_IMG, (CELL_SIZE, CELL_SIZE))

WUMPUS_IMG = pygame.image.load("assets/wumpus1.png")
WUMPUS_IMG = pygame.transform.scale(WUMPUS_IMG, (CELL_SIZE, CELL_SIZE))

PIT_IMG = pygame.image.load("assets/hole.png")
PIT_IMG = pygame.transform.scale(PIT_IMG, (CELL_SIZE, CELL_SIZE))