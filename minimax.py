import math
from copy import deepcopy

class Minimax(object):
    DEPTH = 4
    def __init__(self, player):
        self.player = player
    
    def evaluate(self, currentTurn, board):
        scores = {board.PLAYER_ONE: 0,
                 board.PLAYER_TWO: 0}
        for player in [board.PLAYER_ONE, board.PLAYER_TWO]:
            pieces = board.pieces[player]
            if len(pieces) == 0:
                scores[player] = -1000000
                continue
            else:
                score = 0
                dist = 0
                for piece in pieces:
                    # basic score for each piece
                    score += 150
                    (row0, col0) = (piece.row, piece.col)
                    # for being king
                    if piece.is_king:
                        score += 100
                    else:
                        # how close to other side
                        if player == board.PLAYER_ONE:
                            score += (board.rows - row0 - 1) ** 2
                        else:
                            score += row0 ** 2
                    # how close each piece is to others
                    for piece1 in pieces:
                        (row1, col1) = (piece1.row, piece1.col)
                        drow = row1 - row0
                        dcol = min(abs(col1 - col0), abs(col1 - col0 + 8), abs(col1 - col0 - 8))
                        dist += math.sqrt(drow ** 2 + dcol ** 2)
                dist /= len(pieces)
                scores[player] = score - dist
        # return scores[board.PLAYER_TWO] - scores[board.PLAYER_ONE]
        if currentTurn == board.PLAYER_ONE:
            return scores[board.PLAYER_ONE] - scores[board.PLAYER_TWO]
        else:
            return scores[board.PLAYER_TWO] - scores[board.PLAYER_ONE]
    
    def alpha_beta(self, player, board, depth, alpha, beta):
        if depth >= Minimax.DEPTH or board.gameStatus != board.CONTINUING:
            return self.evaluate(self.player, board)

        actions = board.avail_actions(player)
        # Max
        if player == self.player:
            for action in actions:
                board_copy = deepcopy(board)
                board_copy.try_action(action)
                
                # Switch player
                player2 = board.switch_turn(player)
                board_copy.currentTurn = player2
                
                score = self.alpha_beta(player2, board_copy, depth + 1, alpha, beta)
                # Found a better solution
                if score > alpha:
                    if depth == 0:
                        self.best_action = action
                    alpha = score
                # then return alpha (cut off)
                if alpha > beta:
                    return alpha
            # This is the best action
            return alpha
        # Min
        else:
            for action in actions:
                board_copy = deepcopy(board)
                board_copy.try_action(action)
                
                # Switch player
                player2 = board.switch_turn(player)
                board_copy.currentTurn = player2
                
                score = self.alpha_beta(player2, board_copy, depth + 1, alpha, beta)
                # Opponent has found a worse action
                if score < beta:
                    beta = score
                # then return beta (cut off)
                if alpha >= beta:
                    return beta
            # This is the opponent's best action
            return beta
    
    def take_best(self, board):
        alpha = self.alpha_beta(self.player, board, 0, float('-inf'), float('+inf'))
        # No more actions
        if alpha == float('-inf'):
            board.concide()
        else:
            board.take_action(self.best_action)