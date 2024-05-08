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

            self.update_agent_movement(all_gold_collected, reached_original_pos, return_path)

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

    def update_agent_movement(self, all_gold_collected, reached_original_pos, return_path):
        # Update the agent's movement based on game conditions
        start_node = Node(*self.char_pos)
        if self.gold_positions:  # Check if there is remaining gold
            shortest_path = self.calculate_shortest_path(start_node, [Node(*pos) for pos in self.gold_positions])
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
                self.return_to_start_position(all_gold_collected, reached_original_pos, return_path)
        else:
            self.return_to_start_position(all_gold_collected, reached_original_pos, return_path)

    def calculate_shortest_path(self, start_node, goal_nodes):
        shortest_path = None
        for goal_node in goal_nodes:
            path = start_node.bfs(self.board_values, start_node, goal_node)  # Using BFS instead of A*
            if path and (not shortest_path or len(path) < len(shortest_path)):
                shortest_path = path
        return shortest_path

    def return_to_start_position(self, all_gold_collected, reached_original_pos, return_path):
        # Return to the starting position
        if not reached_original_pos:
            if not return_path:
                # If return path is not calculated yet, calculate it
                return_path = Node(*self.char_pos).bfs(self.board_values, Node(*self.char_pos), Node(*self.original_pos))
            if return_path:
                # If there is a return path, move towards the next cell in the path
                next_pos = return_path.pop(0)
                dx = next_pos[0] - self.char_pos[0]
                dy = next_pos[1] - self.char_pos[1]
                self.move_character(dx, dy)
                if tuple(self.char_pos) == self.original_pos:
                    print("You returned to the starting position!")
                    reached_original_pos = True  # Update the flag