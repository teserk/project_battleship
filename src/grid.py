from parameters import Parameters


class Grid:
    def __init__(self):
        self.grid = [['empty' for i in range(Parameters.sizeofGrid + 2)]
                     for j in range(Parameters.sizeofGrid + 2)]

    def have_neighbours(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not i == j == 0:
                    if self.grid[x + i][y + j] == 'ship':
                        return True
        return False
