def evaluate_segment(segment, player):  # heuristic
    num_player = segment.count(player)
    num_opponent = segment.count("🔴")

    if num_player == 0:
        if num_opponent == 3:
            return -50
        elif num_opponent == 2:
            return -10
        elif num_opponent == 1:
            return -1
        elif num_opponent == 4:
            return -999
        else:
            return 0
    elif num_opponent == 0:
        if num_player == 3:
            return 50
        elif num_player == 2:
            return 10
        elif num_player == 1:
            return 1
        elif num_player == 4:
            return 999
        else:
            return 0
    else:
        return 0


def evaluate_board(board, player):
    total_score = 0
    # opponent = "🔴" if player == "🔵" else "🔵"

    # Evaluate rows
    for row in board:
        for c in range(7 - 3):
            segment = row[c : c + 4]
            total_score += evaluate_segment(segment, player)

    # Evaluate columns
    for c in range(7):
        column = [board[r][c] for r in range(6)]
        for r in range(6 - 3):
            segment = column[r : r + 4]
            total_score += evaluate_segment(segment, player)

    # Evaluate diagonals
    for r in range(6 - 3):
        for c in range(7 - 3):
            segment = [board[r + i][c + i] for i in range(4)]
            total_score += evaluate_segment(segment, player)

    for r in range(6 - 3):
        for c in range(3, 7):
            segment = [board[r + i][c - i] for i in range(4)]
            total_score += evaluate_segment(segment, player)

    return total_score


def A_star_move(board):

    possible_moves = [col for col in range(7) if board[0][col] == "🔲"]
    best_move = possible_moves[0]
    best_score = -float("inf")

    for move in possible_moves:
        temp_board = [row[:] for row in board]
        drop_chip(temp_board, move, "🔵")
        total_score = evaluate_board(temp_board, "🔵")
        if total_score > best_score:
            best_score = total_score
            best_move = move

    return best_move

# from game
def drop_chip(board, column, chip):
    for row in range(5, -1, -1):
        if board[row][column] == "🔲":
            board[row][column] = chip
            return True
    return False