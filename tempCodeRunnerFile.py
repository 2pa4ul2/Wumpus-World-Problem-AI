class Agent:
    def __init__(self):
        self.kb = {}  # Knowledge base

    def perceive(self, x, y, surroundings):
        # Update knowledge base based on perceptions
        self.kb[(x, y)] = surroundings
        for adj_x, adj_y, adj in surroundings:
            if 'Pit' in adj:
                self.update_kb(adj_x, adj_y, True)  # Mark the adjacent cell as unsafe if pit is detected

    def update_kb(self, x, y, is_safe):
        # Update knowledge base with inferred information
        self.kb[(x, y)] = {'Safe': is_safe}

    def make_decision(self, x, y, possible_moves):
        # Make decision based on knowledge base and available moves
        safe_moves = []
        for move in possible_moves:
            new_x = x + move[0]
            new_y = y + move[1]
            if (new_x, new_y) not in self.kb or not self.kb[(new_x, new_y)].get('Unsafe', False):
                safe_moves.append(move)
        if safe_moves:
            return random.choice(safe_moves)
        else:
            return (0, 0)  # If no safe move, stay in the same position