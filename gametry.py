import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

WIDTH, HEIGHT = 1200, 800
CELL_SIZE = 100
BOARD_WIDTH, BOARD_HEIGHT = 12, 8

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


char_pos = [0, 0]
char_dir = 'right'  # Possible values: 'up', 'down', 'left', 'right'


# Create a 2D array to store values for each box
board_values = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

# Function to spawn the character at a specific coordinate
def spawn_character(screen, x, y):
    screen.blit(CHARACTER_IMG, (x * CELL_SIZE, y * CELL_SIZE))

def spawn_gold(screen, x, y):
    screen.blit(GOLD_IMG, (x * CELL_SIZE, y * CELL_SIZE))

def spawn_wumpus(screen, x, y):
    screen.blit(WUMPUS_IMG, (x * CELL_SIZE, y * CELL_SIZE))

def spawn_pit(screen, x, y):
    screen.blit(PIT_IMG, (x * CELL_SIZE, y * CELL_SIZE))

# Function to generate random coordinates for gold
def generate_gold_positions(num_golds):
    gold_positions = []
    for _ in range(num_golds):
        x = random.randint(0, BOARD_WIDTH - 1)
        y = random.randint(0, BOARD_HEIGHT - 1)
        gold_positions.append((x, y))
    return gold_positions

def generate_wumpus_positions(wumpus_monster, gold_positions):
    wumpus_positions = []
    for _ in range(wumpus_monster):
        while True:
            x = random.randint(0, BOARD_WIDTH - 1)
            y = random.randint(0, BOARD_HEIGHT - 1)
            if (x, y) not in gold_positions:
                wumpus_positions.append((x, y))
                break
    return wumpus_positions


def generate_pit_positions(pit, gold_positions):
    pit_positions = []
    for _ in range(pit):
        while True:
            x = random.randint(0, BOARD_WIDTH - 1)
            y = random.randint(0, BOARD_HEIGHT - 1)
            if (x, y) not in gold_positions:
                pit_positions.append((x, y))
                break
    return pit_positions

# Function to draw the board and display the values
def draw_board(screen):
    screen.fill(WHITE)
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            screen.blit(TILE_IMG, (x * CELL_SIZE, y * CELL_SIZE)) #print image on tiles
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1) #Draw borders

# Function to update the board values
def update_board_values(x, y, value):
    board_values[y][x] = value
    print(board_values)

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("15x8 Board with Pygame")

# Generate gold positions
    gold_positions = generate_gold_positions(10)
    # Generate Wumpus positions
    wumpus_positions = generate_wumpus_positions(10, gold_positions)
    pit_positions = generate_pit_positions(5, gold_positions)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Move left
                    char_pos[0] = max(0, char_pos[0] - 1)
                elif event.key == pygame.K_RIGHT:
                    # Move right
                    char_pos[0] = min(BOARD_WIDTH - 1, char_pos[0] + 1)
                elif event.key == pygame.K_UP:
                    # Move up
                    char_pos[1] = max(0, char_pos[1] - 1)
                elif event.key == pygame.K_DOWN:
                    # Move down
                    char_pos[1] = min(BOARD_HEIGHT - 1, char_pos[1] + 1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the x, y position of the mouse click
                x, y = pygame.mouse.get_pos()
                # Convert the x, y position to board coordinates
                board_x, board_y = x // CELL_SIZE, y // CELL_SIZE
                # Update the board values
                update_board_values(board_x, board_y, 1)

        draw_board(screen)
        for pos in gold_positions:
            spawn_gold(screen, *pos)
        for pos in wumpus_positions:
            spawn_wumpus(screen, *pos)
        for pos in pit_positions:
            spawn_pit(screen, *pos)
        spawn_character(screen,*char_pos)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()



#LIST OF NEEDS FOR THE GAME
    #Assets
        # Main Floor
        # Wumpus Floor
        # Wumpus image
        # Gold image
        # Pit image
        # Player image
    #
    #
    #
    #
    #