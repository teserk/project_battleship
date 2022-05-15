from player import Player
from parameters import Parameters
from ship import Ship


class GameState:
    def __init__(self):
        self.first_player = Player("Первый игрок")
        self.second_player = Player("Второй игрок")
        self.status = "placing"
        self.queue = self.first_player  # игрок у которого сейчас ход
        self.defending = self.second_player  # игрок, который ждет хода
        self.popup = '{}, поставьте корабль'.format(self.queue.name)
        self.size_index = 0
        self.number_of_changes = 0
        self.pause = False

    def place_ship(self, size, pos, orientation):
        temp_ship = Ship(size, pos[0], pos[1], orientation)
        if self.validate_ship(temp_ship):
            self.queue.place_ship(temp_ship)
            self.queue.update_grid()
            self.size_index += 1

    def register_shoot(self, pos):
        if self.defending.grid.grid[pos[0]][pos[1]] == 'ship':
            if not self.defending.grid.have_neighbours(pos[0], pos[1]):
                self.popup = "Убил! Стреляйте ещё!"
            else:
                self.popup = "Попал! Стреляйте ещё!"
            self.queue.radar.grid[pos[0]][pos[1]] = 'marked'
            self.defending.grid.grid[pos[0]][pos[1]] = 'marked'
            return True
        self.queue.radar.grid[pos[0]][pos[1]] = 'checked'
        self.defending.grid.grid[pos[0]][pos[1]] = 'checked'
        return False

    def validate_ship(self, ship):
        if ship.orientation == 'V':
            if ship.y + ship.size > Parameters.sizeofGrid + 1:
                return False
            for i in range(ship.size):
                if self.queue.grid.have_neighbours(ship.x, ship.y + i):
                    return False
            return True
        elif ship.orientation == 'H':
            if ship.x + ship.size > Parameters.sizeofGrid + 1:
                return False
            for i in range(ship.size):
                if self.queue.grid.have_neighbours(ship.x + i, ship.y):
                    return False
            return True

    def change_queue(self):
        self.number_of_changes += 1
        self.queue, self.defending = self.defending, self.queue

    def set_pause(self):
        self.pause = True
        self.popup = "Нажмите на стрелку вправо чтобы сменить ход"

    def unset_pause(self):
        if not (self.popup == "Попал!" or self.popup == "Убил!"):
            self.change_queue()
        self.pause = False
        if self.status == "placing":
            self.popup = '{}, поставьте корабль'.format(self.queue.name)
        if self.number_of_changes >= 2:
            self.status = "shooting"
            self.popup = '{}, стреляйте по своему радару!'.format(self.queue.name)

    def update(self, pos, orientation):
        if self.status == "placing":
            if self.size_index >= len(Parameters.ship_size):
                self.set_pause()
                self.size_index = 0
                return
            self.popup = '{}, поставьте корабль'.format(self.queue.name)
            size = Parameters.ship_size[self.size_index]
            self.place_ship(size, pos, orientation=orientation)
            if self.size_index >= len(Parameters.ship_size):
                self.set_pause()
                self.size_index = 0
                return
        elif self.status == "shooting":
            self.popup = '{}, стреляйте по своему радару!'.format(self.queue.name)
            if not self.register_shoot(pos):
                self.set_pause()
            if self.queue.isDead():
                self.popup = '{} ВЫИГРАЛ! ПОЗДРАВЛЯЕМ!!!'.format(self.defending.name)
                self.status = 'end'
            elif self.defending.isDead():
                self.popup = '{} ВЫИГРАЛ! ПОЗДРАВЛЯЕМ!!!'.format(self.queue.name)
                self.status = 'end'
