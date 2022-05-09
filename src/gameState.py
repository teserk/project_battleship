from player import Player
from parameters import Parameters
from ship import Ship


class GameState:
    def __init__(self):
        self.first_player = Player("Первый игрок")
        self.second_player = Player("Второй игрок")
        self.status = "placing"
        self.queue = self.first_player        #игрок у которого сейчас ход
        self.defending = self.second_player   #игрок, который ждет хода
        self.popup = '{}, поставьте корабль'.format(self.queue.name)
        self.size_index = 0
        self.number_of_changes = 0
        self.waiting = 0

    def place_ship(self, size, pos, orientation):
        temp_ship = Ship(size, pos[0], pos[1], orientation)
        if self.validate_ship(temp_ship):
            self.queue.place_ship(temp_ship)
            self.queue.update_grid()
            self.size_index += 1

    def register_shoot(self, pos):
        if self.defending.grid.grid[pos[0]][pos[1]] == '+':
            if not self.defending.grid.check_neighbours([pos[0]][pos[1]]):
                self.popup = "Убил!"
                ...
            else:
                self.popup = "Попал!"
            self.queue.radar[pos[0]][pos[1]] = "x"
            self.defending.grid[pos[0]][pos[1]] = "x"
            return self.defending.grid.check_neighbours([pos[0]][pos[1]])
        return False

    def validate_ship(self, ship):
        if ship.orientation == 'V':
            if ship.y + ship.size > Parameters.sizeofGrid + 1:
                return False
            return self.queue.grid.check_neighbours(ship.x, ship.y)
        elif ship.orientation == 'H':
            if ship.x + ship.size > Parameters.sizeofGrid + 1:
                return False
            return self.queue.grid.check_neighbours(ship.x, ship.y)

    def change_queue(self):
        self.number_of_changes += 1
        self.queue, self.defending = self.defending, self.queue
        self.waiting = 1

    def update(self, pos, orientation):
        if self.waiting:
            self.popup = "Введите любую клавишу чтобы продолжить"
        if self.status == "placing":
            size = Parameters.ship_size[self.size_index]
            self.place_ship(size, pos, orientation=orientation)
            if self.size_index >= len(Parameters.ship_size):
                self.change_queue()
                self.size_index = 0
            self.popup = '{}, поставьте корабль'.format(self.queue.name)
            if self.number_of_changes == 2:
                self.status = "shooting"
        if self.status == "shooting":
            self.popup = '{}, стреляйте по своему радару!'.format(self.queue.name)
            if not self.register_shoot(pos):
                self.queue, self.defending = self.defending, self.queue
            if self.queue.isDead():
                self.popup = '{} ВЫИГРАЛ! ПОЗДРАВЛЯЕМ!!!'.format(self.defending.name)
                self.status = 'end'
            elif self.defending.isDead():
                self.popup = '{} ВЫИГРАЛ! ПОЗДРАВЛЯЕМ!!!'.format(self.queue.name)
                self.status = 'end'

