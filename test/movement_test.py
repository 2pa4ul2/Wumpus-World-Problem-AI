import pygame
import sys
import random
from states.constants import *


class WumpusGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("15x8 Board with Pygame")

        self.char_pos = [0, 0]
        self.board_values = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.random_count = random.randint(1,5)

        self.gold_positions = self.generate_gold_positions(self.random_count)
        self.wumpus_positions = self.generate_wumpus_positions(self.random_count, self.gold_positions)
        self.pit_positions = self.generate_pit_positions(self.random_count, self.gold_positions)
        self.score = 0
        self.direction = (0, 0)

    def move_character(self, dx, dy):
        new_x = self.char_pos[0] + dx
        new_y = self.char_pos[1] + dy
        if 0 <= new_x < BOARD_WIDTH and 0 <= new_y < BOARD_HEIGHT:
            self.char_pos = [new_x, new_y]
            if self.char_pos in self.wumpus_positions or self.char_pos in self.pit_positions:
                print("Game Over!")
                pygame.quit()
                sys.exit()
            elif self.char_pos in self.gold_positions:
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
            if (x,y) not in gold_positions and (x,y) != tuple(self.char_pos): #prevents the object from being placed on top of each other
                gold_positions.append((x, y))
        return gold_positions

    def generate_wumpus_positions(self, wumpus_monster, gold_positions):
        wumpus_positions = []
        for _ in range(wumpus_monster):
            while True:
                x = random.randint(0, BOARD_WIDTH - 1)
                y = random.randint(0, BOARD_HEIGHT - 1)
                if (x,y) not in gold_positions and (x,y) != tuple(self.char_pos): #prevents the object from being placed on top of each other
                    wumpus_positions.append((x, y))
                    break
        return wumpus_positions

    def generate_pit_positions(self, pit, gold_positions):
        pit_positions = []
        for _ in range(pit):
            while True:
                x = random.randint(0, BOARD_WIDTH - 1)
                y = random.randint(0, BOARD_HEIGHT - 1)
                if (x,y) not in gold_positions and (x,y) != tuple(self.char_pos): #prevents the object from being placed on top of each other
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

    def update_board_values(self, x, y, value):
        self.board_values[y][x] = value
        print(self.board_values)

    def spawn_gold(self, x, y):
        self.screen.blit(gold_img, (x * CELL_SIZE, y * CELL_SIZE))

    def spawn_wumpus(self, x, y):
        self.screen.blit(wumpus_img, (x * CELL_SIZE, y * CELL_SIZE))

    def spawn_pit(self, x, y):
        self.screen.blit(pit_img, (x * CELL_SIZE, y * CELL_SIZE))

    def spawn_character(self):
        if self.direction == (-1, 0):
            self.screen.blit(char_l, (self.char_pos[0] * CELL_SIZE, self.char_pos[1] * CELL_SIZE))
        elif self.direction == (1, 0):
            self.screen.blit(char_r, (self.char_pos[0] * CELL_SIZE, self.char_pos[1] * CELL_SIZE))
        elif self.direction == (0, -1):
            self.screen.blit(char_up, (self.char_pos[0] * CELL_SIZE, self.char_pos[1] * CELL_SIZE))
        elif self.direction == (0, 1):
            self.screen.blit(char_d, (self.char_pos[0] * CELL_SIZE, self.char_pos[1] * CELL_SIZE))



    def print_score(self):
        FONT = pygame.font.Font(None, 24)  
        score_text = f"Score: {self.score}"
        text_surface = FONT.render(score_text, True, BLACK)
        self.screen.blit(text_surface, (0, 0))

    def main_loop(self):
        running = True
        self.direction = (0, 1)  # The direction the character is facing
        ready_to_move = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.direction == (-1, 0):
                            self.char_pos[0] = max(0, self.char_pos[0] - 1)
                            ready_to_move = False
                            self.score -= 100
                        else:
                            self.direction = (-1, 0)
                            ready_to_move = True
                    elif event.key == pygame.K_RIGHT:
                        if self.direction == (1, 0):
                            self.char_pos[0] = min(BOARD_WIDTH - 1, self.char_pos[0] + 1)
                            ready_to_move = False
                            self.score -= 100
                        else:
                            self.direction = (1, 0)
                            ready_to_move = True
                    elif event.key == pygame.K_UP:
                        if self.direction == (0, -1):
                            self.char_pos[1] = max(0, self.char_pos[1] - 1)
                            ready_to_move = False
                            self.score -= 100
                        else:
                            self.direction = (0, -1)
                            ready_to_move = True
                    elif event.key == pygame.K_DOWN:
                        if self.direction == (0, 1) :
                            self.char_pos[1] = min(BOARD_HEIGHT - 1, self.char_pos[1] + 1)
                            ready_to_move = False
                            self.score -= 100
                        else:
                            self.direction = (0, 1)
                            ready_to_move = True
                    elif event.key == pygame.K_g:
                        if tuple(self.char_pos) in self.gold_positions:
                            self.gold_positions.remove(tuple(self.char_pos))
                            self.score += 1000
                            print(f"Score: {self.score}")
                    elif event.key == pygame.K_SPACE:
                        ball_pos = [self.char_pos[0] + self.direction[0], self.char_pos[1] + self.direction[1]]
                        if tuple(ball_pos) in self.wumpus_positions:
                            self.wumpus_positions.remove(tuple(ball_pos))
                            self.score += 1000
                            print(f"Score: {self.score}")

            self.draw_board()
            for pos in self.gold_positions:
                self.spawn_gold(*pos)
            for pos in self.wumpus_positions:
                self.spawn_wumpus(*pos)
            for pos in self.pit_positions:
                self.spawn_pit(*pos)
            self.spawn_character()
            self.print_score()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = WumpusGame()
    game.main_loop()
