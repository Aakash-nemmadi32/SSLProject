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
        self.board[3,3] = 2
        self.board[4,4] = 2
        self.board[3,4] = 1
        self.board[4,3] = 1
    def draw_board(self):
        pygame.init()
        self.screen.blit(self.game_screen,(0,0))
        self.game_screen.fill((0,0,0))
        for x in range(19,622,86):
            for y in range(19,622,86):
                pygame.draw.rect(self.game_screen,darkgreen,(x,y,80,80),0,-1)
        for r in range(8):
            for c in range(8):
                x_pos = self.START_X + c * self.STEP + self.CELL_SIZE//2
                y_pos = self.START_Y + r * self.STEP + self.CELL_SIZE//2
                if self.board[r, c] == 1:
                    pygame.draw.circle(self.game_screen,(0,0,0),(x_pos,y_pos),39,width=0)
                    pygame.draw.circle(self.game_screen,(128,128,128),(x_pos,y_pos), 39,width=6)
                elif self.board[r, c] == 2:
                    pygame.draw.circle(self.game_screen,(255,255,255),(x_pos,y_pos),39,width=0)
                    pygame.draw.circle(self.game_screen,(128,128,128),(x_pos,y_pos), 39,width=6)
    def make_move(self):
        if not self.has_valid_move(self.current_player):
            self.switch_turn()
            if not self.has_valid_move(self.current_player):
                self.game_over = True
            return
        position = self.position_in_table()
        if position is None:
            return      
        r = position[0]
        c = position[1]
        if self.check_move_validity(r,c):   
            self.board[r, c] = self.current_player
            l=zip(*np.where(self.board==self.current_player))
            for i in l:
                if i[0] == r and i[1] == c:
                    continue
                elif i[0] == r:
                    arr = self.board[r,min(i[1],c)+1:max(i[1],c):1]
                    if len(arr)>0:
                        opponent = 2 if self.current_player == 1 else 1
                        if arr[0] == opponent and np.all(arr == opponent):
                            self.board[r, min(i[1],c)+1:max(i[1],c):1] = self.current_player
                elif i[1] == c:
                    arr = self.board[min(i[0],r)+1:max(i[0],r):1,c]
                    if len(arr) > 0 :
                        opponent = 2 if self.current_player == 1 else 1
                        if arr[0] == opponent and np.all(arr == opponent):
                            self.board[min(i[0],r)+1:max(i[0],r):1,c] = self.current_player
                elif abs(i[0]-r) == abs(i[1]-c):
                    dr = 1 if r > i[0] else -1
                    dc = 1 if c > i[1] else -1
                    cells = []
                    rr, cc = i[0] + dr, i[1] + dc
                    valid = False
                    while 0 <= rr < 8 and 0 <= cc < 8:
                        if (rr, cc) == (r, c):
                            valid = True
                            break
                        if self.board[rr][cc] == 0:
                            break
                        if self.board[rr][cc] == self.current_player:
                            break
                        cells.append((rr, cc))
                        rr += dr
                        cc += dc
                    if valid and len(cells) > 0:
                        for x, y in cells:
                            self.board[x][y] = self.current_player
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
    def check_move_validity(self,r,c):
        if self.board[r, c] == 0:
            t = False
            arr1 = np.where(self.board[r] == self.current_player)[0]
            for i in arr1:
                if i < c:
                    arr = self.board[r,i+1:c:1]
                    if len(arr) > 0:
                        opponent = 2 if self.current_player == 1 else 1
                        if arr[0] == opponent:
                            if np.all(arr == opponent):
                                t = True
                                break
                elif i > c:
                    arr = self.board[r,c+1:i:1]
                    if len(arr) > 0:
                        opponent = 2 if self.current_player == 1 else 1
                        if arr[0] == opponent:
                            if np.all(arr == opponent):
                                t= True
                                break            
            arr2 = np.where(self.board[:,c] == self.current_player)[0]
            for i in arr2:
                if i < r:
                    Arr = self.board[i+1:r:1,c]
                    if len(Arr) > 0:
                        opponent = 2 if self.current_player == 1 else 1
                        if Arr[0] == opponent and np.all(Arr == opponent):
                            t = True
                            break
                elif i > r:
                    Arr = self.board[r+1:i:1,c]
                    if len(Arr) > 0 :
                        opponent = 2 if self.current_player == 1 else 1
                        if Arr[0] == opponent and np.all(Arr == opponent):
                            t= True
                            break
            opponent = 2 if self.current_player == 1 else 1
            for dr, dc in [(1,1), (1,-1), (-1,1), (-1,-1)]:
                rr, cc = r + dr, c + dc
                found_opponent = False
                while 0 <= rr < 8 and 0 <= cc < 8:
                    if self.board[rr][cc] == opponent:
                        found_opponent = True
                    elif self.board[rr][cc] == self.current_player:
                        if found_opponent:
                            t = True
                            break
                        else:
                            break
                    else:
                        break
                    rr += dr
                    cc += dc
                if t:
                    break
            return t
        else:
            return False
    def has_valid_move(self, player):
        current_backup = self.current_player
        self.current_player = player
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == 0:
                    if self.check_move_validity(r, c):
                        self.current_player = current_backup
                        return True
        self.current_player = current_backup
        return False
    def check_win(self,player):
        if not self.has_valid_move(1) and not self.has_valid_move(2):
            p1 = np.sum(self.board == 1)
            p2 = np.sum(self.board == 2)
            if p1 > p2:
                return player == 1
            elif p2 > p1:
                return player == 2
            else:
                return False
        else:
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