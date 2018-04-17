# Main game using tkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from board import *
import math
import sys

class Game(Frame):
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Tunnel Checkers")
        self.parent.aspect(4,3,4,3)
        self.parent.minsize(600,450)
        super().__init__(parent, width = 600, height = 450)
        self.grid(row=0, column=0, sticky=(N, S, E, W), padx=20, pady=20)
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        # load data.xyz as appropriate
        self.rows = 8
        self.cols = 8
        self.margin = 10
        self.width = 600
        self.height = self.gridSize = 450
        self.timerDelay = 100
        self.gameOver = False
        self.otherTurn = False
        self.press_p = None
        self.press_x = -1
        self.press_y = -1
    
    def getCellBounds(self, row, col):
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = self.gridSize - 2*self.margin
        gridHeight = self.gridSize - 2*self.margin
        x0 = self.margin + gridWidth * col / self.cols
        x1 = self.margin + gridWidth * (col+1) / self.cols
        y0 = self.margin + gridHeight * row / self.rows
        y1 = self.margin + gridHeight * (row+1) / self.rows
        return (x0, y0, x1, y1)
    
    def getPieceBounds(self, row, col):
        (x0, y0, x1, y1) = self.getCellBounds(row, col)
        x_diff = (x1 - x0) / 5
        y_diff = (y1 - y0) / 5
        return (x0 + x_diff, y0 + y_diff, x1 - x_diff, y1 - y_diff)
    
    def pointInGrid(self, x, y):
        # return True if (x, y) is inside the grid defined by data.
        return ((self.margin <= x <= self.gridSize-self.margin) and
                (self.margin <= y <= self.gridSize-self.margin))
    
    def getCell(self, x, y):
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not self.pointInGrid(x, y)):
            return (-1, -1)
        gridWidth  = self.gridSize - 2*self.margin
        gridHeight = self.gridSize - 2*self.margin
        cellWidth  = gridWidth / self.cols
        cellHeight = gridHeight / self.rows
        row = int((y - self.margin) / cellHeight)
        col = int((x - self.margin) / cellWidth)
        # triple-check that we are in bounds
        row = min(self.rows-1, max(0, row))
        col = min(self.cols-1, max(0, col))
        return (row, col)
    
    def getSmallCell(self, x, y):
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not self.pointInGrid(x, y)):
            return (-1, -1)
        gridWidth  = self.gridSize - 2*self.margin
        gridHeight = self.gridSize - 2*self.margin
        cellWidth  = gridWidth / self.cols
        cellHeight = gridHeight / self.rows
        row = int((y - self.margin) / cellHeight)
        col = int((x - self.margin) / cellWidth)
        # triple-check that we are in bounds
        row = min(self.rows-1, max(0, row))
        col = min(self.cols-1, max(0, col))
        if ((row >= 0) and (col >= 0)):
            x0 = self.margin + (col + 1/5) * cellWidth
            x1 = self.margin + (col + 1 - 1/5) * cellWidth
            y0 = self.margin + (row + 1/5) * cellHeight
            y1 = self.margin + (row + 1 - 1/5) * cellHeight
            if ((x0 <= x <= x1) and (y0 <= y <= y1)):
                return (row, col)
        return (-1, -1)
    
    def distance(self, x0, y0, x1, y1):
        return math.sqrt( (x1 - x0)**2 + (y1 - y0)**2 )
    
    def getPieceInCell(self, x, y):
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not self.pointInGrid(x, y)):
            return (-1, -1)
        gridWidth  = self.gridSize - 2*self.margin
        gridHeight = self.gridSize - 2*self.margin
        cellWidth  = gridWidth / self.cols
        cellHeight = gridHeight / self.rows
        row = int((y - self.margin) / cellHeight)
        col = int((x - self.margin) / cellWidth)
        # triple-check that we are in bounds
        row = min(self.rows-1, max(0, row))
        col = min(self.cols-1, max(0, col))
        if ((row >= 0) and (col >= 0)):
            mid_x = self.margin + (col + 0.5) * cellWidth
            mid_y = self.margin + (row + 0.5) * cellHeight
            if (self.distance(x, y, mid_x, mid_y) > cellWidth / 10 * 3):
                return (-1, -1)
        return (row, col)
    
    def getPieceCoords(self, x, y):
        gridWidth  = self.gridSize - 2*self.margin
        gridHeight = self.gridSize - 2*self.margin
        cellWidth  = gridWidth / self.cols * 3 / 10
        cellHeight = gridHeight / self.rows * 3 / 10
        x0 = x - cellWidth
        x1 = x + cellWidth
        y0 = y - cellHeight
        y1 = y + cellHeight
        return (x0, y0, x1, y1)
    
    def drawBoard(self):
        # Background color
        self.board_canvas.create_rectangle(0, 
                                0,
                                 self.gridSize , 
                                 self.gridSize, 
                                fill="wheat3", outline="")
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
                cell = self.board.cells[row][col]
                self.board_canvas.create_rectangle(x0, y0, x1, y1, fill=cell.color, outline="", tags = cell.type)
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board.cells[row][col]
                if cell.piece is not None:
                    color = "black" if cell.piece.player == GameBoard.PLAYER_ONE else "white"
                    if cell.piece.pressed:
                        (x0, y0, x1, y1) = self.getPieceCoords(cell.piece.x, cell.piece.y)
                    else:
                        (x0, y0, x1, y1) = self.getPieceBounds(row, col)
                    self.board_canvas.create_oval(x0, y0, x1, y1, fill=color, outline="black", tags = "piece")
                    if cell.piece.is_king:
                        self.create_star(x0, y0, x1, y1, self.board_canvas)
        fontSize = math.floor(self.gridSize / self.cols / 2)
        if self.gameOver:
            self.board_canvas.create_text(self.gridSize/2, self.gridSize/2, text="Game Over!",
                                    font="Arial "+str(fontSize)+" bold", fill="darkBlue")
    
    def drawGameOver(self):
        self.board_canvas.create_text(self.gridSize/2, self.gridSize/2, text="Game Over",
                                    font="Arial 25 bold", fill="darkBlue")
    
    def drawMenu(self):
        piece_x = piece_y = self.gridSize / self.cols / 2
        piece_color = 'black' if self.board.currentTurn == GameBoard.PLAYER_ONE else 'white'
        
        dTextY = math.floor(piece_y + 20)
        fontSize = dTextY - 25
        
        mid_x = self.gridSize / 3 / 2
        all_x = self.margin
        # line 1
        this_y = self.gridSize / self.rows
        if not self.gameOver:
            self.menu_canvas.create_oval(all_x, this_y, all_x + piece_x, this_y + piece_y, fill=piece_color, outline = 'black')
            self.menu_canvas.create_text(all_x + piece_x * 1.2, this_y + piece_y, text="'s Turn",
                                    font="Arial "+str(fontSize)+" bold", fill="darkBlue", anchor="sw")
        else:
            if self.board.gameStatus == GameBoard.PLAYER_ONE_WIN or self.board.gameStatus == GameBoard.PLAYER_TWO_WIN:
                piece_color = 'black' if self.board.gameStatus == GameBoard.PLAYER_ONE else 'white'
                self.menu_canvas.create_oval(all_x, this_y, all_x + piece_x, this_y + piece_y, fill=piece_color, outline = 'black')
                self.menu_canvas.create_text(all_x + piece_x * 1.2, this_y + piece_y, text=" WINS!",
                                        font="Arial "+str(fontSize)+" bold", fill="darkBlue", anchor="sw")
            elif self.board.gameStatus == GameBoard.DRAW:
                self.menu_canvas.create_text(all_x, this_y + piece_y, text="DRAW!",
                                    font="Arial "+str(fontSize)+" bold", fill="darkBlue", anchor="sw")
        # line 2
        this_y += dTextY * 2
        fontSize = math.floor(fontSize*0.8)
        self.menu_canvas.create_text(all_x + mid_x, this_y + piece_y, text="Turn: "+str(self.board.turnCount),
                         font="Arial "+str(fontSize)+" bold", fill="darkBlue")
        # line 3
        this_y += dTextY * 2
        piece_x *= 0.8
        piece_y *= 0.8
        self.menu_canvas.create_oval(all_x, this_y, all_x + piece_x, this_y + piece_y, fill='black', outline = 'black')
        self.menu_canvas.create_text(all_x + piece_x * 1.4, this_y + piece_y, text="X "+str(self.board.nPieces[GameBoard.PLAYER_ONE]),
                         font="Arial "+str(fontSize)+" bold", fill="darkBlue", anchor="sw")
        self.menu_canvas.create_oval(all_x + mid_x, this_y, all_x + piece_x + mid_x, this_y + piece_y, fill='black', outline = 'black')
        self.create_star(all_x + mid_x, this_y, all_x + piece_x + mid_x, this_y + piece_y, self.menu_canvas)
        self.menu_canvas.create_text(all_x + piece_x * 1.4 + mid_x, this_y + piece_y, text="X "+str(self.board.nKings[GameBoard.PLAYER_ONE]),
                         font="Arial "+str(fontSize)+" bold", fill="darkBlue", anchor="sw")
        # line 3
        this_y += dTextY
        self.menu_canvas.create_oval(all_x, this_y, all_x + piece_x, this_y + piece_y, fill='white', outline = 'black')
        self.menu_canvas.create_text(all_x + piece_x * 1.4, this_y + piece_y, text="X "+str(self.board.nPieces[GameBoard.PLAYER_TWO]),
                         font="Arial "+str(fontSize)+" bold", fill="darkBlue", anchor="sw")
        self.menu_canvas.create_oval(all_x + mid_x, this_y, all_x + piece_x + mid_x, this_y + piece_y, fill='white', outline = 'black')
        self.create_star(all_x + mid_x, this_y, all_x + piece_x + mid_x, this_y + piece_y, self.menu_canvas)
        self.menu_canvas.create_text(all_x + piece_x * 1.4 + mid_x, this_y + piece_y, text="X "+str(self.board.nKings[GameBoard.PLAYER_TWO]),
                         font="Arial "+str(fontSize)+" bold", fill="darkBlue", anchor="sw")
    
    def create_star(self, x0, y0, x1, y1, canvas, fill = "orange", outline = ""):
        width = x1 - x0
        height = y1 - y0
        (cx, cy, r) = ((x0 + x1)/2, (y0 + y1)/2, min(width, height)/2)
        r *= 0.85
        verts = []
        for i in range(10):
            angle = math.pi/2 - (2*math.pi)*(i/10)
            rate = 0.5 if i%2==0 else 1
            verts.append(cx + r * rate * math.cos(angle))
            verts.append(cy + r * rate * math.sin(angle))
        canvas.create_polygon(verts, fill=fill, outline=outline)
    
    def mousePressed(self, event):
        if self.otherTurn or self.gameOver:
            return
        # use event.x and event.y
        (row, col) = self.getPieceInCell(event.x, event.y)
        if ((row < 0) or (col < 0)):
            return
        self.press_x = event.x
        self.press_y = event.y
        piece = self.board.get_piece(row, col)
        if piece is not None:
            piece.x = event.x
            piece.y = event.y
            piece.pressed = True
            self.press_p = piece
    
    def mouseMoved(self, event):
        if self.otherTurn or self.gameOver:
            return
        if self.press_p is not None:
            self.press_p.x = event.x
            self.press_p.y = event.y
    
    def mouseReleased(self, event):
        if self.otherTurn or self.gameOver:
            return
        if self.press_p is None:
            return
        piece = self.press_p
        self.press_x = -1
        self.press_y = -1
        self.press_p.pressed = False
        self.press_p = None
        (row, col) = self.getSmallCell(event.x, event.y)
        if((row<0) or (col<0)):
            return
        elif self.board.get_cell(row, col).type == "white_cell":
            return
        self.board.place(piece.row, piece.col, row, col)
        
    def keyPressed(self, event):
        # use event.char and event.keysym
        pass
    
    def undoPressed(self):
        self.board.undo()
    
    def resetPressed(self):
        self.board = GameBoard()
    
    def redrawAll(self):
        if self.board.gameStatus != GameBoard.CONTINUING:
            self.gameOver = True
        else:
            self.gameOver = False
        if self.board.currentTurn != GameBoard.PLAYER_ONE:
            # TODO for test now!!!
            self.otherTurn = True
        else:
            self.otherTurn = False
        self.drawBoard()
        self.drawMenu()
        
    def redrawAllWrapper(self):
        def redrawOneWrapper(canvas):
            canvas.delete(ALL)
            canvas.create_rectangle(0, 0, canvas.winfo_width(), 
                            canvas.winfo_height(), 
                            fill='white', width=0)
        def update(canvas):
            canvas.update()
        
        for canvas in [self.board_canvas, self.menu_canvas]:
            redrawOneWrapper(canvas)
        self.redrawAll()
        for canvas in [self.board_canvas, self.menu_canvas]:
            update(canvas)
    
    def mousePressedWrapper(self, event):
        self.mousePressed(event)
        self.redrawAllWrapper()
    
    def mouseMovedWrapper(self, event):
        self.mouseMoved(event)
        self.redrawAllWrapper()
    
    def mouseReleasedWrapper(self, event):
        self.mouseReleased(event)
        self.redrawAllWrapper()

    def keyPressedWrapper(self, event):
        self.keyPressed(event)
        self.redrawAllWrapper()
    
    def resizeWrapper(self, event):
        self.width = event.width
        self.height = event.height
        self.recal_size()
        self.redrawAllWrapper()
    
    def undoWrapper(self):
        self.undoPressed()
        self.redrawAllWrapper()
    
    def resetWrapper(self):
        self.resetPressed()
        self.redrawAllWrapper()
    
    def recal_size(self):
        self.gridSize  = self.height
        self.board_frame.place(in_=self, x=0, y=0, 
            width=self.gridSize, height=self.gridSize)
        self.menu_frame.place(in_=self, x=self.gridSize, y=0, 
           width=self.gridSize/3, height=self.gridSize)
    
    def run(self):
        self.board = GameBoard()
        self.board_frame = Frame(self)
        self.menu_frame = Frame(self)
        
        # create the root and the canvas
        self.board_canvas = Canvas(self.board_frame)
        self.board_canvas.pack(fill=BOTH, expand=YES)
        
        self.menu_canvas = Canvas(self.menu_frame)
        self.menu_canvas.pack(fill=BOTH, expand=YES)
        
        self.undo = tk.Button(self.menu_frame, text="Undo", command = self.undoWrapper)
        self.reset = tk.Button(self.menu_frame, text="Reset", command = self.resetWrapper)
        
        self.undo.pack()
        self.reset.pack()
        
        # set up events
        self.board_canvas.bind("<Button-1>", lambda event:
                                self.mousePressedWrapper(event))
        self.board_canvas.bind("<B1-Motion>", lambda event:
                                self.mouseMovedWrapper(event))
        self.board_canvas.bind("<ButtonRelease-1>", lambda event:
                                self.mouseReleasedWrapper(event))
        self.parent.bind("<Key>", lambda event:
                                self.keyPressedWrapper(event))
        self.bind("<Configure>", lambda event:
                                self.resizeWrapper(event))
        
        self.redrawAll()
        self.parent.mainloop()
        print("bye!")
        

def main():
    root = Tk()
    g = Game(root)
    g.run()

if __name__ == '__main__':
    main()