from grid import Grid
from parameters import Parameters
from ship import Ship


class Player:
    def __init__(self, name):
        self.name = name
        self.fleet = []
        self.grid = Grid()
        self.radar = Grid()
        if name == "Первый игрок":
            self.board_pos = Parameters.first_player_board_pos
        else:
            self.board_pos = Parameters.second_player_board_pos

    def place_ship(self, ship: Ship):
        self.fleet.append(ship)

    def isDead(self):
        if not self.fleet:
            return True
        return False

    def update_grid(self):
        for ship in self.fleet:
            for i in range(ship.size):
                if ship.orientation == 'H':
                    self.grid.grid[ship.x + i][ship.y] = '+'
                else:
                    self.grid.grid[ship.x][ship.y + i] = '+'
