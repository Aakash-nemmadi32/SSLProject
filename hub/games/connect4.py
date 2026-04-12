import numpy as np
from sys import exit
import pygame
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def check_win(board, player):
    
    if np.any(np.all(sliding_window_view(board, 4, axis=1) == player, axis=2)):
        return True
        
    if np.any(np.all(sliding_window_view(board, 4, axis=0) == player, axis=2)):
        return True

    windows = sliding_window_view(board, (4,4))
    if np.any(np.all(windows.diagonal(axis1=2, axis2=3) == player, axis=2)):
        return True
    
    if np.any(np.all(np.flip(windows, axis=3).diagonal(axis1=2, axis2=3) == player, axis=2)):
        return True
    
    return False

def check_grid_empty(grid):
    if np.any(grid == 0):
        return True
    else:
        return False



pygame.init()

screen = pygame.display.set_mode((454,454))

BOARD_COLOR = (0, 0, 255)
PLAYER1_COLOR = (255, 0 , 0)
PLAYER2_COLOR = (255, 255, 0)
current_player = 1

X_start = 22
y_start = 22
SPACE = 10
RADIUS = 25

Game_Screen = pygame.Surface((454,454))
Grid = np.zeros((7,7))

player1_screen = pygame.Surface((400,400))
player1_screen.fill(PLAYER1_COLOR)
game_over = False

while True:
    screen.blit(Game_Screen,(0,0))
    Game_Screen.fill(BOARD_COLOR)
    for x in range(47, 408, 60):
        for y in range(47 , 408, 60):
            pygame.draw.circle(Game_Screen, (255,255,255), (x,y), 25, 0)
    
    for r in range(7):
        for c in range(7):
            d = X_start + RADIUS + c*( 2*RADIUS + SPACE )
            e = y_start + RADIUS + r*( 2*RADIUS + SPACE )
            if Grid[r ,c] == 1 :                              
                pygame.draw.circle(Game_Screen, PLAYER1_COLOR, (d, e), 25, 0)
            if Grid[r,c] == 2 :
                pygame.draw.circle(Game_Screen, PLAYER2_COLOR, (d, e), 25, 0)
                        
                            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN :
            mx, my = pygame.mouse.get_pos()
            for r in range(7):
                for c in range(7):
                    d = X_start + RADIUS + c*( 2*RADIUS + SPACE )
                    e = y_start + RADIUS + r*( 2*RADIUS + SPACE )
                    if ( mx - d )**2 + (my - e )**2 <= RADIUS**2 :
                        for f in range(6, -1, -1) :
                            if Grid[f ,c] == 0:
                                Grid[f, c] = current_player
                                if check_win(Grid,current_player):
                                    game_over = True
                                if not game_over:
                                    current_player = 3 - current_player
                                break
    if game_over :
        dark_overlay = pygame.Surface((454,454))
        dark_overlay.fill((0,0,0))
        dark_overlay.set_alpha(120)
        current_player_text = pygame.font.Font(None, 50)
        text = f"Player {current_player} Wins!"
        if current_player == 1 :
            current_player_surface = current_player_text.render(text, True, PLAYER1_COLOR)
        else:
            current_player_surface = current_player_text.render(text, True, PLAYER2_COLOR)
        rect = current_player_surface.get_rect(center=(150, 60))
        ui_surface = pygame.Surface((300, 120))
        ui_surface.fill((BOARD_COLOR))
        ui_surface.set_alpha(230)
        ui_surface.blit(current_player_surface, rect)

        screen.blit(Game_Screen,(0,0))
        screen.blit(dark_overlay,(0,0))
        screen.blit(ui_surface, (77, 167))
    else:
        if not check_grid_empty(Grid):
            dark_overlay = pygame.Surface((454,454))
            dark_overlay.fill((0,0,0))
            dark_overlay.set_alpha(120)
            Game_Draw_text = pygame.font.Font(None, 50)
            Game_Draw_surface = Game_Draw_text.render("Game Draws!", True, (255,0,255))
        
            rect = Game_Draw_surface.get_rect(center=(150, 60))
            ui_surface = pygame.Surface((300, 120))
            ui_surface.fill((BOARD_COLOR))
            ui_surface.set_alpha(230)
            ui_surface.blit(Game_Draw_surface, rect)

            screen.blit(Game_Screen,(0,0))
            screen.blit(dark_overlay,(0,0))
            screen.blit(ui_surface, (77, 167))
         
    pygame.display.update()


