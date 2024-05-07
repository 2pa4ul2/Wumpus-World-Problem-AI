    def generate_gold_positions(self, num_golds):
        gold_positions = []
        for _ in range(num_golds):
            x = random.randint(0, BOARD_WIDTH - 1)
            y = random.randint(0, BOARD_HEIGHT - 1)
            if (x,y) not in gold_positions and (x,y) != tuple(self.char_pos): #prevents the object from being placed on top of each other
                gold_positions.append((x, y))
        return gold_positions
