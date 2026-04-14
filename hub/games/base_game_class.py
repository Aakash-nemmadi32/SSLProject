from abc import ABC, abstractmethod
import numpy as np
class Game(ABC):
    
    def __init__(self,player1,player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.game_over = False

    def create_board(self,r,c):
        self.rows = r
        self.coloums = c
        self.board = np.zeros((r,c))
        return self.board
    
    @abstractmethod
    def make_move(self):
        pass
         

    def switch_turn(self):
        if self.current_player ==  self.player1 :
            self.current_player = self.player2
        elif self.current_player == self.player2 :
            self.current_player = self.player1
    
    @abstractmethod
    def check_win(self,player):
        pass

    @abstractmethod
    def draw_board(self):
        pass

    def reset_board(self):
        self.board = np.zeros((self.rows,self.coloums))

    @abstractmethod
    def run(self):
        pass
    
    def check_grid_empty(self):
        if np.any(self.board == 0):
            return True
        else:
            return False
