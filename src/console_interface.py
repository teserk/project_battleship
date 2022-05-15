import os
from parameters import Parameters
from gameState import GameState


class ConsoleInterface:
    def __init__(self):
        self.gameState = GameState()
        self.running = True
        self.shooting_coords = (None, None)
        self.orientation = 'H'
        self.numbers = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.letters = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")

    def draw_grid(self, grid, message):
        print(message)
        print("    A B C D E F G H I J")
        for row in range(1, len(grid) - 1):
            if row != len(grid) - 2:
                print(row, end=":  ")
            else:
                print(row, end=": ")
            for column in range(1, len(grid[row]) - 1):
                char = grid[column][row]
                if char == "empty":
                    char = "-"
                elif char == "ship":
                    char = "X"
                elif char == "marked":
                    char = "+"
                elif char == "checked":
                    char = "."
                print(char, end=" ")
            print("")
        print("")

    def show_popup(self):
        print(self.gameState.popup)

    def render(self):
        if self.gameState.pause:
            self.draw_grid(self.gameState.queue.grid.grid, "Ваше поле")
            self.draw_grid(self.gameState.queue.radar.grid, "Ваш радар")
        elif self.gameState.status == "placing" or self.gameState.status == "shooting":
            self.draw_grid(self.gameState.queue.grid.grid, "Ваше поле")
            self.draw_grid(self.gameState.defending.radar.grid, "Ваш радар")
        self.show_popup()

    def processInput(self):
        if self.gameState.pause:
            a = input("Введите любую клавишу чтобы продолжить: ")
            self.gameState.unset_pause()
            os.system('clear')
            return
        if self.gameState.status == "placing":
            coordinates = input("{}. введите координаты корабля в (формате A1): ".format(self.gameState.queue.name))
            while coordinates[1:] not in self.numbers or coordinates[0] not in self.letters:
                print("Некорректные координаты, попробуйте еще раз")
                coordinates = input("{}. введите координаты корабля в (формате A1): ".format(self.gameState.queue.name))
            x = self.letters.index(coordinates[0]) + 1
            y = int(coordinates[1:])
            self.shooting_coords = (x, y)
            self.orientation = input("{}, введите ориентацию корабля (H или V): ".format(self.gameState.queue.name))
            while self.orientation != 'V' and self.orientation != 'H':
                print('Неправильная ориентация, попробуйте еще раз')
                self.orientation = input("{}, введите ориентацию корабля (H или V): ".format(self.gameState.queue.name))
        elif self.gameState.status == "shooting":
            coordinates = input("{}. введите координаты стрельбы в (формате A1): ".format(self.gameState.queue.name))
            while coordinates[1:] not in self.numbers or coordinates[0] not in self.letters:
                print("Некорректные координаты, попробуйте еще раз")
                coordinates = input("{}. введите координаты стрельбы в (формате A1): ".format(self.gameState.queue.name))
            x = self.letters.index(coordinates[0]) + 1
            y = int(coordinates[1:])
            self.shooting_coords = (x, y)

    def update(self):
        if self.shooting_coords[0] is not None and not self.gameState.pause:
            self.gameState.update(self.shooting_coords, self.orientation)
            self.shooting_coords = (None, None)

    def run(self):
        while self.running:
            self.render()
            self.processInput()
            self.update()