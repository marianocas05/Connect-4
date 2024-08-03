import random
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = "🔲"
PLAYER_PIECE = "🔴"
AI_PIECE = "🔵"

WINDOW_LENGTH = 4

def create_board():
    board = [[EMPTY] * COLUMN_COUNT for _ in range(ROW_COUNT)]
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r

def print_board(board):
    print("==============")
    for row in reversed(board):
        print(' '.join(row))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    
    if window.count(piece) == 4:
        score += 90000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 50
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10
    elif window.count(piece) == 1 and window.count(EMPTY) == 3:
        score += 1

    if window.count(opp_piece) == 4:
        score -= 10000
    elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 50
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 10
    elif window.count(opp_piece) == 1 and window.count(EMPTY) == 3:
        score -= 1

    return score

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [board[i][COLUMN_COUNT // 2] for i in range(ROW_COUNT)]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = board[r]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [board[i][c] for i in range(ROW_COUNT)]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [row[:] for row in board]
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [row[:] for row in board]
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = [row[:] for row in board]
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def move(human, ai):
	board = create_board()
	print_board(board)
	game_over = False

	turn = 0

	while not game_over:

		if turn == PLAYER and not game_over:
			col = input("Escolhe uma coluna de 1 a 7: ")
			if col == 'x':
				print("FORCE-QUITTING GAME. . .")
				break

			if col.isdigit():
				col = int(col)
				col -= 1

			# Ask for Player 1 Input
			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, PLAYER_PIECE)

				if winning_move(board, PLAYER_PIECE):
					game_over = True

				turn += 1
				turn = turn % 2

				print_board(board)

			else:
				print("Escolha inválida!")

		# # Ask for Player 2 Input
		if turn == AI and not game_over:

			# col = random.randint(0, COLUMN_COUNT-1)
			# col = pick_best_move(board, AI_PIECE)
			col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

			if is_valid_location(board, col):
				# pygame.time.wait(500)
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, AI_PIECE)

				if winning_move(board, AI_PIECE):
					game_over = True

				print_board(board)

				turn += 1
				turn = turn % 2

		if game_over:
			if winning_move(board, PLAYER_PIECE):
				print(f"{human} vence!")
			else:
				print(f"{ai} vence!")

			print("FORCE-QUITTING GAME. . .")
