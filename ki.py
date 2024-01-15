import numpy as np

class KI:
    @staticmethod
    def _evaluate_window(window, player):
        score = 0
        opponent = 3 - player
        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 8
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 3
        if window.count(opponent) == 3 and window.count(0) == 1:
            score -= 4
        return score

    @staticmethod
    def _score_position(board, player):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, 3])]
        center_count = center_array.count(player)
        score += center_count * 3

        # Score Horizontal
        for r in range(6):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(4):
                window = row_array[c:c + 4]
                score += KI._evaluate_window(window, player)

        # Score Vertical
        for c in range(7):
            col_array = [int(i) for i in list(board[:, c])]
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
        valid_locations = []
        for col in range(7):
            row = KI._get_next_open_row(board, col)
            location = KI._is_valid_location(board, row, col)
            if location:
                valid_locations.append(col)
        return valid_locations

    @staticmethod
    def _get_next_open_row(board, col):
        for r in range(5, -1, -1):  # Start from the bottom and go upwards
            if board[r][col] == 0:
                return r
        return -1  # Column is full

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
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, KI._score_position(board, 2))

        if maximizingPlayer:
            value = -np.Inf
            column = np.random.choice(valid_locations)
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
            return (column, value)

        else:  # Minimizing player
            value = np.Inf
            column = np.random.choice(valid_locations)
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
    def choose_best_move(board):
        depth = 100  # You can adjust the depth of the search
        minimax = KI._minimax(board, depth, -np.Inf, np.Inf, True)
        return minimax[0]

    @staticmethod
    def _check_winner(board, player):
        # Check horizontal locations for win
        for c in range(4):
            for r in range(6):
                if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][
                    c + 3] == player:
                    return True

        # Check vertical locations for win
        for c in range(7):
            for r in range(3):
                if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][
                    c] == player:
                    return True

        # Check positively sloped diaganols
        for c in range(4):
            for r in range(3):
                if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and \
                        board[r + 3][c + 3] == player:
                    return True

        # Check negatively sloped diaganols
        for c in range(4):
            for r in range(3, 6):
                if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and \
                        board[r - 3][c + 3] == player:
                    return True

        return False

    @staticmethod
    def _drop_piece(board, row, col, piece):
        board[row][col] = piece
