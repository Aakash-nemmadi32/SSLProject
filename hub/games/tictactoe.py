<<<<<<< HEAD

from games.base_game_class import Game

=======
from games.base_game_class import Game
>>>>>>> dc28f013d8adb75ac8adffe4393b055f97b0a613
import numpy as np
import pygame
from sys import exit
import csv
from datetime import date
from numpy.lib.stride_tricks import sliding_window_view

pygame.init()

# color palette
Dark_blue = (20, 45, 50)
Blue_Grey = (35, 65, 75)
Neon_Blue = (0, 191, 255)
Neon_Yellow = (255, 255, 0)

font = pygame.font.Font("PressStart2P-Regular.ttf",30)
text = font.render("Player :",True,(0,255,200))


class TicTacToe(Game):

    def __init__(self, player1, player2, surface):
        super().__init__(player1, player2, surface)      
        CELL_SIZE = 50
        self.CELL_SIZE = 50
        self.SPACE = 6         # gap between cells
        self.height = 640
        self.width = 640
        self.STEP = self.CELL_SIZE + self.SPACE   # total distance from one cell to the next
        pygame.init()
        self.game_screen = pygame.Surface((self.width, self.height))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.START_X = 42      # left edge of the grid
        self.win_cells = []    # stores the 5 winning cells so we can draw the line
        self.START_Y = 63      # top edge of the grid
        self.game_over = False
        self.create_board(10, 10)
    
    def draw_board(self):    
        self.game_screen.fill(Dark_blue)

        # "Player :" label at the top
        font = pygame.font.Font("PressStart2P-Regular.ttf", 30)
        text = font.render("Player :", True, (0,255,200))
        self.game_screen.blit(text, (43, 20))

        # draw all 100 cell backgrounds
        for x in range(42, 547, 56):
            for y in range(62, 567, 56):
                pygame.draw.rect(self.game_screen, Blue_Grey, (x, y, 50, 50), 0, 3)

        # draw X or O on each occupied cell
        for r in range(10):
            for c in range(10):
                x_pos = self.START_X + c * self.STEP  
                y_pos = self.START_Y + r * self.STEP
                if self.board[r, c] == 1:
                    # player 1 is X — two diagonal lines
                    pygame.draw.line(self.game_screen, Neon_Blue, (x_pos + 2, y_pos + 2), (x_pos + 48, y_pos + 48), 2)
                    pygame.draw.line(self.game_screen, Neon_Blue, (x_pos + 2, y_pos + 48), (x_pos + 48, y_pos + 2), 2)
                elif self.board[r, c] == 2:
                    # player 2 is O — circle
                    pygame.draw.circle(self.game_screen, Neon_Yellow, (x_pos + 25, y_pos + 25), 22, 3)        

        # draw the winning line across the 5 matched cells
        if self.win_cells:
            win_color = Neon_Blue if self.board[self.win_cells[0][0], self.win_cells[0][1]] == 1 else Neon_Yellow
            r0, c0 = self.win_cells[0]
            r4, c4 = self.win_cells[-1]
            x0 = self.START_X + c0 * self.STEP + 25
            y0 = self.START_Y + r0 * self.STEP + 25
            x4 = self.START_X + c4 * self.STEP + 25
            y4 = self.START_Y + r4 * self.STEP + 25
            pygame.draw.line(self.game_screen, win_color, (x0, y0), (x4, y4), 4)
 
        # turn indicator — show X or O symbol next to "Player :"
        if self.current_player == 1:
            pygame.draw.line(self.game_screen, Neon_Blue, (285, 22), (315, 52), 3)
            pygame.draw.line(self.game_screen, Neon_Blue, (285, 52), (315, 22), 3)
        else:
            pygame.draw.circle(self.game_screen, Neon_Yellow, (295, 34), 15, 3)

        # menu button top-right corner
        pygame.draw.rect(self.game_screen, (200, 50, 50), (585, 5, 50, 30), 0, 4)
        font_small = pygame.font.Font("PressStart2P-Regular.ttf", 7)
        text_menu_btn = font_small.render("MENU", True, (255, 255, 255))
        self.game_screen.blit(text_menu_btn, (588, 13))            

        self.surface.blit(self.game_screen, (0, 0))

    def check_win(self, player):
        
        # check 5 in a row horizontally
        windows = sliding_window_view(self.board, 5, axis=1)
        match = np.argwhere(np.all(windows == player, axis=2))
        if len(match):
            r, c = match[0]
            self.win_cells = [(r, c+i) for i in range(5)]
            return True

        # check 5 in a row vertically
        windows = sliding_window_view(self.board, 5, axis=0)
        match = np.argwhere(np.all(windows == player, axis=2))
        if len(match):
            r, c = match[0]
            self.win_cells = [(r+i, c) for i in range(5)]
            return True

        # check 5 in a row diagonally (top-left to bottom-right)
        self.windows = sliding_window_view(self.board, (5, 5))
        match = np.argwhere(np.all(self.windows.diagonal(axis1=2, axis2=3) == player, axis=2))
        if len(match):
            r, c = match[0]
            self.win_cells = [(r+i, c+i) for i in range(5)]
            return True

        # check 5 in a row diagonally (top-right to bottom-left)
        match = np.argwhere(np.all(np.flip(self.windows, axis=3).diagonal(axis1=2, axis2=3) == player, axis=2))
        if len(match):
            r, c = match[0]
            self.win_cells = [(r+i, c+4-i) for i in range(5)]
            return True

        return False

    def position_in_table(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # check if menu button was clicked
                if self.menu_btn_rect.collidepoint(mx, my):
                    self.quit_to_menu = True
                    return None

                # figure out which cell was clicked
                for r in range(10):
                    for c in range(10):
                        valid_x_min_row = self.START_X + (c * (self.CELL_SIZE + self.SPACE))
                        valid_x_max_row = valid_x_min_row + self.CELL_SIZE
                        valid_y_min_col = self.START_Y + (r * (self.CELL_SIZE + self.SPACE))
                        valid_y_max_col = valid_y_min_col + self.CELL_SIZE
                        if valid_x_min_row < mx < valid_x_max_row and valid_y_min_col < my < valid_y_max_col:
                            return [r, c]
    
    def make_move(self):
        position = self.position_in_table()
        if position is None:
            return        # no click this frame
        
        r = position[0]
        c = position[1]

        if self.board[r, c] == 0:    # only place if the cell is empty
            self.board[r, c] = self.current_player
            if self.check_win(self.current_player):
                self.game_over = True
            elif not np.any(self.board == 0):   # board is full with no winner
                self.game_over = True
                self.is_draw = True     
            if not self.game_over:
                self.switch_turn()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:                
            self.draw_board()

            if self.quit_to_menu:       # user hit menu, don't save result
                return "Menu"

            if not self.game_over:
                self.make_move()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                if not self.result_saved:
                    # show final board for 1.5 seconds before wrapping up
                    self.draw_board()              
                    pygame.display.update()        
                    pygame.time.wait(1500)

                    if not self.is_draw:                
                        with open("history.csv", "a", newline="", encoding="utf-8-sig") as f:
                            writer = csv.writer(f)
                            if self.current_player == 1:
                                writer.writerow([self.player1, self.player2, self.today, "tictactoe"])
                            elif self.current_player == 2:
                                writer.writerow([self.player1, self.player2, self.today, "tictactoe"])    
                        self.result_saved = True 
                        running = False

                    if self.is_draw:
                        return "Draw"  
                    if self.current_player == 1:
                        return self.player1
                    elif self.current_player == 2:
                        return self.player2     
                                                      
            pygame.display.update() 
            clock.tick(60)

