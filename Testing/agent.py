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

# Place the rest of your code here

