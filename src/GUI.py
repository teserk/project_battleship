import pygame
from gameState import GameState
from parameters import Parameters
from ship import Ship


class UserInterface:
    def __init__(self):
        self.gameState = GameState()
        self.running = True
        pygame.init()
        pygame.font.init()
        self.orientation = 'H'
        self.mouse_pos = (None, None)
        self.shooting_coords = (None, None)
        window = pygame.display.set_mode((Parameters.windowwidth, Parameters.windowheight))

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                if self.gameState.pause and event.key == pygame.K_RIGHT:
                    self.gameState.pause = False
                    self.shooting_coords = (None, None)
                    self.gameState.unset_pause()
            if self.gameState.pause:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.shooting_coords = self.get_square_under_mouse("place/shoot")
                    if self.shooting_coords[0] is not None:
                        self.shooting_coords = (self.shooting_coords[0] + 1, self.shooting_coords[1] + 1)
                elif event.button == 3:
                    if self.orientation == 'H':
                        self.orientation = 'V'
                    else:
                        self.orientation = 'H'

    def render(self):
        Parameters.window.fill(Parameters.GRAY)
        if self.gameState.pause:
            self.draw_grid(self.gameState.defending, self.gameState.queue.grid)
            self.draw_grid(self.gameState.queue, self.gameState.queue.radar)
        if self.gameState.status == 'placing':
            self.draw_grid(self.gameState.queue, self.gameState.queue.grid)
            self.draw_grid(self.gameState.defending, self.gameState.queue.radar)
        elif self.gameState.status == 'shooting':
            self.draw_grid(self.gameState.queue, self.gameState.queue.grid)
            self.draw_grid(self.gameState.defending, self.gameState.queue.radar)
        self.mouse_pos = self.get_square_under_mouse("render")
        if self.mouse_pos[0] is not None:
            self.render_tiles_on_mouse()
        self.show_popup()
        pygame.display.flip()

    def render_tiles_on_mouse(self):
        if self.gameState.status == "placing":
            temp_ship_for_render = Ship(Parameters.ship_size[self.gameState.size_index], self.mouse_pos[0] + 1,
                                        self.mouse_pos[1] + 1, orientation=self.orientation)
            try:
                if self.gameState.validate_ship(temp_ship_for_render):
                    color = Parameters.PALE_GREEN
                else:
                    color = (255, 0, 0, 50)
            except IndexError:
                color = (255, 0, 0, 50)
            if self.orientation == 'H':
                for i in range(Parameters.ship_size[self.gameState.size_index]):
                    rect = (1 + i * Parameters.tilesize + self.gameState.queue.board_pos[0] + self.mouse_pos[0]
                            * Parameters.tilesize,
                            1 + self.gameState.queue.board_pos[1] + self.mouse_pos[1] * Parameters.tilesize,
                            Parameters.tilesize - 2,
                            Parameters.tilesize - 2)
                    pygame.draw.rect(Parameters.window, color, rect)
            else:
                for i in range(Parameters.ship_size[self.gameState.size_index]):
                    rect = (1 + self.gameState.queue.board_pos[0] + self.mouse_pos[0] * Parameters.tilesize,
                            1 + i * Parameters.tilesize + self.gameState.queue.board_pos[1] + self.mouse_pos[1]
                            * Parameters.tilesize,
                            Parameters.tilesize - 2,
                            Parameters.tilesize - 2)
                    pygame.draw.rect(Parameters.window, color, rect)
        else:
            rect = (self.gameState.queue.board_pos[0] + self.mouse_pos[0] * Parameters.tilesize,
                    self.gameState.queue.board_pos[1] + self.mouse_pos[1] * Parameters.tilesize,
                    Parameters.tilesize,
                    Parameters.tilesize)
            pygame.draw.rect(Parameters.window, (255, 0, 0, 50), rect, 2)

    def update(self):
        if self.shooting_coords[0] is not None and not self.gameState.pause:
            self.gameState.update(self.shooting_coords, self.orientation)
            self.shooting_coords = (None, None)

    def run(self):
        while self.running:
            self.render()
            self.processInput()
            self.update()

    def get_square_under_mouse(self, purpose):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        if purpose == "render":
            mouse_pos -= self.gameState.queue.board_pos
        elif purpose == "place/shoot":
            if self.gameState.status == "placing":
                mouse_pos -= self.gameState.queue.board_pos
            elif self.gameState.status == "shooting":
                mouse_pos -= self.gameState.defending.board_pos
        x, y = [int(v // Parameters.tilesize) for v in mouse_pos]
        try:
            if x in range(Parameters.sizeofGrid) and y in range(Parameters.sizeofGrid):
                return x, y
            delta_tiles_x = self.gameState.second_player.board_pos[0] // Parameters.tilesize
            if purpose == "render" and x in range(delta_tiles_x, Parameters.sizeofGrid + delta_tiles_x) and \
                    y in range(Parameters.sizeofGrid):
                return x, y
        except IndexError:
            pass
        return None, None

    def show_popup(self):
        font1 = pygame.font.SysFont('Comic Sans MS', 48)
        text = font1.render(self.gameState.popup, False, Parameters.WHITE)
        Parameters.window.blit(text, Parameters.popup_pos)

    def draw_grid(self, player, board):
        for i in range(100):
            x = player.board_pos[0] + i % 10 * Parameters.tilesize
            y = player.board_pos[1] + i // 10 * Parameters.tilesize

            if board.grid[i % 10 + 1][i // 10 + 1] == 'empty':
                color = Parameters.WHITE
            elif board.grid[i % 10 + 1][i // 10 + 1] == 'ship':
                color = Parameters.GREEN
            elif board.grid[i % 10 + 1][i // 10 + 1] == 'marked':
                color = Parameters.DARKGRAY
            elif board.grid[i % 10 + 1][i // 10 + 1] == 'checked':
                color = Parameters.YELLOW
            else:
                color = Parameters.WHITE
            square = pygame.Rect(x, y, Parameters.tilesize, Parameters.tilesize)
            pygame.draw.rect(Parameters.window, color, square)
            pygame.draw.rect(Parameters.window, Parameters.BLACK, square, width=2)
