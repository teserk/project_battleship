import pygame
from gameState import GameState
from parameters import Parameters


class UserInterface:
    def __init__(self):
        self.gameState = GameState()
        self.running = True
        pygame.init()
        pygame.font.init()
        self.orientation = 'H'
        self.mouse_pos = (None, None)

    def processInput(self):
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_pos = self.get_square_under_mouse()
                if self.mouse_pos[0] is not None:
                    pos = (self.mouse_pos[0] + 1, self.mouse_pos[1] + 1)
                    self.gameState.update(pos, self.orientation)
            elif event.button == 3:
                if self.orientation == 'H':
                    self.orientation = 'V'
                else:
                    self.orientation = 'H'

    def draw_grid(self):
        for i in range(100):
            x = self.gameState.queue.board_pos[0] + i % 10 * Parameters.tilesize
            y = self.gameState.queue.board_pos[1] + i // 10 * Parameters.tilesize

            if self.gameState.queue.grid.grid[i % 10 + 1][i // 10 + 1] == '-':
                color = Parameters.WHITE
            elif self.gameState.queue.grid.grid[i % 10 + 1][i // 10 + 1] == '+':
                color = Parameters.GREEN
            elif self.gameState.queue.grid.grid[i % 10 + 1][i // 10 + 1] == 'x':
                color = Parameters.DARKGRAY
            square = pygame.Rect(x, y, Parameters.tilesize, Parameters.tilesize)
            pygame.draw.rect(Parameters.window, color, square)
            pygame.draw.rect(Parameters.window, Parameters.BLACK, square, width=2)

    def show_popup(self):
        font1 = pygame.font.SysFont('Comic Sans MS', 64)
        text = font1.render(self.gameState.popup, False, Parameters.GREEN)
        Parameters.window.blit(text, Parameters.popup_pos)

    def render(self):
        Parameters.window.fill(Parameters.GRAY)
        if self.gameState.status == 'placing':
            self.draw_grid()
        elif self.gameState.status == 'shooting':
            self.draw_grid()
        self.mouse_pos = self.get_square_under_mouse()
        if self.mouse_pos[0] is not None:
            rect = (self.gameState.queue.board_pos[0] + self.mouse_pos[0] * Parameters.tilesize,
                    self.gameState.queue.board_pos[1] + self.mouse_pos[1] * Parameters.tilesize,
                    Parameters.tilesize,
                    Parameters.tilesize)
            pygame.draw.rect(Parameters.window, (255, 0, 0, 50), rect, 2)
        self.show_popup()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.render()
            self.processInput()

    def get_square_under_mouse(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - self.gameState.queue.board_pos
        x, y = [int(v // Parameters.tilesize) for v in mouse_pos]
        try:
            if x >= 0 and y >= 0: return (x, y)
        except IndexError:
            pass
        return None, None
