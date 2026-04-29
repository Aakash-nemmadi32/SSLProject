from games.base_game_class import Game
import numpy as np
import pygame
<<<<<<< HEAD
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
=======
from sys import exit
import csv
from datetime import date

class othello(Game):

    def __init__(self, player1, player2, surface):
        super().__init__(player1, player2, surface)

        # Window dimensions
        self.width = 640
        self.height = 640
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Color definitions
        self.BOARD_COLOR        = (20, 100, 40)    # Green board background
        self.GRID_COLOR         = (10, 80, 30)     # Darker green for grid
        self.player1_color      = (30, 30, 30)     # Black pieces for player 1
        self.player2_color      = (240, 240, 240)  # White pieces for player 2
        self.possible_move_color = (100, 200, 100) # Highlight for valid moves

        self.Game_Screen = pygame.Surface((self.width, self.height))

        # Initialize an 8x8 board (0 = empty, 1 = player1, 2 = player2)
        self.create_board(8, 8)

        # Board layout constants
        self.CELL_SIZE = 68   # Pixel size of each cell
        self.X_START   = 40   # Left offset where board begins
        self.Y_START   = 80   # Top offset where board begins
        self.RADIUS    = 26   # Radius of each piece circle

        # All 8 directions for flip detection 
        self.DIRECTIONS = [(-1,-1), (-1,0), (-1,1),
                           ( 0,-1),         ( 0,1),
                           ( 1,-1), ( 1,0), ( 1,1)]

        # Placing first four pieces
        self.settingup_initial_pieces()

    def settingup_initial_pieces(self):
        """Set up the standard Othello starting position."""
        self.board[3, 3] = 2
        self.board[3, 4] = 1
        self.board[4, 3] = 1
        self.board[4, 4] = 2

    def _in_bounds(self, r, c):
        """Return True if (r, c) is within the 8x8 grid."""
        return 0 <= r < 8 and 0 <= c < 8

    def _flips_for_move(self, r, c, player):
        """
        Return a list of opponent pieces that would be flipped
        if `player` places a piece at (r, c).
        Returns an empty list if the move is invalid.
        """
        # Cell must be empty to be a valid placement
        if self.board[r, c] != 0:
            return []

        opponent = 3 - player  # Player 1 ,2 toggle
        all_flips = []

        for dr, dc in self.DIRECTIONS:
            line = []
            nr, nc = r + dr, c + dc

            # Walk in this direction while we see opponent pieces
            while self._in_bounds(nr, nc) and self.board[nr, nc] == opponent:
                line.append((nr, nc))
                nr += dr
                nc += dc

            # Valid flip only if the line ends with one of our own pieces
            if line and self._in_bounds(nr, nc) and self.board[nr, nc] == player:
                all_flips.extend(line)

        return all_flips

    def get_valid_moves(self, player):
        """Return all (row, col) positions where `player` can legally place a piece."""
        moves = []
        for r in range(8):
            for c in range(8):
                if self._flips_for_move(r, c, player):
                    moves.append((r, c))
        return moves

    def _cell_center(self, r, c):
        """Convert grid coordinates (r, c) to pixel center coordinates (x, y)."""
        x = self.X_START + c * self.CELL_SIZE + self.CELL_SIZE // 2
        y = self.Y_START + r * self.CELL_SIZE + self.CELL_SIZE // 2
        return x, y

    def draw_board(self):
        """Render the full board state: background, turn indicator, pieces, valid moves, and scores."""
        self.Game_Screen.fill(self.BOARD_COLOR)

        # --- Turn indicator (top-left) ---
        font = pygame.font.Font("PressStart2P-Regular.ttf", 25)
        text = font.render("Player :", True, (0, 255, 200))
        self.Game_Screen.blit(text, (20, 20))

        # Circle showing whose turn it is
        indicator_color = self.player1_color if self.current_player == 1 else self.player2_color
        pygame.draw.circle(self.Game_Screen, indicator_color, (370, 35), 20, 0)
        pygame.draw.circle(self.Game_Screen, (0, 255, 200), (370, 35), 20, 2)  # Cyan outline

        # --- Drawing empty cell slots (dark circles as "holes")
        for r in range(8):
            for c in range(8):
                cx, cy = self._cell_center(r, c)
                pygame.draw.circle(self.Game_Screen, (10, 60, 20), (cx, cy), self.RADIUS, 0)

        # --- Highlight valid moves for the current player ---
        valid = self.get_valid_moves(self.current_player)
        for (r, c) in valid:
            cx, cy = self._cell_center(r, c)
            pygame.draw.circle(self.Game_Screen, (0, 255, 200), (cx, cy), self.RADIUS, 3)  # Cyan ring

        # --- Draw placed pieces on top of the slots 
        for r in range(8):
            for c in range(8):
                if self.board[r, c] != 0:
                    color = self.player1_color if self.board[r, c] == 1 else self.player2_color
                    cx, cy = self._cell_center(r, c)
                    pygame.draw.circle(self.Game_Screen, color, (cx, cy), self.RADIUS, 0)

        # (top-right area) 
        player1_score = int(np.sum(self.board == 1))
        player2_score = int(np.sum(self.board == 2))
        score_font = pygame.font.Font("PressStart2P-Regular.ttf", 14)
        s1 = score_font.render(f"{self.player1}: {player1_score}", True, (200, 200, 200))
        s2 = score_font.render(f"{self.player2}: {player2_score}", True, (200, 200, 200))
        self.Game_Screen.blit(s1, (430, 15))
        self.Game_Screen.blit(s2, (430, 40))

        #  Menu button (top-right corner) 
        pygame.draw.rect(self.Game_Screen, (200, 50, 50), (585, 5, 50, 30), 0, 4)
        font_small = pygame.font.Font("PressStart2P-Regular.ttf", 7)
        text_menu_btn = font_small.render("MENU", True, (255, 255, 255))
        self.Game_Screen.blit(text_menu_btn, (588, 13))

        # Blit the game surface onto the main display surface
        self.surface.blit(self.Game_Screen, (0, 0))

    def check_win(self):
        """
        Check whether the game has ended.
        The game ends when the board is full or neither player has valid moves.
        Returns (True, winner) where winner is 1, 2, or None (draw).
        Returns (False, None) if the game is still ongoing.
        """
        p1_moves = self.get_valid_moves(1)
        p2_moves = self.get_valid_moves(2)
        board_full = not self.check_grid_empty()

        if board_full or (not p1_moves and not p2_moves):
            p1 = int(np.sum(self.board == 1))
            p2 = int(np.sum(self.board == 2))
            if p1 > p2:
                return True, 1
            elif p2 > p1:
                return True, 2
            else:
                return True, None  # Draw: equal pieces
        return False, None

    def position_in_table(self):
        """
        Process pygame events and return the grid cell [row, col] that was clicked.
        Returns None if no valid cell was clicked this frame.
        Also handles quit events and menu button clicks.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Check if the menu button was clicked
                if self.menu_btn_rect.collidepoint(mx, my):
                    self.quit_to_menu = True
                    return None

                # Check if a board cell was clicked
                for r in range(8):
                    for c in range(8):
                        x = self.X_START + c * self.CELL_SIZE
                        y = self.Y_START + r * self.CELL_SIZE
                        if x < mx < x + self.CELL_SIZE and y < my < y + self.CELL_SIZE:
                            return [r, c]
        return None

    def make_move(self):
        """
        Handle one move for the current player.
        - If the current player has no valid moves, skip their turn.
        - Otherwise wait for a mouse click on a valid cell and apply the move.
        """
        valid = self.get_valid_moves(self.current_player)

        # No valid moves: skip this player's turn
        if not valid:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.time.wait(300)  # Brief pause before switching
            self.switch_turn()
            return

        # Wait for the player to click a cell
        position = self.position_in_table()
        if position is None:
            return  # No click yet this frame

        r, c = position[0], position[1]
        if r is None:
            return

        # Validate the chosen cell
        flips = self._flips_for_move(r, c, self.current_player)
        if not flips:
            return  # Clicked cell is not a legal move

        # Place the piece and flip all captured opponent pieces
        self.board[r, c] = self.current_player
        for fr, fc in flips:
            self.board[fr, fc] = self.current_player

        self.switch_turn()



    def run(self):
        """
        Main game loop. Draws the board, processes moves, and handles
        end-of-game logic (saving result to CSV, returning outcome string).
        Returns 'Menu' if the player quits to menu, 'Draw', or the winner's name.
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            self.draw_board()

            # Check if the user navigated back to the menu
            if self.quit_to_menu:
                return "Menu"

            is_over, winner = self.check_win()

            if not is_over:
                # choosing Move
                self.make_move()
            else:
                # Handle quit events when Menu is chosen
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                if not self.result_saved:
                    winner_name = self.player1 if winner == 1 else self.player2
                    loser_name  = self.player1 if winner == 2 else self.player2

                    # Show the final board briefly before recording the result
                    self.draw_board()
                    pygame.display.update()
                    pygame.time.wait(1500)

                    # Saveing match result to CSV 
                    if winner is not None:
                        with open("history.csv", "a", newline="", encoding="utf-8-sig") as f:
                            writer = csv.writer(f)
                            writer.writerow([winner_name, loser_name, self.today, "othello"])

                    self.result_saved = True
                    running = False
                    return "Draw" if winner is None else winner_name

            pygame.display.update()
            clock.tick(60)  # Cap at 60 FPS
>>>>>>> Harshith
