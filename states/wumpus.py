import pygame
import sys
import random
from collections import deque
from constants import *
from agent import Agent

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
        return None

class WumpusGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("15x8 Board with Pygame")
        self.agent = Agent()
        # Initialize game variables
        self.char_pos = [0, 0]  # Default position of the character
        self.board_values = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]  # Initialize the matrix
        self.random_count = random.randint(4, 5)
        self.random_count_wumpus = random.randint(3, 4)
        self.random_count_pit = random.randint(2, 3)
        # Generate game elements (gold, Wumpus, pits)
        self.gold_positions = self.generate_gold_positions(self.random_count)
        self.wumpus_positions = self.generate_wumpus_positions(self.random_count_wumpus, self.gold_positions)
        self.pit_positions = self.generate_pit_positions(self.random_count_pit, self.gold_positions)
        self.score = 0
        self.direction = (0, 1)  # Default direction
        self.safe_positions = set()  # Store safe positions visited by the agent
        self.original_pos = tuple(self.char_pos)
        self.update_board_values()  # Update the board values initially

    def move_character(self, dx, dy):
        new_x = self.char_pos[0] + dx
        new_y = self.char_pos[1] + dy
        if 0 <= new_x < BOARD_WIDTH and 0 <= new_y < BOARD_HEIGHT:
            if (new_x, new_y) in self.wumpus_positions:
                print("You encountered a wumpus! You killed it!")
                self.wumpus_positions.remove((new_x, new_y))
                self.score -= 100  # Deduct points for killing the Wumpus
            elif (new_x, new_y) in self.pit_positions:
                print("You fell into a pit! Game Over!")
                pygame.quit()
                sys.exit()
            else:
                self.char_pos = [new_x, new_y]
                self.score -= 100
                self.safe_positions.add((new_x, new_y))
                if dx == 1:
                    self.direction = (1, 0)  # Moving right
                elif dx == -1:
                    self.direction = (-1, 0)  # Moving left
                elif dy == 1:
                    self.direction = (0, 1)  # Moving down
                elif dy == -1:
                    self.direction = (0, -1)  # Moving up
                if self.char_pos in self.gold_positions:
                    self.gold_positions.remove(tuple(self.char_pos))
                    if not self.gold_positions:
                        print("You collected all the gold! You win!")
                        pygame.quit()
                        sys.exit()
                if self.char_pos in self.original_pos:
                    print("You returned to the starting position!")
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
                if (x, y) not in gold_positions and (x, y) != tuple(self.char_pos) and not self.is_too_close_to_start(x, y):  # Prevents object from being placed on top of each other
                    pit_positions.append((x, y))
                    break
        return pit_positions

    def is_too_close_to_start(self, x, y):
        # Check if the specified position is too close to the start position
        start_x, start_y = self.char_pos
        return abs(x - start_x) <= 1 and abs(y - start_y) <= 1

    def draw_board(self):
        self.screen.fill(WHITE)
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                self.screen.blit(tile_img, (x * CELL_SIZE, y * CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            for pos in self.wumpus_positions:
                for adj in self.get_adjacent_cells(*pos):
                    scaled_stench_img = pygame.transform.scale(stench_img, (CELL_SIZE, CELL_SIZE))
                    self.screen.blit(scaled_stench_img, (adj[0] * CELL_SIZE, adj[1] * CELL_SIZE))
            for pos in self.gold_positions:
                for adj in self.get_adjacent_cells(*pos):
                    scaled_glitter_img = pygame.transform.scale(glitter_img, (CELL_SIZE, CELL_SIZE))
                    self.screen.blit(scaled_glitter_img, (adj[0] * CELL_SIZE, adj[1] * CELL_SIZE))
            for pos in self.pit_positions:
                for adj in self.get_adjacent_cells(*pos):
                    scaled_breeze_img = pygame.transform.scale(breeze_img, (CELL_SIZE, CELL_SIZE))
                    self.screen.blit(scaled_breeze_img, (adj[0] * CELL_SIZE, adj[1] * CELL_SIZE))
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

    def update_board_values(self):
        # Update the matrix based on game elements
        for pos in self.gold_positions:
            x, y = pos
            self.board_values[y][x] = "G"  # Represent gold
        for pos in self.wumpus_positions:
            x, y = pos
            self.board_values[y][x] = "W"  # Represent Wumpus
        for pos in self.pit_positions:
            x, y = pos
            self.board_values[y][x] = "P"  # Represent 
            
    def print_board(self):
        # Print the matrix representation of the game board
        for row in self.board_values:
            print(" ".join(str(cell) for cell in row))

    def print_board(self):
        symbols = {
            0: '.',  # Empty cell
            'P': 'P',  # Pit
            'G': 'G',  # Gold
            'W': 'W',  # Wumpus
            'C': 'C'   # Character
        }
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if (x, y) == tuple(self.char_pos):
                    print(symbols['C'], end=' ')
                else:
                    print(symbols[self.board_values[y][x]], end=' ')
            print()

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

    def shoot_ball(self, x, y):
        # Check if Wumpus is in the line of fire
        dx, dy = self.direction
        next_x, next_y = x + dx, y + dy
        iterations = 0  # Initialize the iteration counter
        while iterations < 5 and 0 <= next_x < BOARD_WIDTH and 0 <= next_y < BOARD_HEIGHT:
            if (next_x, next_y) in self.wumpus_positions:
                # Kill the Wumpus
                self.wumpus_positions.remove((next_x, next_y))
                self.score -= 500
                return True
            next_x += dx
            next_y += dy
            iterations += 1
        return False


    def main_loop(self):
        pygame_clock = pygame.time.Clock()
        running = True
        all_gold_collected = not self.gold_positions
        reached_original_pos = False  # Add a flag to track if the character reached the original position
        return_path = []  # Stores the path to return to the starting position
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_ai_movement(all_gold_collected, reached_original_pos, return_path)

            # Check for perception
            x, y = self.char_pos
            if (x, y) in self.gold_positions:
                print("You found gold!")
                self.gold_positions.remove((x, y))
                self.score += 100

            if self.check_pit_nearby(x, y):
                print("There's a pit nearby!")
                self.check_game_over(x, y)

            if self.check_wumpus_nearby(x, y):
                print("There's a Wumpus nearby!")
                if self.shoot_ball(x, y):  # Shoot a ball in the direction
                    print("You killed the Wumpus!")
                    self.score += 500

            # Update the display
            self.draw_board()
            self.print_board()
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

    def handle_ai_movement(self, all_gold_collected, reached_original_pos, return_path):
        if self.gold_positions:  # Check if there is remaining gold
            start_node = Node(*self.char_pos)
            gold_nodes = [Node(*pos) for pos in self.gold_positions]
            shortest_path = None
            for goal_node in gold_nodes:
                path = start_node.bfs(self.board_values, start_node, goal_node)  # Using BFS instead of A*
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
            elif shortest_path:
                print("Reached dead end. Backtracking...")
                prev_pos = shortest_path[-2]  # Get the second last position
                dx = prev_pos[0] - self.char_pos[0]
                dy = prev_pos[1] - self.char_pos[1]
                self.move_character(dx, dy)
            else:
                # Check if the character is at the original position
                if all_gold_collected and not reached_original_pos:
                    if not return_path:
                        # If return path is not calculated yet, calculate it
                        return_path = start_node.bfs(self.board_values, start_node, Node(*self.original_pos))
                    if return_path:
                        # If there is a return path, move towards the next cell in the path
                        next_pos = return_path.pop(0)
                        dx = next_pos[0] - self.char_pos[0]
                        dy = next_pos[1] - self.char_pos[1]
                        self.move_character(dx, dy)
                        if tuple(self.char_pos) == self.original_pos:
                            print("You returned to the starting position!")
                            reached_original_pos = True  # Update the flag
        else:
            # All gold collected, return to the starting position
            if not reached_original_pos:
                if not return_path:
                    # If return path is not calculated yet, calculate it
                    start_node = Node(*self.char_pos)
                    return_path = start_node.bfs(self.board_values, start_node, Node(*self.original_pos))
                if return_path:
                    # If there is a return path, move towards the next cell in the path
                    next_pos = return_path.pop(0)
                    dx = next_pos[0] - self.char_pos[0]
                    dy = next_pos[1] - self.char_pos[1]
                    self.move_character(dx, dy)
                    if tuple(self.char_pos) == self.original_pos:
                        print("You returned to the starting position!")
                        reached_original_pos = True  # Update the flag
