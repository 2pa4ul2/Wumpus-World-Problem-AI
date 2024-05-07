import pygame
import sys
import random
import heapq
from trial.constants import *

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.f < other.f

    def heuristic(self, goal):
        return abs(self.x - goal.x) + abs(self.y - goal.y)

    def astar(self, board, start, goal):
        open_list = []
        closed_list = []

        heapq.heappush(open_list, (start.f, start))

        while open_list:
            current = heapq.heappop(open_list)[1]

            if current == goal:
                path = []
                while current:
                    path.append((current.x, current.y))
                    current = current.parent
                return path[::-1]

            closed_list.append(current)

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                x = current.x + dx
                y = current.y + dy

                if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT:
                    continue
                if board[y][x] == 1:
                    continue

                neighbor = Node(x, y, current)

                if neighbor in closed_list:
                    continue

                neighbor.g = current.g + 1
                neighbor.h = neighbor.heuristic(goal)
                neighbor.f = neighbor.g + neighbor.h

                if (neighbor.f, neighbor) in open_list:
                    continue

                heapq.heappush(open_list, (neighbor.f, neighbor))

        return None

class WumpusGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("15x8 Board with Pygame")

        self.char_pos = [0, 0]  # Default position of the character
        self.board_values = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.random_count = random.randint(5,5)

        self.gold_positions = self.generate_gold_positions(self.random_count)
        self.wumpus_positions = self.generate_wumpus_positions(self.random_count, self.gold_positions)
        self.pit_positions = self.generate_pit_positions(self.random_count, self.gold_positions)
        self.score = 0
        self.direction = (0, 1)  # Default direction

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
                if self.char_pos in self.gold_positions:
                    self.gold_positions.remove(tuple(self.char_pos))
                    if not self.gold_positions:
                        if tuple(self.char_pos) == (0, 0): 
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
        pygame_clock = pygame.time.Clock()
        running = True
        return_to_start = False  # Flag to indicate if the character is returning to start
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.gold_positions:  # Check if there is remaining gold
                start_node = Node(*self.char_pos)
                gold_nodes = [Node(*pos) for pos in self.gold_positions]
                shortest_path = None
                min_distance = float('inf')
                for goal_node in gold_nodes:
                    path = start_node.astar(self.board_values, start_node, goal_node)
                    if path and len(path) < min_distance:
                        shortest_path = path
                        min_distance = len(path)
                if shortest_path and len(shortest_path) > 1:
                    next_pos = shortest_path[1]  # Skip the current position
                    dx = next_pos[0] - self.char_pos[0]
                    dy = next_pos[1] - self.char_pos[1]
                    self.move_character(dx, dy)
                    if tuple(self.char_pos) in self.gold_positions:
                        self.gold_positions.remove(tuple(self.char_pos))
                        self.score += 1000
                        if not self.gold_positions:
                            return_to_start = True

            elif return_to_start:  # If all gold collected, return to start
                start_node = Node(*self.char_pos)
                start_to_start_path = start_node.astar(self.board_values, start_node, Node(0, 0))
                if start_to_start_path and len(start_to_start_path) > 1:
                    next_pos = start_to_start_path[1]  # Skip the current position
                    dx = next_pos[0] - self.char_pos[0]
                    dy = next_pos[1] - self.char_pos[1]
                    self.move_character(dx, dy)
                    if tuple(self.char_pos) == (0, 0):
                        print("You collected all the gold and returned to the start position! You win!")
                        pygame.quit()
                        sys.exit()

            # Update the display
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

            # Introduce a delay to control the speed
            pygame_clock.tick(5)  # Adjust the value to control the speed

        pygame.quit()
        sys.exit()




if __name__ == "__main__":
    game = WumpusGame()
    game.main_loop()
