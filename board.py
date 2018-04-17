from minimax import *

class GameBoard(object):
    PLAYER_ONE          = 1
    PLAYER_TWO          = 2
    ABS_TOP_LEFT        = (-1,  -1)
    ABS_TOP_RIGHT       = (-1,   1)
    ABS_BOTTOM_LEFT     = ( 1,  -1)
    ABS_BOTTOM_RIGHT    = ( 1,   1)
    NOCAP_DRAW_TURNS    = 100
    PLAYER_ONE_WIN      = PLAYER_ONE
    PLAYER_TWO_WIN      = PLAYER_TWO
    DRAW                = -1
    CONTINUING          = 0
    
    def FORWARD_LEFT(self):
        return GameBoard.ABS_TOP_LEFT \
                    if self.currentTurn == GameBoard.PLAYER_ONE \
                    else GameBoard.ABS_BOTTOM_RIGHT
    
    def FORWARD_RIGHT(self):
        return GameBoard.ABS_TOP_RIGHT \
                    if self.currentTurn == GameBoard.PLAYER_ONE \
                    else GameBoard.ABS_BOTTOM_LEFT
    
    def BACKWARD_LEFT(self):
        return GameBoard.ABS_BOTTOM_LEFT \
                    if self.currentTurn == GameBoard.PLAYER_ONE \
                    else GameBoard.ABS_TOP_RIGHT
    
    def BACKWARD_RIGHT(self):
        return GameBoard.ABS_BOTTOM_RIGHT \
                    if self.currentTurn == GameBoard.PLAYER_ONE \
                    else GameBoard.ABS_TOP_LEFT
    
    def __init__(self, rows = 8, cols = 8, cells = None):
        self.rows = rows
        self.cols = cols
        self.currentTurn = GameBoard.PLAYER_ONE
        self.cells = self.make2dList(rows, cols)
        self.pieces = {GameBoard.PLAYER_ONE:[], GameBoard.PLAYER_TWO:[]}
        self.nPieces = {GameBoard.PLAYER_ONE:0, GameBoard.PLAYER_TWO:0}
        self.nKings = {GameBoard.PLAYER_ONE:0, GameBoard.PLAYER_TWO:0}
        self.turnCount = 0
        self.restrictedPieces = []
        self.jumpPossible = False
        self.lastCapture = -1
        self.currentHistory = {"move":[],"jump":[],"delete":[]}
        self.history = []
        self.set_cells()
        self.gameStatus = GameBoard.CONTINUING
        self.bot = Minimax(GameBoard.PLAYER_TWO)
        # self.set_test_cells2()
    
    def set_test_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 0:
                    cell = Cell("white_cell")
                else:
                    cell = Cell("black_cell")
                    if (row, col) in [(3, 2), (1,4), (3,6), (6, 1),(6,7), (1,6), (3,0)]:
                        cell.piece = Piece(row, col, GameBoard.PLAYER_TWO)
                        self.pieces[GameBoard.PLAYER_TWO].append(cell.piece)
                    elif (row, col) in [(4, 1), (4,5),(6,3),(1,0)]:
                        cell.piece = Piece(row, col, GameBoard.PLAYER_ONE)
                        self.pieces[GameBoard.PLAYER_ONE].append(cell.piece)
                self.cells[row][col] = cell
        self.update_count()
    
    def set_test_cells2(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 0:
                    cell = Cell("white_cell")
                else:
                    cell = Cell("black_cell")
                    if (row, col) in [(6,1), (5,4), (3,2)]:
                        cell.piece = Piece(row, col, GameBoard.PLAYER_TWO)
                        self.pieces[GameBoard.PLAYER_TWO].append(cell.piece)
                    elif (row, col) in [(1,4), (6,7)]:
                        cell.piece = Piece(row, col, GameBoard.PLAYER_ONE)
                        self.pieces[GameBoard.PLAYER_ONE].append(cell.piece)
                self.cells[row][col] = cell
        self.update_count()
    
    def set_test_cells3(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 0:
                    cell = Cell("white_cell")
                else:
                    cell = Cell("black_cell")
                    if (row, col) in [(5,2)]:
                        cell.piece = Piece(row, col, GameBoard.PLAYER_TWO)
                        cell.piece.is_king = True
                        self.pieces[GameBoard.PLAYER_TWO].append(cell.piece)
                    elif (row, col) in [(3,2)]:
                        cell.piece = Piece(row, col, GameBoard.PLAYER_ONE)
                        cell.piece.is_king = True
                        self.pieces[GameBoard.PLAYER_ONE].append(cell.piece)
                self.cells[row][col] = cell
        self.update_count()
    
    def set_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 0:
                    cell = Cell("white_cell")
                else:
                    cell = Cell("black_cell")
                    if row < self.rows / 2 - 1:
                        cell.piece = Piece(row, col, GameBoard.PLAYER_TWO)
                        self.pieces[GameBoard.PLAYER_TWO].append(cell.piece)
                    elif row > self.rows / 2:
                        cell.piece = Piece(row, col, GameBoard.PLAYER_ONE)
                        self.pieces[GameBoard.PLAYER_ONE].append(cell.piece)
                self.cells[row][col] = cell
        self.update_count()
    
    def make2dList(self, rows, cols):
        a=[]
        for row in range(rows): a += [[0]*cols]
        return a
    
    def switch_turn(self, player):
        return GameBoard.PLAYER_ONE \
                if player == GameBoard.PLAYER_TWO \
                else GameBoard.PLAYER_TWO
    
    def update_count(self):
        for player in [GameBoard.PLAYER_ONE, GameBoard.PLAYER_TWO]:
            self.nPieces[player] = sum((not x.is_king) for x in self.pieces[player])
            self.nKings[player] = sum(x.is_king for x in self.pieces[player])
    
    def delete_piece_coord(self, row, col):
        """
        Delete the piece by coord:
        return if is None
        Else:   1) set piece to (-1, -1)
                2) nPiece--
                3) add piece to history
                4) set cell.piece to None
        """
        piece = self.cells[row][col].piece
        if piece is not None:
            piece.set_coord(-1, -1)
            self.pieces[piece.player].remove(piece)
            self.update_count()
            self.currentHistory["delete"].append(piece)
            self.cells[row][col].piece = None
    
    def delete_piece(self, *args):
        """
        Delete piece by object
        call delete_piece_coord()
        """
        if len(args) == 1 and isinstance(args[0],Piece):
            piece = args[0]
            row = piece.row
            col = piece.col
            self.delete_piece_coord(row, col)
        elif len(args) == 2 and isinstance(args[0],int) and isinstance(args[1],int):
            self.delete_piece_coord(args[0], args[1])
    
    def concide(self):
        self.gameStatus = self.switch_turn(self.currentTurn)
    
    def check_win(self):
        if self.nPieces[GameBoard.PLAYER_ONE] + self.nKings[GameBoard.PLAYER_ONE] == 0:
            self.gameStatus = GameBoard.PLAYER_TWO_WIN
        elif self.nPieces[GameBoard.PLAYER_TWO] + self.nKings[GameBoard.PLAYER_TWO] == 0:
            self.gameStatus = GameBoard.PLAYER_ONE_WIN
        elif self.turnCount >= GameBoard.NOCAP_DRAW_TURNS:
            self.gameStatus = GameBoard.DRAW
        else:
            self.gameStatus = GameBoard.CONTINUING
        return self.gameStatus
    
    def process_turn(self):
        self.check_win()
    
    def resign(self):
        self.history.append(self.currentHistory)
        self.currentHistory = {"move":[],"jump":[],"delete":[]}
        self.currentTurn = GameBoard.PLAYER_ONE \
                if self.currentTurn == GameBoard.PLAYER_TWO \
                else GameBoard.PLAYER_TWO
        self.update_count()
        self.turnCount += 1
        if self.currentTurn == GameBoard.PLAYER_TWO:
            self.bot.take_best(self)
    
    def undo(self):
        self.undo1()
        if self.turnCount % 2 != 0:
            self.undo1()
        
    def undo1(self):
        if len(self.history) > 0:
            last = self.history.pop()
            for group in ["move", "jump", "delete"]:
                for piece in last[group]:
                    if group in ["move", "jump"]:
                        self.cells[piece.row][piece.col].piece = None
                        piece.undo()
                        self.cells[piece.row][piece.col].piece = piece
                    else:
                        piece.undo()
                        self.pieces[piece.player].append(piece)
                        self.cells[piece.row][piece.col].piece = piece
                    self.update_count()
            self.currentTurn = GameBoard.PLAYER_ONE \
                    if self.currentTurn == GameBoard.PLAYER_TWO \
                    else GameBoard.PLAYER_TWO
            self.turnCount -= 1
        self.check_win()
    
    def get_pieces(self):
        return self.cells
    
    def add_dir(self, row, col, direction):
        if abs(direction[0]) != abs(direction[1]):
            raise ValueError("|directions[0]| != |direction[1]|")
        (rowx, colx) = tuple(map(lambda x, y: x + y, (row, col), direction))
        if (rowx <0) or (rowx >= self.rows):
            raise ValueError("Move out of board")
        colx %= self.cols
        return (rowx, colx)
    
    def get_dirs(self, row, col, goalRow, goalCol):
        """
        From (r,c) to (r', c'), which direction should it take?
        may be more than 1
        """
        row_diff = goalRow - row
        if row_diff == 0:
            return []
        col_norm = goalCol - col
        col_pass = goalCol - col - self.cols \
                if 0 <= abs(goalCol - col - self.cols) < self.cols \
                else goalCol - col + self.cols
        dirs = []
        for col_diff in [col_norm, col_pass]:
            if abs(row_diff) == abs(col_diff):
                dirs.append((row_diff, col_diff))
        return dirs

    def is_valid_jump_coord(self, row, col, goalRow, goalCol, pieces_to_delete = None):
        dirs = self.get_dirs(row, col, goalRow, goalCol)
        if len(dirs) == 0:
            return False
        for dir in dirs:
            if self.is_valid_jump_dir(row, col, dir, pieces_to_delete):
                return True
        return False
    
    def is_valid_jump_dir(self, row, col, direction, pieces_to_delete = None):
        """
        Whether this coor's direction can get moved (FOR JUMP)
        """
        piece = self.get_piece(row, col)
        if piece is None or piece.player != self.currentTurn:
            return False
        dir0 = abs(direction[0])
        dir1 = abs(direction[1])
        if dir0 != dir1 or dir0 == 0:
            return False
        if dir0 % 2 != 0:
            return False
        directions = [self.FORWARD_LEFT(), self.FORWARD_RIGHT()]
        if piece.is_king:
            directions += [self.BACKWARD_LEFT(), self.BACKWARD_RIGHT()]
        unit_dir = tuple(dir // dir0 for dir in direction)
        if unit_dir not in directions:
            return False
        rowx = row + direction[0]
        if rowx < 0 or rowx >= self.rows:
            return False
        for i in (unit + 1 for unit in range(dir0)):
            temp_dir = tuple(dir * i for dir in unit_dir)
            try:
                (rowx, colx) = self.add_dir(row, col, temp_dir)
            except ValueError:
                return False
            mid_piece = self.get_piece(rowx, colx)
            if i % 2 == 0 and mid_piece is not None:
                return False
            elif i % 2 != 0:
                if mid_piece is None or mid_piece.player == piece.player:
                    return False
            if pieces_to_delete is not None:
                pieces_to_delete.append(mid_piece)
        return True
    
    def is_valid_move_coord(self, row, col, goalRow, goalCol):
        dirs = self.get_dirs(row, col, goalRow, goalCol)
        if len(dirs) == 0:
            return False
        for dir in dirs:
            if self.is_valid_move_dir(row, col, dir):
                return True
        return False
        pass
    
    def is_valid_move_dir(self, row, col, direction):
        piece = self.get_piece(row, col)
        if piece is None or piece.player != self.currentTurn:
            return False
        directions = [self.FORWARD_LEFT(), self.FORWARD_RIGHT()]
        if piece.is_king:
            directions += [self.BACKWARD_LEFT(), self.BACKWARD_RIGHT()]
        if direction in directions:
            try:
                (rowx, colx) = self.add_dir(row, col, direction)
            except ValueError:
                return False
            piece = self.get_piece(rowx, colx)
            if piece is None:
                return True
        return False
    
    def move_dir(self, row, col, direction):
        if self.is_valid_move_dir(row, col, direction):
            try:
                (goalRow, goalCol) = self.add_dir(row, col, direction)
                self.move_success(row, col, goalRow, goalCol)
                return True
            except ValueError:
                return False
    
    def move_coord(self, row, col, goalRow, goalCol):
        if self.is_valid_move_coord(row, col, goalRow, goalCol):
            self.move_success(row, col, goalRow, goalCol)
            return True
        return False
    
    def move_success(self, row, col, goalRow, goalCol):
        piece = self.get_piece(row, col)
        if piece.player != self.currentTurn:
            return
        self.check_king(piece, goalRow)
        piece.set_coord(goalRow, goalCol)
        self.currentHistory["move"].append(piece)
        self.cells[row][col].piece = None
        self.cells[goalRow][goalCol].piece = piece
        self.process_turn()
        
    def move(self, *args):
        if len(args) == 3 and isinstance(args[0],int) \
                            and isinstance(args[1],int) \
                            and isinstance(args[2],tuple):
            return self.move_dir(args[0], args[1], args[2])
        elif len(args) == 4 and isinstance(args[0],int) \
                            and isinstance(args[1],int) \
                            and isinstance(args[2],int) \
                            and isinstance(args[3],int):
            return self.move_coord(args[0], args[1], args[2], args[3])
    
    def jump_dir(self, row, col, direction):
        pieces_to_delete = []
        if not self.is_valid_jump_dir(row, col, direction, pieces_to_delete):
            return False
        try:
            (goalRow, goalCol) = self.add_dir(row, col, direction)
        except ValueError:
            return False
        self.jump_success(row, col, goalRow, goalCol, pieces_to_delete)
        return True
        
    def jump_coord(self, row, col, goalRow, goalCol):
        dirs = self.get_dirs(row, col, goalRow, goalCol)
        if len(dirs) == 0:
            return False
        for dir in dirs:
            if self.is_valid_jump_dir(row, col, dir):
                return self.jump_dir(row, col, dir)
        return False
    
    def jump(self, *args):
        if len(args) == 3 and isinstance(args[0],int) \
                            and isinstance(args[1],int) \
                            and isinstance(args[2],tuple):
            return self.jump_dir(args[0], args[1], args[2])
        elif len(args) == 4 and isinstance(args[0],int) \
                            and isinstance(args[1],int) \
                            and isinstance(args[2],int) \
                            and isinstance(args[3],int):
            return self.jump_coord(args[0], args[1], args[2], args[3])
    
    def jump_success(self, row, col, goalRow, goalCol, pieces_to_delete):
        piece = self.get_piece(row, col)
        self.check_king(piece, goalRow)
        piece.set_coord(goalRow, goalCol)
        self.currentHistory["jump"].append(piece)
        self.cells[row][col].piece = None
        self.cells[goalRow][goalCol].piece = piece
        for mid_piece in pieces_to_delete:
            self.delete_piece(mid_piece)
        self.pieces_to_delete = []
        self.process_turn()
    
    def check_king(self, piece, goalRow):
        if not piece.is_king:
            if (piece.player == GameBoard.PLAYER_ONE and goalRow == 0):
                piece.make_king()
                self.nKings[piece.player] = sum(x.is_king for x in self.pieces[piece.player])
            if (piece.player == GameBoard.PLAYER_TWO and goalRow == self.rows - 1):
                piece.make_king()
                self.nKings[piece.player] = sum(x.is_king for x in self.pieces[piece.player])
    
    def get_piece(self, row, col):
        return self.cells[row][col].piece
    
    def get_cell(self, row, col):
        return self.cells[row][col]
    
    def place(self, row0, col0, row1, col1):
        if ((row0 ==row1) and (col0 == col1)):
            return False
        if not self.move(row0, col0, row1, col1):
            if not self.jump(row0, col0, row1, col1):
                return
        self.resign()
    
    def take_action(self, action):
        """
        ONLY if it's successful!
        """
        self.try_action(action)
        self.resign()
    
    def try_action(self, action):
        """
        ONLY if it's successful!
        """
        (row, col, direction) = action
        if abs(direction[0]) == 1:
            self.move_dir(row, col, direction)
        else:
            self.jump_dir(row, col, direction)
    
    def avail_actions(self, player):
        actions = []
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                if cell.piece is not None and cell.piece.player == player:
                    directions = [self.FORWARD_LEFT(), self.FORWARD_RIGHT()]
                    if cell.piece.is_king:
                        directions += [self.BACKWARD_LEFT(), self.BACKWARD_RIGHT()]
                    for direction in directions:
                        if self.is_valid_move_dir(row, col, direction):
                            actions.append((row, col, direction))
                        else:
                            for i in range(2, self.rows, 2):
                                direction_jump = tuple(x * i for x in direction)
                                if self.is_valid_jump_dir(row, col, direction_jump):
                                    actions.append((row, col, direction_jump))
                                else:
                                    break
        return actions
    
    def print_board(self):
        lines = []
        lines.append("____"*self.cols)
        for row in range(self.rows):
            line = []
            for col in range(self.cols):
                cell = self.cells[row][col]
                if cell.piece is not None:
                    line.append("_X_" if cell.piece.player == GameBoard.PLAYER_ONE \
                                else "_O_")
                else:
                    line.append("___")
            line = "|" + "|".join(line) + "|"
            lines.append(line)
        print("\n".join(lines))
            
    
    
class Cell(object):
    def __init__(self, type):
        self.type = type
        self.color = "wheat1" if type == "white_cell" else "wheat4"
        self.piece= None

class Piece(object):
    BLACK = 1
    WHITE = 2
    def __init__(self, row, col, player):
        self.col = col
        self.row = row
        self.player = player
        self.is_king = False
        self.history = []
        self.pressed = False
        self.x = None
        self.y = None
        self.king_changed = False
    
    def make_king(self):
        self.is_king = True
        self.king_changed = True
    
    def set_coord(self, row, col):
        self.history.append((self.row, self.col, self.king_changed))
        self.col = col
        self.row = row
        self.king_changed = False
    
    def undo(self):
        if len(self.history) > 0:
            (self.row, self.col, self.king_changed) = self.history.pop()
            if self.king_changed:
                self.is_king = False
        
    def __repr__(self):
        #useful for debugging
        type = 'k' if self.is_king else 'p'
        return 'P'+str(self.player)+','+type+'('+str(self.col)+','+str(self.row)+')'

