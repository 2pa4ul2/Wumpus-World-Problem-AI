import pygame
import sys
import random
from trial.constants import *
from collections import deque

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

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return self.f < other.f

    def heuristic(self, goal):
        return abs(self.x - goal.x) + abs(self.y - goal.y)

    def bfs(self, board, start, goal):
        queue = deque([start])
        visited = set()

        while queue:
            current = queue.popleft()

            if current == goal:
                path = []
                while current:
                    path.append((current.x, current.y))
                    current = current.parent
                return path[::-1]

            visited.add(current)

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                x = current.x + dx
                y = current.y + dy

                if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT:
                    continue
                if board[y][x] == 1:
                    continue

                neighbor = Node(x, y, current)

                if neighbor in visited:
                    continue

                queue.append(neighbor)
                visited.add(neighbor)

        return None

class WumpusGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("15x8 Board with Pygame")

        # Initialize game variables
        self.char_pos = [0, 0]  # Default position of the character
        self.board_values = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.random_count = random.randint(5,8)

        # Generate game elements (gold, Wumpus, pits)
        self.gold_positions = self.generate_gold_positions(self.random_count)
        self.wumpus_positions = self.generate_wumpus_positions(self.random_count, self.gold_positions)
        self.pit_positions = self.generate_pit_positions(self.random_count, self.gold_positions)
        self.score = 0
        self.direction = (0, 1)  # Default direction
        
        # Initialize knowledge base
        self.knowledge_base = {
            "stench": set(),
            "breeze": set(),
            "glitter": set(),
            "safe": set(),
            "visited": set(),
            "pit": set(),
            "wumpus": set()
        }

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

    def check_game_over(self, x, y):
        if (x, y) in self.pit_positions or (x, y) in self.wumpus_positions:
            print("Game Over!")
            pygame.quit()
            sys.exit()

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

    def update_knowledge_base(self, percept):
        x, y = self.char_pos
        adjacent_cells = self.get_adjacent_cells(x, y)
        if percept == "stench":
            self.knowledge_base["stench"].add((x, y))
            for adj_x, adj_y in adjacent_cells:
                self.knowledge_base["wumpus"].add((adj_x, adj_y))
        elif percept == "breeze":
            self.knowledge_base["breeze"].add((x, y))
            for adj_x, adj_y in adjacent_cells:
                self.knowledge_base["pit"].add((adj_x, adj_y))
        elif percept == "glitter":
            self.knowledge_base["glitter"].add((x, y))
        self.knowledge_base["visited"].add((x, y))

    def infer_hazards(self):
        for x, y in self.knowledge_base["visited"]:
            if (x, y) not in self.knowledge_base["safe"]:
                if all(adj_cell not in self.knowledge_base["pit"] for adj_cell in self.get_adjacent_cells(x, y)):
                    self.knowledge_base["safe"].add((x, y))
            if (x, y) not in self.knowledge_base["visited"]:
                if all(adj_cell not in self.knowledge_base["wumpus"] for adj_cell in self.get_adjacent_cells(x, y)):
                    self.knowledge_base["safe"].add((x, y))

    def move_away_from_stench(self):
        x, y = self.char_pos
        adjacent_cells = self.get_adjacent_cells(x, y)
        possible_moves = []
        for adj_x, adj_y in adjacent_cells:
            if (adj_x, adj_y) not in self.knowledge_base["stench"]:
                possible_moves.append((adj_x - x, adj_y - y))  # Calculate the direction vector away from stench

        if possible_moves:
            # Choose a random direction away from stench
            dx, dy = random.choice(possible_moves)
            self.move_character(dx, dy)

    def move_away_from_breeze(self):
        x, y = self.char_pos
        adjacent_cells = self.get_adjacent_cells(x, y)
        possible_moves = []
        for adj_x, adj_y in adjacent_cells:
            if (adj_x, adj_y) not in self.knowledge_base["breeze"]:
                possible_moves.append((adj_x - x, adj_y - y))  # Calculate the direction vector away from breeze

        if possible_moves:
            # Choose a random direction away from breeze
            dx, dy = random.choice(possible_moves)
            self.move_character(dx, dy)

    def move_towards_wumpus(self):
        x, y = self.char_pos
        adjacent_cells = self.get_adjacent_cells(x, y)
        possible_moves = []
        for adj_x, adj_y in adjacent_cells:
            if (adj_x, adj_y) in self.knowledge_base["wumpus"]:
                possible_moves.append((adj_x - x, adj_y - y))  # Calculate the direction vector towards the Wumpus

        if possible_moves:
            # Choose a random direction towards the Wumpus
            dx, dy = random.choice(possible_moves)
            self.move_character(dx, dy)

    def move_away_from_wumpus(self):
        x, y = self.char_pos
        adjacent_cells = self.get_adjacent_cells(x, y)
        possible_moves = []
        for adj_x, adj_y in adjacent_cells:
            if (adj_x, adj_y) not in self.knowledge_base["wumpus"]:
                possible_moves.append((adj_x - x, adj_y - y))  # Calculate the direction vector away from the Wumpus

        if possible_moves:
            # Choose a random direction away from the Wumpus
            dx, dy = random.choice(possible_moves)
            self.move_character(dx, dy)

    def is_wumpus_clear(self):
        x, y = self.char_pos
        adjacent_cells = self.get_adjacent_cells(x, y)
        for adj_x, adj_y in adjacent_cells:
            if (adj_x, adj_y) in self.knowledge_base["wumpus"]:
                return False
        return True

    def main_loop(self):
        pygame_clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.gold_positions:  # Check if there is remaining gold
                start_node = Node(*self.char_pos)
                gold_nodes = [Node(*pos) for pos in self.gold_positions]
                shortest_path = None
                for goal_node in gold_nodes:
                    path = start_node.bfs(self.board_values, start_node, goal_node)
                    if path and (not shortest_path or len(path) < len(shortest_path)):
                        shortest_path = path

                if shortest_path and len(shortest_path) > 1:
                    next_pos = shortest_path[1]  # Skip the current position
                    dx = next_pos[0] - self.char_pos[0]
                    dy = next_pos[1] - self.char_pos[1]
                    self.move_character(dx, dy)
                    if tuple(self.char_pos) in self.gold_positions:
                        self.gold_positions.remove(tuple(self.char_pos))
                        self.score += 1000

            # Check for perception
            x, y = self.char_pos
            if (x, y) in self.gold_positions:
                self.update_knowledge_base("glitter")

            if self.check_pit_nearby(x, y):
                self.update_knowledge_base("breeze")

            if self.check_wumpus_nearby(x, y):
                self.update_knowledge_base("stench")

            # Decision-making based on perceptual cues and knowledge base
            if (x, y) in self.knowledge_base["stench"]:
                # Avoid moving towards stench
                self.move_away_from_stench()
            elif (x, y) in self.knowledge_base["breeze"]:
                # Avoid moving towards breeze
                self.move_away_from_breeze()
            elif (x, y) in self.knowledge_base["wumpus"]:
                # If the position of Wumpus is clear, move towards it to kill
                if self.is_wumpus_clear():
                    self.move_towards_wumpus()
                else:
                    # Otherwise, avoid moving towards the Wumpus
                    self.move_away_from_wumpus()
                
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

            # Infer hazards based on perceptual cues
            self.infer_hazards()

            # Introduce a delay to control the speed
            pygame_clock.tick(30)  # Adjust the value to control the speed

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = WumpusGame()
    game.main_loop()
