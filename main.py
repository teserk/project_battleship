import os

# Пример доски для первого человека:
#    A B C D E F G H I J    (Думаю, лучше не использовать кириллицу для названия позиций)
# 1  + + + + - - - - - +
# 2  - - - - - - - - - +
# 3  - - X X - - - - - +
# 4  - - - - - - - - - -
# 5  - - X + + - - - - -
# 6  - - - - - - - X - X
# 7  - + + - - - - - - -
# 8  - - - - + - + - - -
# 9  - - - - - - - - - -
# 10 - - - - - - - - - -
# Будем обозначать пустые клетки символом "-", клетки с кораблями символом "X", клетки с попаданием "+"

sizeofGrid = 10

numbers = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
letters = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
ship_size = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]


class Grid:

    def __init__(self, name):
        """Нужно имя для каждой доски"""
        self.grid = [["-" for i in range(sizeofGrid + 2)]
                     for j in range(sizeofGrid + 2)]
        self.name = name

    def get_shot(self, another_player):
        print(another_player.name + ", сделайте выстрел")
        coordinates = input()

        if coordinates[1:] not in numbers or coordinates[0] not in letters:
            print("Некорректные координаты, попробуйте еще раз")
            self.get_shot(another_player)
        x = letters.index(coordinates[0]) + 1
        y = int(coordinates[1:])

        if self.grid[x][y] != "X":
            print("Мимо!")
            return

        if not self.check_neighbors(x, y):
            print("Убил!")
            self.grid[x][y] = "+"
            for i in range(-1, 2):
                for j in range(-1, 2):
                    another_player.grid[x + i][y + j] = "+"
            self.get_shot(another_player)
        else:
            print("Попал!")
            self.grid[x][y] = "+"
            another_player.grid[x][y] = "+"
            self.get_shot(another_player)

    def print_grid(self):
        print("    A B C D E F G H I J")
        for row in range(1, len(self.grid) - 1):
            if row != len(self.grid) - 2:
                print(row, end=":  ")
            else:
                print(row, end=": ")
            for column in range(1, len(self.grid[row]) - 1):
                print(self.grid[column][row], end=" ")
            print("")
        print("")

    def check_neighbors(self, x, y):  # вычисляет есть ли корабли в радиусе 1 вокруг точки
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.grid[x + i][y + j] == "X" and not (i == 0 and j == 0):
                    return True
        return False

    def win_condition(self, name):  # поиск элемента в поле
        for row in self.grid:
            if "X" in row:
                return False
        print(self.name + " выиграл! Игра окончена!")
        return True


class Ship:

    def __init__(self, size, name):

        """
        :param size: размер корабля
        :param coordinates: координаты в виде (буква)(цифра), например А1. Так как с таким форматом работать неудобно,
        переведем такие координаты в пару (x,y), где x, y от 1 до 10
        :param orientation: ориентация корабля:
                            horizontal - параллелен оси Ox
                            vertical - параллелен оси Oy
        """

        print(name + ", введите координаты и ориентацию корабля:")
        coordinates = input()
        orientation = input()

        if coordinates[1:] not in numbers or coordinates[0] not in letters:
            print("Некорректные координаты, попробуйте еще раз")
            self.__init__(size, name)
            return
        x = letters.index(coordinates[0]) + 1
        y = int(coordinates[1:])

        if orientation == 'horizontal' or orientation == 'vertical':
            self.orientation = orientation
        else:
            print("Некорректная ориентация, попробуйте еще раз")
            self.__init__(size, name)
            return

        if (orientation == 'horizontal' and x + size - 1 > sizeofGrid) \
                or (orientation == 'vertical' and y + size - 1 > sizeofGrid):
            print("Некорректная позиция или размер")
            self.__init__(size, name)
            return

        else:
            self.x = x
            self.y = y
            self.size = size

    def add_ship_to_grid(self, grid):

        """
        Добавляем корабль к полю
        :param grid: поле
        """

        if self.orientation == 'horizontal':
            for i in range(self.x, self.x + self.size):  # проверка на условие, что корабли не касаются друг друга
                if grid.check_neighbors(i, self.y):
                    print("Корабли не могут касаться друг друга!")
                    self.__init__(size, grid.name)
                    return
            for i in range(self.x, self.x + self.size):
                grid.grid[i][self.y] = "X"  # все норм, заполняем поле

        else:
            for i in range(self.y, self.y + self.size):  # проверка на условие, что корабли не касаются друг друга
                if grid.check_neighbors(self.x, i):
                    print("Корабли не могут касаться друг друга!")
                    self.__init__(size, grid.name)
                    return
            for i in range(self.y, self.y + self.size):
                grid.grid[self.x][i] = "X"  # все норм заполняем поле


if __name__ == "__main__":
    os.system("clear")
    First_player_grid = Grid("Первый игрок")
    First_player_radar = Grid("Первый игрок")
    Second_player_grid = Grid("Второй игрок")
    Second_player_radar = Grid("Второй игрок")

    for size in ship_size:  # сначала попросим ввести корабли первого игрока
        First_player_grid.print_grid()
        first_player_ship = Ship(size, First_player_grid.name)
        first_player_ship.add_ship_to_grid(First_player_grid)
        os.system("clear")

    for size in ship_size:  # сначала попросим ввести корабли первого игрока
        Second_player_grid.print_grid()
        second_player_ship = Ship(size, Second_player_grid.name)
        second_player_ship.add_ship_to_grid(Second_player_grid)
        os.system("clear")

    while True:
        print("(ваше поле)")
        First_player_grid.print_grid()
        print("(ваш радар)")
        First_player_radar.print_grid()
        Second_player_grid.get_shot(First_player_radar)

        print("Введите любую кнопку, чтобы закончить ход")
        pause_for_first_player = input()

        os.system("clear")

        if Second_player_grid.win_condition(First_player_grid.name):
            break

        print("(ваше поле)")
        Second_player_grid.print_grid()
        print("(ваш радар)")
        Second_player_radar.print_grid()
        First_player_grid.get_shot(Second_player_radar)

        print("Введите любую кнопку, чтобы закончить ход")
        pause_for_second_player = input()

        os.system("clear")

        if First_player_grid.win_condition(Second_player_grid.name):
            break

