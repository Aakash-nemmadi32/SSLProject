import pygame
import numpy
import matplotlib
import pathlib
import time
import os
import sys
#defining a base class for all games
class Game:
    #constructor(__init__) to initiate the game
    def __init__(self, player1, player2, n, ):
        self.player1 = player1
        self.player2 = player2
        self.n = n
        self.curplayer = player1
    
#assigning the usernames given as arguments as the players of game 
player1 = sys.argv[1]
player2 = sys.argv[2]
pygame.init()
#creating a menu display, an interface to select the game
pygame.display.set_caption('Menu')
screen = pygame.display.set_mode((1282,725))
select=pygame.Surface((1280,180))
tictac = pygame.Surface((1280,180))
othello = pygame.Surface((1280,180))
connect4 = pygame.Surface((1280,180))
seld = pygame.font.Font(None,60)
ticopt = pygame.font.Font(None,60)
othopt = pygame.font.Font(None,60)
conopt = pygame.font.Font(None,60)
menu = seld.render('Select a game', True, 'Blue')
topt = ticopt.render('Tictactoe', True, 'Red')
opt = othopt.render('Othello', True, 'Gray')
con = conopt.render('Connect4', True, 'Orange')
tictac_rect   = pygame.Rect(1,182,1280,180)
othello_rect  = pygame.Rect(1,363,1280,180)
connect4_rect = pygame.Rect(1,544,1280,180)
darkgreen = (0,100,0)
select.fill('Violet')
tictac.fill('White')
othello.fill(darkgreen)
connect4.fill(darkgreen)
c = 12
r = 2
w = 1280 / c
h = 180 / r
for col in range(c + 1):
    x = int(col * w)
    if col == c:
        x = 1280
    pygame.draw.line(othello, "black", (x, 0), (x, 180), 2)
for row in range(r + 1):
    y = int(row * h)
    if row == r:
        y = 180
    pygame.draw.line(othello, "black", (0, y), (1280, y), 2)
for row in range(r):
    for col in range(c):
        x = int(col*w+w//2)
        y = int(row*h+h//2)
        color = "black" if (row + col) % 2 == 0 else "white"
        radius = min(w,h)//3
        pygame.draw.circle(othello, color, (x, y), radius)
        pygame.draw.circle(othello, "black", (x, y), radius, 2)
for row in range(2):              
    for col in range(12):
        x = 50 + col * 100
        y = 50 + row * 70
        if (row + col) % 2 == 0:
            color = "red"
        else:
            color = "yellow"
        pygame.draw.circle(connect4, color, (x, y), 25)
        pygame.draw.circle(connect4, "black", (x, y), 25, 2)  

running = True
while running:
    screen.blit(select,(1,1))
    screen.blit(tictac,(1,182))
    screen.blit(othello,(1,363))
    screen.blit(connect4,(1,544))
    screen.blit(menu,(321,61))
    screen.blit(topt,(321,242))
    screen.blit(opt,(321,423))
    screen.blit(con,(321,604))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            

            if tictac_rect.collidepoint(event.pos):
                pygame.quit()
                game=tictac()
                game.play()
                pygame.display.update()

            elif othello_rect.collidepoint(event.pos):
                pygame.quit()
                game=othello()
                game.play()
                pygame.display.update()

            elif connect4_rect.collidepoint(event.pos):
                pygame.quit()
                game=connect4()
                game.play()
                pygame.display.update()

pygame.quit()
