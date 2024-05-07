import pygame
import sys
import random
from collections import deque
from trial.constants import *  # Assuming constants are defined in constants.py

import numpy as np

# Constants
S = 0
B = 1
P = 2
W = 3
V = 4
G = 5

class Agent:
    def __init__(self, w_world, start_col, start_row):
        self.w_world = w_world
        self.c = start_col
        self.r = start_row
        self.direction = 'N'
        self.is_alive = True
        self.has_exited = False
        self.kb = np.zeros((w_world.world.shape[0], w_world.world.shape[1], 6), dtype=object)
        self.score = 0

        for i in range(self.kb.shape[0]):
            for j in range(self.kb.shape[1]):
                for k in range(self.kb.shape[2]):
                    self.kb[i][j][k] = ""

    def print_kb(self):
        for r in range(4):
            for c in range(4):
                for x in range(6):
                    print('{:>2},'.format(self.kb[r][c][x]), end='')
                print('\t', end='')
            print('\n')

    def loc(self):
        return np.array([self.c, self.r])

    def perceives(self):
        pos = self.loc()
        return self.w_world.cell(pos[0], pos[1])

    def adjacent(self):
        rows = self.w_world.world.shape[0]
        cols = self.w_world.world.shape[1]
        locations = []
        for row in [self.r - 1, self.r + 1]:
            if row > 0 and row < rows:
                locations.append([(row, self.c), self.w_world.cell(row, self.c)])
        for col in [self.c - 1, self.c + 1]:
            if col > 0 and col < cols:
                locations.append([(self.r, col), self.w_world.cell(self.r, col)])
        return locations

    def move(self, new_r, new_c):
        if new_r != self.r:
            if new_r < self.w_world.world.shape[0] and new_r > 0:
                self.r = new_r
        if new_c != self.c:
            if new_c < self.w_world.world.shape[1] and new_c > 0:
                self.c = new_c
        return 0

    def learn_from_pos(self):
        actual_components = self.perceives()
        self.kb[4 - self.r, self.c - 1][S] = ("S" if "S" in actual_components else "~S")
        self.kb[4 - self.r, self.c - 1][B] = ("B" if "B" in actual_components else "~B")
        self.kb[4 - self.r, self.c - 1][P] = ("P" if "P" in actual_components else "~P")
        self.kb[4 - self.r, self.c - 1][W] = ("W" if "W" in actual_components else "~W")
        self.kb[4 - self.r, self.c - 1][V] = ("V")
        self.kb[4 - self.r, self.c - 1][G] = ("G" if "G" in actual_components else "~G")

        for (nrow, ncol), _ in self.adjacent():
            if "S" in actual_components:
                if "~W" not in self.kb[4 - nrow, ncol - 1][W]:
                    self.kb[4 - nrow, ncol - 1][W] = "W?"
            else:
                self.kb[4 - nrow, ncol - 1][W] = "~W"

            if "B" in actual_components:
                if "~P" not in self.kb[4 - nrow, ncol - 1][P]:
                    self.kb[4 - nrow, ncol - 1][P] = "P?"
            else:
                self.kb[4 - nrow, ncol - 1][P] = "~P"

    def find_gold(self):
        path = []
        gold = False

        while not gold:
            print(f"Agent is on: {self.r}, {self.c}")

            self.learn_from_pos()
            path.append([self.r, self.c])
            self.print_kb()

            if 'G' in self.perceives():
                gold = True
                break

            next_xy = []

            for (x, y), _ in self.adjacent():
                if "~W" == self.kb[4 - x, y - 1][W]:
                    if "~P" == self.kb[4 - x, y - 1][P]:
                        if "V" != self.kb[4 - x, y - 1][V]:
                            next_xy = [x, y]
                            break

            if len(next_xy) > 0:
                self.move(next_xy[0], next_xy[1])
            else:
                path = path[:-1]
                self.move(path[-1][0], path[-1][1])

            print()

        print(path)

        return "path.... with score:" + str(self.score)

class WumpusGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("15x8 Board with Pygame")
        # Initialize game variables
        self.char_pos = [0, 0]  # Default position of the character
        self.board_values = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.random_count = random.randint(3, 5)
        # Generate game elements (gold, Wumpus, pits)
        self.gold_positions = self.generate_gold_positions(self.random_count)
        self.wumpus_positions = self.generate_wumpus_positions(self.random_count, self.gold_positions)
        self.pit_positions = self.generate_pit_positions(self.random_count, self.gold_positions)
        self.score = 0
        self.direction = (0, 1)  # Default direction
        # Initialize the agent
        self.agent = Agent(self.board_values, self.char_pos[0], self.char_pos[1])  # Pass the world representation



    def move_character(self, dx, dy):
        new_x = self.char_pos[0] + dx
        new_y = self.char_pos[1] + dy
        if 0 <= new_x < BOARD_WIDTH and 0 <= new_y < BOARD_HEIGHT:
            if (new_x, new_y) in self.wumpus_positions:
                print("You encountered a wumpus! Game Over!")
                pygame.quit()
                sys.exit()
            elif (new_x, new_y) in self.pit_positions:
                print("You fell into a pit! Game Over!")
                pygame.quit()
                sys.exit()
            else:
                self.char_pos = [new_x, new_y]
                self.score -= 100
                if self.char_pos in self.gold_positions:
                    self.gold_positions.remove(tuple(self.char_pos))
                    if not self.gold_positions:
                        print("You collected all the gold! You win!")
                        pygame.quit()
                        sys.exit()

    def get_adjacent_cells(self, x, y):
        adjacent_cells = []
        if y > 0:
            adjacent_cells.append((x, y - 1))  # Top
        if x < BOARD_WIDTH - 1:
            adjacent_cells.append((x + 1, y))  # Right
        if y < BOARD_HEIGHT - 1:
            adjacent_cells.append((x, y + 1))  # Bottom
        if x > 0:
            adjacent_cells.append((x - 1, y))  # Left
        return adjacent_cells

    def print_text(self, text, x, y, color=(0, 0, 0), size=24):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x * CELL_SIZE, y * CELL_SIZE))

    def generate_gold_positions(self, num_golds):
        gold_positions = []
        for _ in range(num_golds):
            x = random.randint(0, BOARD_WIDTH - 1)
            y = random.randint(0, BOARD_HEIGHT - 1)
            if (x, y) not in gold_positions and (x, y) != tuple(self.char_pos):  # Prevents object from being placed on top of each other
                gold_positions.append((x, y))
        return gold_positions

    def generate_wumpus_positions(self, wumpus_monster, gold_positions):
        wumpus_positions = []
        for _ in range(wumpus_monster):
            while True:
                x = random.randint(0, BOARD_WIDTH - 1)
                y = random.randint(0, BOARD_HEIGHT - 1)
                if (x, y) not in gold_positions and (x, y) != tuple(self.char_pos):  # Prevents object from being placed on top of each other
                    wumpus_positions.append((x, y))
                    break
        return wumpus_positions

    def generate_pit_positions(self, pit, gold_positions):
        pit_positions = []
        for _ in range(pit):
            while True:
                x = random.randint(0, BOARD_WIDTH - 1)
                y = random.randint(0, BOARD_HEIGHT - 1)
                if (x, y) not in gold_positions and (x, y) != tuple(self.char_pos):  # Prevents object from being placed on top of each other
                    pit_positions.append((x, y))
                    break
        return pit_positions

    def draw_board(self):
        self.screen.fill(WHITE)
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                self.screen.blit(tile_img, (x * CELL_SIZE, y * CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        for pos in self.wumpus_positions:
            for adj in self.get_adjacent_cells(*pos):
                self.print_text("Stench", *adj)
        for pos in self.gold_positions:
            for adj in self.get_adjacent_cells(*pos):
                self.print_text("glitter", *adj)
        for pos in self.pit_positions:
            for adj in self.get_adjacent_cells(*pos):
                self.print_text("breeze", *adj)
        self.spawn_character()

    def check_pit_nearby(self, x, y):
        adjacent_cells = self.get_adjacent_cells(x, y)
        for adj_x, adj_y in adjacent_cells:
            if (adj_x, adj_y) in self.pit_positions:
                return True
        return False

    def check_wumpus_nearby(self, x, y):
        adjacent_cells = self.get_adjacent_cells(x, y)
        for adj_x, adj_y in adjacent_cells:
            if (adj_x, adj_y) in self.wumpus_positions:
                return True
        return False

    def spawn_character(self):
        self.screen.blit(char_d, (self.char_pos[0] * CELL_SIZE, self.char_pos[1] * CELL_SIZE))

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_character(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_character(1, 0)
                    elif event.key == pygame.K_UP:
                        self.move_character(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.move_character(0, 1)

            self.draw_board()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = WumpusGame()
    game.play()
