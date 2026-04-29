import pygame
from datetime import date
import numpy as np
class Game():
    
    def __init__(self,player1,player2,surface):
        self.player1 = player1
        self.player2 = player2
        self.surface = surface
        self.current_player = 1
        self.game_over = False
        self.is_draw = False
        self.run_completed = False
        self.result_saved = False
        self.today = date.today()
        self.quit_to_menu = False 
        self.menu_btn_rect = pygame.Rect(585, 5, 50, 30)
        pygame.init()

    def create_board(self,r,c):
        self.rows = r
        self.coloums = c
        self.board = np.zeros((r,c))
        return self.board
    
    
    def make_move(self):
        pass
         

    def switch_turn(self):
        if self.current_player ==  1 :
            self.current_player = 2
        elif self.current_player == 2 :
            self.current_player = 1
    
    
    def check_win(self,player):
        pass

    
    def draw_board(self):
        pass

    def reset_board(self):
        self.board = np.zeros((self.rows,self.coloums))

    
    def run(self):
        pass
    
    def check_grid_empty(self):
        if np.any(self.board == 0):
            return True
        else:
            return False
        

    

        
        