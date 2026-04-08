import pygame
import numpy as np
from sys import exit

screen = pygame.display.set_mode((600,600))

game_screen = pygame.Surface((598,598))

Dark_blue = (20, 45, 50)
Blue_Grey = (35, 65, 75)
Neon_Blue = (0, 191, 255)
Neon_Yellow = (255, 255, 0)

game_screen.fill(Dark_blue)
pygame.display.set_caption('Tic Tac Toe')
Grid = np.zeros((10,10))

PLAYER_1 = 1
PLAYER_2 = 2
CURRENT_PLAYER = 1

CELL_SIZE = 50
X_OFFSET = 1
Y_OFFSET = 1
SPACE = 6
STEP = CELL_SIZE + SPACE
START_X = 22   
START_Y = 22

while True:
    game_screen.fill(Dark_blue)
    for x in range(22,527,56):
        for y in range(22,527,56):

            pygame.draw.rect(game_screen, Blue_Grey, (x, y, 50, 50), 0, 3)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN :

            mx, my = pygame.mouse.get_pos()

            c = (mx - X_OFFSET) // (CELL_SIZE + SPACE )
            r = (my - Y_OFFSET) // (CELL_SIZE + SPACE )   
            x_pos = START_X + c * STEP
            y_pos = START_Y + r * STEP 

            if Grid[r, c] == 0 :
                if CURRENT_PLAYER == 1 :        
                    Grid[r, c] = 1
                    pygame.draw.line(game_screen, Neon_Blue, (x_pos + 2,y_pos + 2), (x_pos + 48,y_pos + 48), 2)
                    pygame.draw.line(game_screen, Neon_Blue, (x_pos + 2,y_pos + 48), (x_pos + 48,y_pos + 2), 2)                    
                    CURRENT_PLAYER = 2
                elif CURRENT_PLAYER == 2 :
                    Grid[r, c] = 2
                    pygame.draw.circle(game_screen, Neon_Yellow, (x_pos + 25,y_pos + 25), 22, 4)
                    CURRENT_PLAYER = 1
        else:
            continue
    screen.blit(game_screen,(1,1))        
    pygame.display.update()     
