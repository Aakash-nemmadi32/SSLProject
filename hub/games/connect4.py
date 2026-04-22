from abc import abstractmethod

from basegame_class import Game
import numpy as np
import pygame
from sys import exit
from numpy.lib.stride_tricks import sliding_window_view

class connect4(Game):

    def __init__(self, player1, player2):
        super().__init__(player1, player2)

        self.width = 454
        self.height = 454
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.player1_color = (255,0,0)
        self.player2_color = (255,255,0)
        self.BOARD_COLOR = (0,0,255)
        self.Game_Screen = pygame.Surface((self.width,self.height))
        self.create_board(7,7)
        self.X_start = 22
        self.y_start = 22
        self.RADIUS = 25
        self.SPACE = 10

    def draw_board(self):
        pygame.init()
        self.screen.blit(self.Game_Screen,(0,0))
        self.Game_Screen.fill(self.BOARD_COLOR)
        for x in range(47, 408, 60):
            for y in range(47 , 408, 60):
                pygame.draw.circle(self.Game_Screen, (255,255,255), (x,y), self.RADIUS, 0)

        for r in range(7):
            for c in range(7):
                d = self.X_start + self.RADIUS + c*( 2*self.RADIUS + self.SPACE )
                e = self.y_start + self.RADIUS + r*( 2*self.RADIUS + self.SPACE )
                if self.board[r ,c] == self.player1 :                              
                    pygame.draw.circle(self.Game_Screen, self.player1_color, (d, e), self.RADIUS, 0)
                if self.board[r,c] == self.player2 :
                    pygame.draw.circle(self.Game_Screen, self.player2_color, (d, e), self.RADIUS, 0)



    def check_coloum(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
            if event.type == pygame.MOUSEBUTTONDOWN :
                mx, my = pygame.mouse.get_pos()
                for r in range(7):
                    for c in range(7):
                        d = self.X_start + self.RADIUS + c*( 2*self.RADIUS + self.SPACE )
                        e = self.y_start + self.RADIUS + r*( 2*self.RADIUS + self.SPACE )
                        if ( mx - d )**2 + (my - e )**2 <= self.RADIUS**2 :
                            return c
                        
    def check_win(self, player):
        
        if np.any(np.all(sliding_window_view(self.board, 4, axis=1) == player, axis=2)):
            return True
            
        if np.any(np.all(sliding_window_view(self.board, 4, axis=0) == player, axis=2)):
            return True

        self.windows = sliding_window_view(self.board, (4,4))
        if np.any(np.all(self.windows.diagonal(axis1=2, axis2=3) == player, axis=2)):
            return True
        
        if np.any(np.all(np.flip(self.windows, axis=3).diagonal(axis1=2, axis2=3) == player, axis=2)):
            return True
        
        return False                            

    def make_move(self):
        c = self.check_coloum()
        if c is None:
            return  
        for f in range(6, -1, -1) :
            if self.board[f, c] == 0:
                self.board[f, c] = self.current_player
                if self.check_win(self.current_player):
                    self.game_over = True
                if not self.game_over:
                    self.switch_turn()
                break

    def show_result(self):
        dark_overlay = pygame.Surface((454,454))
        dark_overlay.fill((0,0,0))
        dark_overlay.set_alpha(120)
        current_player_text = pygame.font.Font(None, 50)

        if self.game_over:
            text = f"Player {self.current_player} Wins!"
            if self.current_player == self.player1 :                
                color = self.player1_color
            else:
                color = self.player2_color
        elif not self.check_grid_empty():
            text = "Game Draws!"
            color = (255, 0, 255)
        else:
            return
        
        text_surface = current_player_text.render(text, True, color)
        rect = text_surface.get_rect(center=(150, 60))
        ui_surface = pygame.Surface((300, 120))
        ui_surface.fill((self.BOARD_COLOR))
        ui_surface.set_alpha(230)        
        ui_surface.blit(text_surface, rect)

        self.screen.blit(self.Game_Screen,(0,0))
        self.screen.blit(dark_overlay,(0,0))
        self.screen.blit(ui_surface, (77, 167))    


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
            
