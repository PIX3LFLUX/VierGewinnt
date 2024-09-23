import numpy as np
import random
from multiprocessing import Pool, cpu_count
from functools import lru_cache

Inf = 1000000

class KI:
    
    transposition_table = {}

    @staticmethod
    def _evaluate_window(window, player):
        score = 0
        opponent = 3 - player  # Annahme: Spieler 1 and 2

        summe_player = np.sum(np.equal(window, player))
        summe_opponent = np.sum(np.equal(window, opponent))

        if summe_player == 4:
            score += 10000  # Direkter Gewinn
        elif summe_player == 3 and np.sum(np.equal(window, 0)) == 1:
            score += 100  # Drei in einer Reihe mit einer offenen Stelle
        elif summe_player == 2 and np.sum(np.equal(window, 0)) == 2:
            score += 10  # Zwei in einer Reihe mit zwei offenen Stellen
          
        if summe_opponent == 3 and np.sum(np.equal(window, 0)) == 1:
            score -= 120  # Gegner blockieren
        elif summe_opponent == 2 and np.sum(np.equal(window, 0)) == 2:
            score -= 60

        return score

    @staticmethod
    def _score_position(board, player):
        score = 0

        center_array = [int(i) for i in list(board[:, 3])]
        center_count = center_array.count(player)
        score += center_count * 6

        for r in range(6):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(4):
                window = row_array[c:c + 4]
                score += KI._evaluate_window(window, player)

        for c in range(7):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(3):
                window = col_array[r:r + 4]
                score += KI._evaluate_window(window, player)

        for r in range(3):
            for c in range(4):
                window = [board[r + i][c + i] for i in range(4)]
                score += KI._evaluate_window(window, player)

        for r in range(3):
            for c in range(4):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += KI._evaluate_window(window, player)
        
        return score

    @staticmethod
    def _is_valid_location(board, col):
        return board[0][col] == 0

    @staticmethod
    def _get_valid_locations(board):
        valid_locations = [col for col in range(7) if KI._is_valid_location(board, col)]
        return sorted(valid_locations, key=lambda x: abs(x - 3))  # Mitte bevorzugen

    @staticmethod
    def _get_next_open_row(board, col):
        for r in range(5, -1, -1):
            if board[r][col] == 0:
                return r
        return -1  # Spalte ist voll

    @staticmethod
    def _is_terminal_node(board):
        return KI._check_winner(board, 1) or KI._check_winner(board, 2) or len(KI._get_valid_locations(board)) == 0

    @staticmethod
    def _opponent_is_threatening(board, opponent):
        """Überprüft, ob der Gegner kurz davor ist, zu gewinnen."""
        for col in KI._get_valid_locations(board):
            row = KI._get_next_open_row(board, col)
            temp_board = board.copy()
            KI._drop_piece(temp_board, row, col, opponent)
            if KI._check_winner(temp_board, opponent):
                return True
        return False

    @staticmethod
    def _check_immediate_win(board, player):
        """Überprüft, ob der Spieler mit dem nächsten Zug gewinnen kann."""
        for col in KI._get_valid_locations(board):
            row = KI._get_next_open_row(board, col)
            temp_board = board.copy()
            KI._drop_piece(temp_board, row, col, player)
            if KI._check_winner(temp_board, player):
                return col
        return None

    @staticmethod
    @lru_cache(maxsize=None)
    def _minimax(board_tuple, depth, alpha, beta, maximizingPlayer):
        board = np.array(board_tuple)
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

        # Sofortige Gewinnüberprüfung
        immediate_win = KI._check_immediate_win(board, 2 if maximizingPlayer else 1)
        if immediate_win is not None:
            return immediate_win, 100000000000000 if maximizingPlayer else -100000000000000

        if maximizingPlayer:
            value = -Inf
            best_column = random.choice(valid_locations)
            best_moves = []

            for col in valid_locations:
                row = KI._get_next_open_row(board, col)
                temp_board = board.copy()
                KI._drop_piece(temp_board, row, col, 2)
                new_score = KI._minimax(tuple(map(tuple, temp_board)), depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    best_moves = [col]
                elif new_score == value:
                    best_moves.append(col)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return random.choice(best_moves) if best_moves else best_column, value

        else:
            value = Inf
            best_column = random.choice(valid_locations)
            best_moves = []

            for col in valid_locations:
                row = KI._get_next_open_row(board, col)
                temp_board = board.copy()
                KI._drop_piece(temp_board, row, col, 1)
                new_score = KI._minimax(tuple(map(tuple, temp_board)), depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    best_moves = [col]
                elif new_score == value:
                    best_moves.append(col)
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return random.choice(best_moves) if best_moves else best_column, value

    @staticmethod
    def _minimax_worker(args):
        board, depth, alpha, beta, col, maximizingPlayer = args
        row = KI._get_next_open_row(board, col)
        temp_board = board.copy()
        KI._drop_piece(temp_board, row, col, 2 if maximizingPlayer else 1)
        return col, KI._minimax(tuple(map(tuple, temp_board)), depth - 1, alpha, beta, not maximizingPlayer)[1]

    @staticmethod
    def get_spalte(board):
        opponent = 1  # Gegner ist Spieler 1
        if KI._opponent_is_threatening(board, opponent):
            depth = 8  # Höhere Suchtiefe bei Bedrohung
        else:
            depth = 6  # Standard-Suchtiefe

        KI.transposition_table.clear()

        valid_locations = KI._get_valid_locations(board)

        with Pool(cpu_count()) as pool:
            results = pool.map(KI._minimax_worker, [(board, depth, -Inf, Inf, col, True) for col in valid_locations])

        best_col, best_score = max(results, key=lambda x: x[1])
        return best_col

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

    @staticmethod
    def _drop_piece(board, row, col, piece):
        board[row][col] = piece