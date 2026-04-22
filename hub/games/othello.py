import numpy as np
import pygame
import sys
from .base_game_class import Game
darkgreen = (0,100,0)
class Othello(Game):
    
    def __init__(self,player1,player2):
        super().__init__(player1,player2)
        CELL_SIZE = 80
        self.CELL_SIZE = 80
        self.X_OFFSET = 0
        self.Y_OFFSET = 0
        self.SPACE = 6
        self.height = 720
        self.width = 720
        self.STEP = self.CELL_SIZE + self.SPACE
        self.game_screen = pygame.Surface((self.width,self.height))
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.START_X = 19   
        self.START_Y = 19
        self.game_over = False
        self.create_board(8,8)
    def draw_board(self):
        pygame.init()
        self.screen.blit(self.game_screen,(0,0))
        self.game_screen.fill((0,0,0))
        for x in range(19,622,86):
            for y in range(19,622,86):
                pygame.draw.rect(self.game_screen,darkgreen,(x,y,80,80),0,-1)
        pygame.draw.circle(self.game_screen,(255,255,255),(317,317),39,width=0)
        pygame.draw.circle(self.game_screen,(255,255,255),(403,403),39,width=0)
        pygame.draw.circle(self.game_screen,(0,0,0),(317,403),39,width=0)
        pygame.draw.circle(self.game_screen,(0,0,0),(403,317),39,width=0)
        pygame.draw.circle(self.game_screen,(128,128,128),(317,317),39,width=6)
        pygame.draw.circle(self.game_screen,(128,128,128),(403,403),39,width=6)
        pygame.draw.circle(self.game_screen,(128,128,128),(317,403),39,width=6)
        pygame.draw.circle(self.game_screen,(128,128,128),(403,317),39,width=6)
        for r in range(8):
            for c in range(8):
                x_pos = self.START_X + c * self.STEP + self.CELL_SIZE//2
                y_pos = self.START_Y + r * self.STEP + self.CELL_SIZE//2
                if self.board[r, c] == 1:
                    pygame.draw.circle(self.game_screen,(255,255,255),(x_pos,y_pos),39,width=0)
                    pygame.draw.circle(self.game_screen,(128,128,128),(x_pos,y_pos), 39,width=6)
                elif self.board[r, c] == 2:
                    pygame.draw.circle(self.game_screen,(0,0,0),(x_pos,y_pos),39,width=0)
                    pygame.draw.circle(self.game_screen,(128,128,128),(x_pos,y_pos), 39,width=6)
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
    def position_in_table(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN :

                mx, my = pygame.mouse.get_pos()
                

                for r in range(8):
                    for c in range(8):
                        valid_x_min_row = self.X_OFFSET + self.START_X + (c*(self.CELL_SIZE + self.SPACE))
                        valid_x_max_row = valid_x_min_row + self.CELL_SIZE
                        valid_y_min_col = self.Y_OFFSET + self.START_Y + (r*(self.CELL_SIZE + self.SPACE))
                        valid_y_max_col = valid_y_min_col + self.CELL_SIZE
                        if valid_x_min_row < mx < valid_x_max_row and valid_y_min_col < my < valid_y_max_col:
                            return [r, c]
    def check_win(self, player):
        return False
    def show_result(self):
        overlay = pygame.Surface((self.width,self.height))
        overlay.fill((135,206,250))
        overlay.set_alpha(120)
        current_player_text = pygame.font.Font(None, 50)

        if self.game_over:
            text = f"Player {self.current_player} Wins!"
            if self.current_player == self.player1 :                
                color = ((0,0,0))
            else:
                color = ((255,255,255))
        elif not self.check_grid_empty():
            text = "Game Draws!"
            color = (192,192,192)
        else:
            return
        text_surface = current_player_text.render(text, True, color)
        rect = text_surface.get_rect(center=(150, 60))
        ui_surface = pygame.Surface((300, 120))
        ui_surface.fill((135,206,250))
        ui_surface.set_alpha(230)        
        ui_surface.blit(text_surface, rect)

        self.screen.blit(self.game_screen,(0,0))
        self.screen.blit(overlay,(0,0))
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
