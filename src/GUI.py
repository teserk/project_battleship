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
        elif event.type == pygame.MOUSEBUTTONDOWN:
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

    def render(self):
        Parameters.window.fill(Parameters.GRAY)
        if self.gameState.waiting:
            self.draw_grid(self.gameState.defending, self.gameState.queue.grid)
            self.draw_grid(self.gameState.queue, self.gameState.queue.radar)
        if self.gameState.status == 'placing':
            self.draw_grid(self.gameState.queue, self.gameState.queue.grid)
            self.draw_grid(self.gameState.defending, self.gameState.queue.radar)
        elif self.gameState.status == 'shooting':
            self.draw_grid(self.gameState.queue, self.gameState.queue.grid)
            self.draw_grid(self.gameState.defending, self.gameState.queue.radar)
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
            if x >= 0 and y >= 0:
                return x, y
        except IndexError:
            pass
        return None, None

    def show_popup(self):
        font1 = pygame.font.SysFont('Comic Sans MS', 64)
        text = font1.render(self.gameState.popup, False, Parameters.GREEN)
        Parameters.window.blit(text, Parameters.popup_pos)

    def draw_grid(self, player, board):
        for i in range(100):
            x = player.board_pos[0] + i % 10 * Parameters.tilesize
            y = player.board_pos[1] + i // 10 * Parameters.tilesize

            if board.grid[i % 10 + 1][i // 10 + 1] == '-':
                color = Parameters.WHITE
            elif board.grid[i % 10 + 1][i // 10 + 1] == '+':
                color = Parameters.GREEN
            elif board.grid[i % 10 + 1][i // 10 + 1] == 'x':
                color = Parameters.DARKGRAY
            else:
                color = Parameters.WHITE
            square = pygame.Rect(x, y, Parameters.tilesize, Parameters.tilesize)
            pygame.draw.rect(Parameters.window, color, square)
            pygame.draw.rect(Parameters.window, Parameters.BLACK, square, width=2)
