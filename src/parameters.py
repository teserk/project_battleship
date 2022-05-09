import pygame


class Parameters:
    sizeofGrid = 10

    numbers = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
    letters = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
    ship_size = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    FPS = 30
    revealspeed = 8
    windowwidth = 1000
    windowheight = 900
    tilesize = 32
    markersize = 32

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 204, 0)
    GRAY = (40, 50, 60)
    BLUE = (0, 50, 255)
    YELLOW = (255, 255, 0)
    DARKGRAY = (40, 40, 40)

    first_player_board_pos = (10, 10)
    second_player_board_pos = (600, 10)
    first_player_radar_pos = (10, 350)
    second_player_radar_pos = (600, 350)

    popup_pos = (200, 800)

    window = pygame.display.set_mode((windowwidth, windowheight))
