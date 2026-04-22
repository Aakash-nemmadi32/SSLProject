import pygame
import numpy as np
import matplotlib
import pathlib
import time
import os
import sys
from games.base_game_class import Game
from games.tictactoe import TicTacToe
from games.othello import Othello
from games.connect4 import connect4
#assigning the usernames given as arguments as the players of game 
player1 = sys.argv[1]
player2 = sys.argv[2]
#creating a menu display, an interface to select the game
pygame.init()
w,h = 720, 720
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Mini Game Hub")
# Loading image as menu
menu_img = pygame.image.load("menu.jpg")
menu_img = pygame.transform.scale(menu_img, (w,h))
# Defining button areas 
tic_rect = pygame.Rect(50, 520, 160, 70)
oth_rect = pygame.Rect(270, 520, 180, 70)
con_rect = pygame.Rect(512, 528, 150, 50)
running = True
while running:
    screen.blit(menu_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if tic_rect.collidepoint(mouse_pos):
                pygame.quit()
                t=TicTacToe(1,2)
                t.run()
                sys.exit()
            elif oth_rect.collidepoint(mouse_pos):
                pygame.quit()
                o=Othello(1,2)
                o.run()
                sys.exit()
            elif con_rect.collidepoint(mouse_pos):
                pygame.quit()
                c=connect4(1,2)
                c.run()
                sys.exit()
    pygame.display.update()
pygame.quit()