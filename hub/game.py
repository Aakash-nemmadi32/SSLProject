
import pygame
import numpy as np
import pathlib
import time
import os
import sys
import subprocess
from games.base_game_class import Game
from games.tictactoe import TicTacToe

from games.connect4 import connect4
from games.othello import othello

# draws the main menu with game selection buttons
def menu_page():
    screen.fill("black")
    screen.blit(text, (40,100))
    pygame.draw.rect(screen, (0,255,100), (200,200,200,50), width=2)   # tictactoe button
    pygame.draw.rect(screen, (255,50,50), (200,300,200,50), width=2)   # othello button
    pygame.draw.rect(screen, (150,0,255), (200,400,200,50), width=2)   # connect4 button
    screen.blit(text_tictactoe, (215,215))
    screen.blit(text_othello, (215,315))
    screen.blit(text_connect4, (215,415))

# shows the game over screen with winner name and options to continue
def game_over_page():
    exit_surface.fill("black")
    exit_surface.blit(text_game_over,(120,80))
    exit_surface.blit(text_winner,(180,155))
    pygame.draw.rect(exit_surface, (0,255,100), (170,220,300,55), width=2)   # leaderboard
    pygame.draw.rect(exit_surface, (255,50,50), (170,300,300,55), width=2)   # statistics
    pygame.draw.rect(exit_surface, (150,0,255), (170,380,300,55), width=2)   # restart
    exit_surface.blit(text_leaderboard, (205,235))
    exit_surface.blit(text_statistics, (215,315))
    exit_surface.blit(text_restart, (235,395))
    screen.blit(exit_surface, (0,0))

