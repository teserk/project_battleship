import pygame


class Parameters:
    sizeofGrid = 10

    ship_size = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    FPS = 30
    windowwidth = 1000
    windowheight = 900
    tilesize = 32
    markersize = 32

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    PALE_GREEN = (0, 102, 0)
    GREEN = (0, 204, 0)
    GRAY = (40, 50, 60)
    BLUE = (0, 50, 255)
    YELLOW = (255, 255, 0)
    DARKGRAY = (40, 40, 40)

    first_player_board_pos = (10, 10)
    second_player_board_pos = (650, 10)

    popup_pos = (10, 350)

    window = pygame.display.set_mode((windowwidth, windowheight))
