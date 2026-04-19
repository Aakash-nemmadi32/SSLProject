
from .base_game_class import Game
import numpy as np
import pygame
from sys import exit
from numpy.lib.stride_tricks import sliding_window_view

Dark_blue = (20, 45, 50)
Blue_Grey = (35, 65, 75)
Neon_Blue = (0, 191, 255)
Neon_Yellow = (255, 255, 0)

class TicTacToe(Game):

    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        CELL_SIZE = 50
        self.CELL_SIZE = 50
        self.X_OFFSET = 0
        self.Y_OFFSET = 0
        self.SPACE = 6
        self.height = 600
        self.width = 600
        self.STEP = self.CELL_SIZE + self.SPACE
        self.game_screen = pygame.Surface((self.width,self.height))
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.START_X = 23   
        self.START_Y = 23
        self.game_over = False
        self.create_board(10,10)
    
    def draw_board(self):
        pygame.init()
        self.screen.blit(self.game_screen,(0,0))
        self.game_screen.fill(Dark_blue)
        for x in range(22,527,56):
            for y in range(22,527,56):
                pygame.draw.rect(self.game_screen, Blue_Grey, (x, y, 50, 50), 0, 3)

            for r in range(10):
                for c in range(10):
                    x_pos = self.START_X + c * self.STEP
                    y_pos = self.START_Y + r * self.STEP
                    if self.board[r, c] == 1:
                        pygame.draw.line(self.game_screen, Neon_Blue, (x_pos + 2,y_pos + 2), (x_pos + 48,y_pos + 48), 2)
                        pygame.draw.line(self.game_screen, Neon_Blue, (x_pos + 2,y_pos + 48), (x_pos + 48,y_pos + 2), 2)
                    elif self.board[r, c] == 2:
                        pygame.draw.circle(self.game_screen, Neon_Yellow, (x_pos + 25,y_pos + 25), 22, 3)        
    
    def check_win(self, player):
        if np.any(np.all(sliding_window_view(self.board, 5, axis=1) == player, axis=2)):
            return True
        
        if np.any(np.all(sliding_window_view(self.board, 5, axis=0) == player, axis=2)):
            return True

        self.windows = sliding_window_view(self.board, (5,5))
        if np.any(np.all(self.windows.diagonal(axis1=2, axis2=3) == player, axis=2)):
            return True
        
        if np.any(np.all(np.flip(self.windows, axis=3).diagonal(axis1=2, axis2=3) == player, axis=2)):
            return True
        
        return False
    
    def position_in_table(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN :

                mx, my = pygame.mouse.get_pos()

                for r in range(10):
                    for c in range(10):
                        valid_x_min_row = self.X_OFFSET + self.START_X + (c*(self.CELL_SIZE + self.SPACE))
                        valid_x_max_row = valid_x_min_row + self.CELL_SIZE
                        valid_y_min_col = self.Y_OFFSET + self.START_Y + (r*(self.CELL_SIZE + self.SPACE))
                        valid_y_max_col = valid_y_min_col + self.CELL_SIZE
                        if valid_x_min_row < mx < valid_x_max_row and valid_y_min_col < my < valid_y_max_col:
                            return [r, c]
    

    def make_move(self):
        position = self.position_in_table()
        if position is None:
            return
        
        r = position[0]
        c = position[1]
        if self.board[r, c] == 0 :   
            self.board[r, c] = self.current_player
            if self.check_win(self.current_player):
                self.game_over = True
            if not self.game_over:
                self.switch_turn()

    def show_result(self):
        dark_overlay = pygame.Surface((self.width,self.height))
        dark_overlay.fill((0,0,0))
        dark_overlay.set_alpha(120)
        current_player_text = pygame.font.Font(None, 50)

        if self.game_over:
            text = f"Player {self.current_player} Wins!"
            if self.current_player == self.player1 :                
                color = Neon_Blue
            else:
                color = Neon_Yellow
        elif not self.check_grid_empty():
            text = "Game Draws!"
            color = (255, 0, 255)
        else:
            return
        
        text_surface = current_player_text.render(text, True, color)
        rect = text_surface.get_rect(center=(150, 60))
        ui_surface = pygame.Surface((300, 120))
        ui_surface.fill((Dark_blue))
        ui_surface.set_alpha(230)        
        ui_surface.blit(text_surface, rect)

        self.screen.blit(self.game_screen,(0,0))
        self.screen.blit(dark_overlay,(0,0))
        self.screen.blit(ui_surface, (177, 267))  

    def run(self):
        clock = pygame.time.Clock()


        while True:
            self.draw_board()
            
            if not self.game_over:
                self.make_move()
            else:
                self.show_result()     
                
        
            pygame.display.update() 
            clock.tick(60)   


        