# shows leaderboard sorting options 
def leader_board_page():     
    leaderboard_surface.fill("black")
    leaderboard_surface.blit(text_sort_by, (640//2 - text_sort_by.get_width()//2, 80))
    pygame.draw.rect(leaderboard_surface, (0,255,100), (160,220,320,55), width=2)
    pygame.draw.rect(leaderboard_surface, (255,50,50), (160,300,320,55), width=2)
    pygame.draw.rect(leaderboard_surface, (150,0,255), (160,380,320,55), width=2)
    pygame.draw.rect(leaderboard_surface, (0,150,255), (160,460,320,55), width=2)
    pygame.draw.rect(leaderboard_surface, (255,255,255), (160,540,320,55), width=2)

    # center each label inside its button
    leaderboard_surface.blit(text_username,  (160 + 320//2 - text_username.get_width()//2,  220 + 55//2 - text_username.get_height()//2))
    leaderboard_surface.blit(text_wins,      (160 + 320//2 - text_wins.get_width()//2,      300 + 55//2 - text_wins.get_height()//2))
    leaderboard_surface.blit(text_loses,     (160 + 320//2 - text_loses.get_width()//2,     380 + 55//2 - text_loses.get_height()//2))
    leaderboard_surface.blit(text_winbyloss, (160 + 320//2 - text_winbyloss.get_width()//2, 460 + 55//2 - text_winbyloss.get_height()//2))
    leaderboard_surface.blit(text_Menu, (160 + 320//2 - text_Menu.get_width()//2, 540 + 55//2 - text_Menu.get_height()//2))
    screen.blit(leaderboard_surface,(0,0))

# runs charts.py to generate the image, then displays it
def statistic_page():
    statistics_surface.fill("black")
    subprocess.run(["python", "charts.py"])
    
    image = pygame.image.load("Statistics.png")
    image = pygame.transform.scale(image, (640, 530))
    statistics_surface.blit(image, (0, 0))  
    
    pygame.draw.rect(statistics_surface, (0, 255, 100), (290, 570, 300, 55), width=2)
    statistics_surface.blit(
        text_back_sta,
        (
            290 + 300//2 - text_back_sta.get_width()//2,   
            570 + 55//2  - text_back_sta.get_height()//2
        )
    )
    
    screen.blit(statistics_surface, (0, 0))


# player names passed in from command line

player1 = sys.argv[1]
player2 = sys.argv[2]

pygame.init()
w,h = 640, 640
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Mini Game Hub")


# ------ fonts and text surfaces ------
font = pygame.font.Font("PressStart2P-Regular.ttf",45)
text = font.render("AAHa Gamehub",True,(0,255,200))
font_small = pygame.font.Font("PressStart2P-Regular.ttf",20)
text_tictactoe = font_small.render("TicTacToe",True,(0,255,255))
text_connect4 = font_small.render("Connect4",True,(0,255,255))
text_othello = font_small.render("Othello",True,(0,255,255))

# ------ menu button rects ------
tic_rect = pygame.Rect(200, 200, 200, 50)
oth_rect = pygame.Rect(200, 300, 200, 50)
con_rect = pygame.Rect(200, 400, 200, 50)

# ------ game over screen setup ------
exit_surface = pygame.Surface((640,640))
exit_surface.fill("black")
text_leaderboard = font_small.render("leaderboard",True,(0,255,255))
text_statistics = font_small.render("statistics",True,(0,255,255))
text_restart = font_small.render("restart",True,(0,255,255))
font_game_over = pygame.font.Font("PressStart2P-Regular.ttf",45)
text_game_over = font_game_over.render("Game Over",True,(0,255,200))
font_winner = pygame.font.Font("PressStart2P-Regular.ttf",20)

# ------ leaderboard screen setup ------
leaderboard_surface = pygame.Surface((640,640))
font_sort_by = pygame.font.Font("PressStart2P-Regular.ttf",45)
text_sort_by = font_sort_by.render("Sort By",True,(0,255,200))
text_username = font_small.render("Username",True,(0,255,255))
text_wins = font_small.render("Number of Wins",True,(0,255,255))
text_loses = font_small.render("Number of Loses",True,(0,255,255))
text_winbyloss = font_small.render("Win/Lose",True,(0,255,255))

# click rects for game over page buttons
leaderboard_rect = pygame.Rect(170, 220, 300, 55)
statistics_rect = pygame.Rect(170, 300, 300, 55)
restart_rect = pygame.Rect(170, 380, 300, 55)

# click rects for leaderboard sort buttons
username_rect = pygame.Rect(160, 220, 320, 55)
wins_rect = pygame.Rect(160, 300, 320, 55)
loses_rect = pygame.Rect(160, 380, 320, 55)
winbyloses_rect = pygame.Rect(160, 460, 320, 55)
text_Menu = font_small.render("Menu",True,(0,255,255))
Menu_rect = pygame.Rect(160,540,320,55)

# ------ statistics screen setup ------
statistics_surface = pygame.Surface((640,640))
text_back_sta = font_small.render("Back",True,(255,255,255))
back_sta_rect = pygame.Rect(290, 570, 300, 55) 


running = True

# flags to track which screen we're currently on
game_started = False
game_over = False
leader_board_clicked = False
statistic_show = False

while running:
    # decide which screen to draw based on current state
    if  not game_started:
        menu_page()
    elif statistic_show:           
        statistic_page()
    elif game_over and not leader_board_clicked:
        game_over_page()
    elif leader_board_clicked:
        leader_board_page()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # ---- menu screen clicks ----
            if  not game_started:
                if tic_rect.collidepoint(mouse_pos):
                    current_game = "tictactoe"
                    game_started = True
                    t = TicTacToe(player1,player2,screen)
                    winner = t.run()
                    if winner == "Menu":
                        # user quit back to menu mid-game
                        game_started = False
                        game_over = False
                        leader_board_clicked = False
                        statistic_show = False
                    elif winner == "Draw":
                        text_winner = font_winner.render("It's a Draw!", True, (0,255,200))
                    else:
                        text_winner = font_winner.render(f"{winner} Wins!", True, (0,255,200))                    
                    game_over = True                          

                elif oth_rect.collidepoint(mouse_pos):
                    current_game = "othello"
                    game_started = True
                    t = othello(player1,player2,screen)
                    winner = t.run()
                    if winner == "Menu":
                        game_started = False
                        game_over = False
                        leader_board_clicked = False
                        statistic_show = False
                    elif winner == "Draw":
                        text_winner = font_winner.render("It's a Draw!", True, (0,255,200))
                    else:
                        text_winner = font_winner.render(f"{winner} Wins!", True, (0,255,200))
                    game_over = True

                elif con_rect.collidepoint(mouse_pos):
                    current_game = "connect4"
                    game_started = True
                    t = connect4(player1,player2,screen)
                    winner = t.run()
                    if winner == "Menu":
                        game_started = False
                        game_over = False
                        leader_board_clicked = False
                        statistic_show = False
                    if winner == "Draw":
                        text_winner = font_winner.render("It's a Draw!", True, (0,255,200))
                    else:
                        text_winner = font_winner.render(f"{winner} Wins!", True, (0,255,200))
                    game_over = True

            # ---- statistics screen clicks ----
            elif statistic_show:                          
                if back_sta_rect.collidepoint(mouse_pos):
                    statistic_show = False

            # ---- game over screen clicks ----
            elif game_over and not leader_board_clicked:
                if leaderboard_rect.collidepoint(mouse_pos):
                    leader_board_clicked = True
                if statistics_rect.collidepoint(mouse_pos):
                    statistic_show = True 
                        
                if restart_rect.collidepoint(mouse_pos):
                    # restart the same game that was just played
                    game_over = False
                    if current_game == "tictactoe":
                        t = TicTacToe(player1,player2,screen)
                    elif current_game == "othello":
                        t = othello(player1,player2,screen)
                    else:
                        t = connect4(player1,player2,screen)

                    winner = t.run()
                    text_winner = font_winner.render(f"{winner} Wins!", True, (0,255,200))
                    game_over = True 

            # ---- leaderboard screen clicks — calls shell script to sort & display ----
            elif leader_board_clicked:
                if username_rect.collidepoint(mouse_pos):
                    subprocess.run(["bash", "leaderboard.sh" , "username" ])  
                if wins_rect.collidepoint(mouse_pos):
                    subprocess.run(["bash", "leaderboard.sh" , "Wins" ]) 
                if loses_rect.collidepoint(mouse_pos):
                    subprocess.run(["bash", "leaderboard.sh" , "Loses" ]) 
                if winbyloses_rect.collidepoint(mouse_pos):
                    subprocess.run(["bash", "leaderboard.sh" , "Wins/Loses" ])
                if Menu_rect.collidepoint(mouse_pos):
                    # go back to the main menu
                    game_started = False
                    game_over = False
                    leader_board_clicked = False

    pygame.display.update()

