import pygame


# Constants
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

WIDTH, HEIGHT = 700, 700
CELL_SIZE = 140
BOARD_WIDTH, BOARD_HEIGHT = 5, 5

tile_img = pygame.image.load("assets/tile3.jpg")
tile_img = pygame.transform.scale(tile_img, (CELL_SIZE, CELL_SIZE))

char_d = pygame.image.load("assets/character1-01.png")
char_d = pygame.transform.scale(char_d, (CELL_SIZE, CELL_SIZE))

char_up = pygame.image.load("assets/character1-02.png")
char_up = pygame.transform.scale(char_up, (CELL_SIZE, CELL_SIZE))

char_l = pygame.image.load("assets/character1-03.png")
char_l = pygame.transform.scale(char_l, (CELL_SIZE, CELL_SIZE))

char_r = pygame.image.load("assets/character1-04.png")
char_r = pygame.transform.scale(char_r, (CELL_SIZE, CELL_SIZE))



gold_img = pygame.image.load("assets/gold.png")
gold_img = pygame.transform.scale(gold_img, (CELL_SIZE, CELL_SIZE))

wumpus_img = pygame.image.load("assets/wumpus1.png")
wumpus_img = pygame.transform.scale(wumpus_img, (CELL_SIZE, CELL_SIZE))

pit_img = pygame.image.load("assets/hole.png")
pit_img = pygame.transform.scale(pit_img, (CELL_SIZE, CELL_SIZE))

cover_img = pygame.image.load("assets/wall_1.png")
cover_img = pygame.transform.scale(cover_img, (CELL_SIZE, CELL_SIZE))

glitter_img = pygame.image.load("assets/glitter.png")
stench_img = pygame.image.load("assets/stench.png")
breeze_img = pygame.image.load("assets/breeze.png")


start_img = pygame.image.load("assets/bg.jpeg")
start_img = pygame.transform.scale(start_img, (WIDTH, HEIGHT))

title_img = pygame.image.load("assets/title.png")
play_img = pygame.image.load("assets/start.png")
play_img = pygame.transform.scale(play_img, (WIDTH//4, HEIGHT//5.5))
exit_img = pygame.image.load("assets/exit.png")
exit_img = pygame.transform.scale(exit_img, (WIDTH//4, HEIGHT//5.5))