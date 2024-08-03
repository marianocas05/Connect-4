import time
from Astar_RV import A_star_move
from mcts import MCTS_move

# o módulo time serve para que a jogada do A* não seja automática fazendo com que o jogo fique menos confuso no terminal pq JESUS

def print_board(board):
    for row in board:
        print(" ".join(row))


def drop_chip(board, column, chip):
    for row in range(5, -1, -1):
        if board[row][column] == "🔲":
            board[row][column] = chip
            return True
    return False


def is_board_full(board):
    for row in board:
        if "🔲" in row:
            return False
    return True


def check_winner(board, chip):
    # 4 EM LINHA HORIZONTAL
    for c in range(7 - 3):  # Iterate over columns
        for r in range(6):  # Iterate over rows
            if (
                board[r][c] == chip
                and board[r][c + 1] == chip
                and board[r][c + 2] == chip
                and board[r][c + 3] == chip
            ):
                return True

    # 4 EM LINHA VERTICAL
    for c in range(7):  # Iterate over columns
        for r in range(6 - 3):  # Iterate over rows
            if (
                board[r][c] == chip
                and board[r + 1][c] == chip
                and board[r + 2][c] == chip
                and board[r + 3][c] == chip
            ):
                return True

    # 4 EM LINHA DIAGONAL (pos)
    for c in range(7 - 3):  # Iterate over columns
        for r in range(6 - 3):  # Iterate over rows
            if (
                board[r][c] == chip
                and board[r + 1][c + 1] == chip
                and board[r + 2][c + 2] == chip
                and board[r + 3][c + 3] == chip
            ):
                return True

    # 4 EM LINHA DIAGONAL (neg)
    for c in range(7 - 3):  # Iterate over columns
        for r in range(3, 6):  # Iterate over rows
            if (
                board[r][c] == chip
                and board[r - 1][c + 1] == chip
                and board[r - 2][c + 2] == chip
                and board[r - 3][c + 3] == chip
            ):
                return True

    return False


def main():
    board = [["🔲"] * 7 for _ in range(6)]
    print("4 em Linha")

    player_one = "Algoritmo A*"
    player_two = "Algoritmo MCTS"
    time.sleep(1)

    print("%s contra %s" % (player_one, player_two))
    print("==============")
    print_board(board)
    print("%s controla 🔴" % player_one)
    print("%s controla 🔵" % player_two)

    players = [(player_one, "🔴"), (player_two, "🔵")]
    turn = 0

    while True:
        player, chip = players[turn % 2]

        if player == player_one:
            print("É a vez do %s." % (player_one))
            print("==============")
            column = A_star_move(board)
            time.sleep(1)

        elif player == player_two:
            print("É a vez do %s." % (player_two))
            print("==============")
            column = MCTS_move(board)
            time.sleep(1)

        if column is not None and 0 <= column < 7:
            if drop_chip(board, column, chip):
                print_board(board)
                if check_winner(board, chip):
                    print(f"{player} vence!")
                    break
                elif is_board_full(board):
                    print("Empate!")
                    break
                turn += 1
            else:
                print("Escolha inválida!")
        else:
            print("Escolha inválida!")


if __name__ == "__main__":
    main()