import pygame
import numpy as np
import matplotlib
import pathlib
import time
import os
import sys
import importlib
from games.base_game_class import Game
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
            print(pygame.mouse.get_pos())
            mouse_pos = pygame.mouse.get_pos()

            if tic_rect.collidepoint(mouse_pos):
                module = importlib.import_module("games.tictactoe")
                game = module.TicTacToe(player1,player2)
                game.run()
            elif oth_rect.collidepoint(mouse_pos):
                module = importlib.import_module("games.othello")
                game = module.Othello(player1,player2)
                game.run()
            elif con_rect.collidepoint(mouse_pos):
                module = importlib.import_module("games.connect4")
                game = module.Connect4(player1,player2)
                game.run()

    pygame.display.update()

pygame.quit()
