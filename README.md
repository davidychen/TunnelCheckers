# Tunnel Checkers

-------------------

[![Demo](demo/canvas_play.png)](https://youtu.be/DTkAF7T3rtM)

This is a Tunnel Checkers with AI player on one side, implemented in Python.

## Goal

The goal is as a complete game-play software that plays tunnel checkers with an opponent.  

## Properties

- GUI interface using tkinter
- Enable history "undo" for all steps
- No extra packages used
- Minimax & Alpha-Beta pruning with depth = 4 for searching moves

## Example
Start the game
```bash
python3 game.py
```
## Requirements

It requires Python3

No dependencies required.

## Installing Tunnel checkers

Run the following commands to clone the repository and install Tunnel Checkers:

```bash
git clone https://github.com/davidychen/TunnelCheckers.git
cd TunnelCheckers/
```

This will link the cloned directory to your local.

## Code

The library contains the following files:

- **game.py**: this file contains a the canvas including resizing, mouse and buttons interaction
  - **_Game_**: class for all GUI functions with a `__main__` to run
- **board.py**: this file contains all game rules
  - **_GameBoard_**: The GameBoard is represented by a 2D array with dimensions 8x8. The top-left corner is assigned (0,0), and the bottom right corner is assigned (7,7). Player one's pieces start at the top of the board (rows 0, 1, 2) and the forward direction of this player is indicated by successively increasing row numbers.  In contrast, player two's pieces start at the bottom (rows 5, 6, 7) and the forward direction of this player is indicated by successively decreasing row numbers.
  - **_Cell_**: Has type as determine the color of the cell and may or not contain a piece
  - **_Piece_**: With information about the position this piece is, which player it belongs to and whether it is a king
- **minimax.py**: The basic AI model to be used recursively searches the decision tree of the current game to a certain depth (e.g. when depth=4, predict 4 moves ahead in total), then comparing different paths in these trees and pick one that has the best payoff.
  - **Minimax**: Using Alpha-Beta to get more efficient calculation on minimax; Heuristic function by counting piece, giving bonus to king (before being a king, bonus to how close to other end), and bonus to all pieces if they stay closer to each other.
