# SSLProject

## Overview of GameHub project
   Mini Game Hub is a Two-player gaming Platform built using Bash and Python (pygame).
   It allows two authenticated users to log in ,select a game from a menu,play via a graphical interface , and have their
   results recorded on a persistent leaderboard
 
---

## Features of this Mini Game Hub
- user authentication with SHA-256 password hashing
- Two player login system with distinct usernames and passwords
- Games included to play are:
  - Tic-Tac-Toe (10x10 , 5 in a row horizontally,vertically or diagonally)
  - Othello (Reversi)
  - Connect Four ( 7x7 , 4 in a row)
- Games are rendenred in Pygame GUI window
- LeaderBoard system after each Gameplay will be updated (wins , losses , win ratio)
- Data Visualization using Matplotlib
- option to replay games

---

## Requirements
- python
- numpy
- pygame
- matplotlib

## How to Run

bash main.sh

---

## Project Structure
    
hub/ |- main.sh |-game.py |-leaderboard.sh 
  |--  |-games/ |-tictactoe.py |-othello.py |- connectfour.py
  |-- users.tsv
  |-- history.csv

---

Install Dependencies :
```bash
pip install pygame numpy matplotlib
