import random

class Agent:
    def __init__(self):
        self.knowledge_base = {}

    def perceive(self, cell):
        # Perceive the cell and update the knowledge base
        if cell.breeze:
            self.knowledge_base[cell] = 'breeze'
        elif cell.stench:
            self.knowledge_base[cell] = 'stench'
        elif cell.glitter:
            self.knowledge_base[cell] = 'glitter'
        else:
            self.knowledge_base[cell] = 'safe'

    def choose_next_cell(self):
        # Choose the next cell to move to based on the knowledge base
        for cell in self.knowledge_base:
            if self.knowledge_base[cell] == 'safe':
                return cell
        return None

    def move_to_cell(self, cell):
        # Move to the chosen cell and perceive it
        self.current_cell = cell
        self.perceive(cell)

    def update_kb(self, x, y, value):
        # Update knowledge base with inferred information
        self.kb[(x, y)] = value

    def make_decision(self, x, y, possible_moves):
        # Make decision based on knowledge base and available moves
        safe_moves = []
        for move in possible_moves:
            new_x = x + move[0]
            new_y = y + move[1]
            if (new_x, new_y) not in self.kb or 'Unsafe' not in self.kb[(new_x, new_y)]:
                safe_moves.append(move)
        if safe_moves:
            return random.choice(safe_moves)
        else:
            return (0, 0)  # If no safe move, stay in the same position
