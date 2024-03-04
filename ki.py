from ulab import numpy as np
import random

class KI:
    @staticmethod
    def _evaluate_window(window, player):
        score = 0
        opponent = -player

        summe_player = np.sum(np.equal(window, player))

        # Gewinn bewerten

        if summe_player == 4:
            score += 100
        elif summe_player == 3 and np.sum(np.equal(window, 0)) == 1:
            score += 50
        elif summe_player == 2 and np.sum(np.equal(window, 0)) == 2:
            score += 15

        # Gegner blocken

        if np.sum(np.equal(window, opponent)) == 3 and np.sum(np.equal(window, 0)) == 1:
            score -= 60
        elif np.sum(np.equal(window, opponent)) == 2 and np.sum(np.equal(window, 0)) == 2:
            score -= 30
    
       # Bonus für das Zentrum
        center_point = 3
        if window[center_point] == player:
            score += 10
    
        # Bonus für vertikale Verbindungen
        vertical_score = 0
        for i in range(len(window) - 1):
            if window[i] == player and window[i + 1] == player:
                vertical_score += 5
        score += vertical_score

        return score

    @staticmethod
    def _score_position(board, player):
        score = 0

        # Score center column
        center_array = board[:, 3]
        center_count = np.sum(center_array == player)
        score += center_count * 3

        # Score Horizontal
        for r in range(6):
            row_array = board[r, :]
            for c in range(4):
                window = row_array[c:c + 4]
                score += KI._evaluate_window(window, player)

        # Score Vertical
        for c in range(7):
            col_array = board[:, c]
            for r in range(3):
                window = col_array[r:r + 4]
                score += KI._evaluate_window(window, player)

        # Score positive diagonal
        for r in range(3):
            for c in range(4):
                window = [board[r + i][c + i] for i in range(4)]
                score += KI._evaluate_window(window, player)

        # Score negative diagonal
        for r in range(3):
            for c in range(4):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += KI._evaluate_window(window, player)

        return score

    @staticmethod
    def _is_valid_location(board, row, col):
        return board[row][col] == 0

    @staticmethod
    def _get_valid_locations(board):
        valid_locations = [col for col in range(7) if KI._is_valid_location(board, KI._get_next_open_row(board, col), col)]
        return valid_locations

    @staticmethod
    def _get_next_open_row(board, col):
        for r in range(5, -1, -1):
            if board[r][col] == 0:
                return r
        return -1

    @staticmethod
    def _is_terminal_node(board):
        return KI._check_winner(board, 1) or KI._check_winner(board, 2) or len(KI._get_valid_locations(board)) == 0

    @staticmethod
    def _minimax(board, depth, alpha, beta, maximizingPlayer):
        valid_locations = KI._get_valid_locations(board)

        is_terminal = KI._is_terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if KI._check_winner(board, 2):
                    return (None, 100000000000000)
                elif KI._check_winner(board, 1):
                    return (None, -100000000000000)
                else:
                    return (None, 0)
            else:
                return (None, KI._score_position(board, 2))

        if maximizingPlayer:
            value = -100000
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = KI._get_next_open_row(board, col)
                if row != -1:
                    temp_board = board.copy()
                    KI._drop_piece(temp_board, row, col, 2)
                    new_score = KI._minimax(temp_board, depth - 1, alpha, beta, False)[1]
                    if new_score > value:
                        value = new_score
                        column = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return column, value

        else:
            value = 100000
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = KI._get_next_open_row(board, col)
                if row != -1:
                    temp_board = board.copy()
                    KI._drop_piece(temp_board, row, col, 1)
                    new_score = KI._minimax(temp_board, depth - 1, alpha, beta, True)[1]
                    if new_score < value:
                        value = new_score
                        column = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return column, value

    @staticmethod
    def _drop_piece(board, row, col, piece):
        board[row][col] = piece

    @staticmethod
    def _check_winner(board, player):
        for c in range(4):
            for r in range(6):
                if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][c + 3] == player:
                    return True

        for c in range(7):
            for r in range(3):
                if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][c] == player:
                    return True

        for c in range(4):
            for r in range(3):
                if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
                    return True

        for c in range(4):
            for r in range(3, 6):
                if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
                    return True

        return False

    def get_spalte(self, board):
        depth = 2
        minimax = KI._minimax(board, depth, -100000000000000, 100000000000000, True)
        return minimax[0]
