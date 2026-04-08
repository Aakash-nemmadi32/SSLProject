import pygame
import numpy as np
from sys import exit

pygame.init()

Dark_blue = (20, 45, 50)
Blue_Grey = (35, 65, 75)
Neon_Blue = (0, 191, 255)
Neon_Yellow = (255, 255, 0)
player_1_win = pygame.font.Font(None, 20)
player_1_win_surface = player_1_win.render("PLAYER1 WIN", True, Neon_Blue) 
player_2_win = pygame.font.Font(None, 20)
player_2_win_surface = player_2_win.render("PLAYER2 WIN", True, Neon_Yellow)

screen = pygame.display.set_mode((600,600))

game_screen = pygame.Surface((600,600))


game_screen.fill(Dark_blue)
pygame.display.set_caption('Tic Tac Toe')
Grid = np.zeros((10,10))

PLAYER_1 = 1
PLAYER_2 = 2
CURRENT_PLAYER = 1

CELL_SIZE = 50
X_OFFSET = 0
Y_OFFSET = 0
SPACE = 6
STEP = CELL_SIZE + SPACE
START_X = 23   
START_Y = 23

while True:
    game_screen.fill(Dark_blue)
    for x in range(22,527,56):
        for y in range(22,527,56):
            pygame.draw.rect(game_screen, Blue_Grey, (x, y, 50, 50), 0, 3)

    for r in range(10):
        for c in range(10):
            x_pos = START_X + c * STEP
            y_pos = START_Y + r * STEP
            if Grid[r, c] == 1:
                pygame.draw.line(game_screen, Neon_Blue, (x_pos + 2,y_pos + 2), (x_pos + 48,y_pos + 48), 2)
                pygame.draw.line(game_screen, Neon_Blue, (x_pos + 2,y_pos + 48), (x_pos + 48,y_pos + 2), 2)
            elif Grid[r, c] == 2:
                pygame.draw.circle(game_screen, Neon_Yellow, (x_pos + 25,y_pos + 25), 22, 3)



    
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN :

            mx, my = pygame.mouse.get_pos()

            for r in range(10):
                for c in range(10):
                    valid_x_min_row = X_OFFSET + START_X + (c*(CELL_SIZE + SPACE))
                    valid_x_max_row = valid_x_min_row + 50
                    valid_y_min_col = Y_OFFSET + START_Y + (r*(CELL_SIZE + SPACE))
                    valid_y_max_col = valid_y_min_col + 50
                    if valid_x_min_row < mx < valid_x_max_row and valid_y_min_col < my < valid_y_max_col:
                        if Grid[r, c] == 0 :
                            if CURRENT_PLAYER == 1 :        
                                Grid[r, c] = 1
                                CURRENT_PLAYER = 2
                            elif CURRENT_PLAYER == 2 :
                                Grid[r, c] = 2
                                CURRENT_PLAYER = 1
                        else:
                            continue
                    else:
                        continue    



    screen.blit(game_screen,(0,0))        
    pygame.display.update()        
 
