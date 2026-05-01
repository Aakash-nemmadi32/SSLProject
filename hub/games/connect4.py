
from games.base_game_class import Game

import numpy as np
import pygame
from sys import exit
import csv
from datetime import date
from numpy.lib.stride_tricks import sliding_window_view

class connect4(Game):

    def __init__(self, player1, player2, surface,n):
        super().__init__(player1, player2, surface,n)
        self.width = 640
        self.height = 640
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

        # piece and board colors
        self.player1_color = (255, 80, 20)    # orange
        self.player2_color = (255, 220, 50)   # yellow
        self.BOARD_COLOR   = (80, 20, 60)     # dark purple

        self.Game_Screen = pygame.Surface((self.width, self.height))
        self.create_board(7, 7)

        # grid layout
        self.X_start = 50
        self.y_start = 70
        self.RADIUS  = 30    # size of each piece
        self.SPACE   = 18    # gap between pieces

    def draw_board(self):
        self.Game_Screen.fill(self.BOARD_COLOR)

        # "Player :" label at the top
        font = pygame.font.Font("PressStart2P-Regular.ttf", 45)
        text = font.render("Player :", True, (0, 255, 200))
        self.Game_Screen.blit(text, (20, 18))

        # draw all 49 cells — empty hole, player1, or player2
        for r in range(7):
            for c in range(7):
                d = self.X_start + self.RADIUS + c * (2 * self.RADIUS + self.SPACE)
                e = self.y_start + self.RADIUS + r * (2 * self.RADIUS + self.SPACE)
                if self.board[r, c] == 0:
                    pygame.draw.circle(self.Game_Screen, (40, 10, 30), (d, e), self.RADIUS, 0)   # empty slot
                if self.board[r, c] == 1:                              
                    pygame.draw.circle(self.Game_Screen, self.player1_color, (d, e), self.RADIUS, 0)
                if self.board[r, c] == 2:
                    pygame.draw.circle(self.Game_Screen, self.player2_color, (d, e), self.RADIUS, 0)

        # turn indicator circle next to the "Player :" label
        if self.current_player == 1:
            pygame.draw.circle(self.Game_Screen, self.player1_color, (400, 37), 27, 0)
        elif self.current_player == 2:
            pygame.draw.circle(self.Game_Screen, self.player2_color, (400, 37), 27, 0)

        # menu button top-right corner
        pygame.draw.rect(self.Game_Screen, (200, 50, 50), (585, 5, 50, 30), 0, 4)
        font_small = pygame.font.Font("PressStart2P-Regular.ttf", 7)
        text_menu_btn = font_small.render("MENU", True, (255, 255, 255))
        self.Game_Screen.blit(text_menu_btn, (588, 13))

        self.surface.blit(self.Game_Screen, (0, 0))

    def check_coloum(self):
        # wait for a mouse click and return which column was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # check if menu button was hit
                if self.menu_btn_rect.collidepoint(mx, my):
                    self.quit_to_menu = True
                    return None

                # check if the click landed inside any cell circle
                for r in range(7):
                    for c in range(7):
                        d = self.X_start + self.RADIUS + c * (2 * self.RADIUS + self.SPACE)
                        e = self.y_start + self.RADIUS + r * (2 * self.RADIUS + self.SPACE)
                        if (mx - d)**2 + (my - e)**2 <= self.RADIUS**2:
                            return c   # only the column matters in connect4
                        
    def check_win(self, player):
        # 4 in a row horizontally
        if np.any(np.all(sliding_window_view(self.board, 4, axis=1) == player, axis=2)):
            return True

        # 4 in a row vertically
        if np.any(np.all(sliding_window_view(self.board, 4, axis=0) == player, axis=2)):
            return True

        # 4 in a row diagonally (top-left to bottom-right)
        self.windows = sliding_window_view(self.board, (4, 4))
        if np.any(np.all(self.windows.diagonal(axis1=2, axis2=3) == player, axis=2)):
            return True
        
        # 4 in a row diagonally (top-right to bottom-left)
        if np.any(np.all(np.flip(self.windows, axis=3).diagonal(axis1=2, axis2=3) == player, axis=2)):
            return True
        
        return False                            

    def make_move(self):
        c = self.check_coloum()
        if c is None:
            return   # no click this frame

        # drop the piece to the lowest empty row in the chosen column
        for f in range(6, -1, -1):
            if self.board[f, c] == 0:
                self.board[f, c] = self.current_player
                if self.check_win(self.current_player):
                    self.game_over = True
                elif not np.any(self.board == 0):   # board full, no winner
                    self.game_over = True
                    self.is_draw = True      
                if not self.game_over:
                    self.switch_turn()
                break   # piece placed, stop looking further down

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.draw_board()

            if self.quit_to_menu:       # user hit menu, skip saving result
                return "Menu"
            
            if not self.game_over:
                self.make_move()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  
                        pygame.quit()
                        exit()

                if not self.result_saved: 
                    # show the final board for 1.5 seconds before saving
                    self.draw_board()            
                    pygame.display.update()     
                    pygame.time.wait(1500)

                    if not self.is_draw:
                        with open("history.csv", "a", newline="", encoding="utf-8-sig") as f:
                            writer = csv.writer(f)
                            if self.current_player == 1:
                                writer.writerow([self.player1, self.player2, self.today, "connect4"])
                            elif self.current_player == 2:
                                writer.writerow([self.player2, self.player1, self.today, "connect4"])   

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

