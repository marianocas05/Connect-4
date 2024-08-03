import time
from Astar_RV import A_star_move
from mcts import MCTS_move
from minimax_connect4 import move

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

    player_one = input("Nome do Jogador: ")
    #   player_two = input("Nome do JOgador 2: ")
    player_two = "AI"

    while True:
        print("==============")
        print("Algoritmo 'a' - A*")
        print("Algoritmo 'b' - Monte-Carlo Tree Search")
        print("Algoritmo 'c' - MinMax (IN TESTING)")
        choice = input("Pretende jogar contra qual algoritmo? ")
        time.sleep(0.5)
        
        if choice == 'a':
            print("Selecionou o algoritmo A*.")
            break
        elif choice == 'b':
            print("Selecionou o algoritmo Monte-Carlo Tree Search.")
            break
        elif choice == 'c':
            print("Selecionou o algoritmo MinMax.")
            time.sleep(0.5)
            print("Este algoritmo apenas sai do jogo com um FORCE-QUIT. . .")
            time.sleep(0.5)
            move(player_one, player_two)
            time.sleep(0.5)
            column == 'x'
            break
        else:
            print("Escolha inválida!")

    print("%s contra %s" % (player_one, player_two))
    print("==============")
    print_board(board)
    print("%s controla 🔴" % player_one)
    print("AI controla 🔵")

    players = [(player_one, "🔴"), (player_two, "🔵")]
    turn = 0

    while True:
        player, chip = players[turn % 2]

        if player == player_one:
            while True:
                column = input("Escolhe uma coluna de 1 a 7: ")
                if column == 'x':
                    print("FORCE-QUITTING GAME. . .")
                    break
                if column.isdigit() and 1 <= int(column) <= 7:
                    column = int(column) -1
                    break
                else:
                    print("Escolha inválida!")

            print("==============")
            time.sleep(0.5)
        else:
            print("É a vez do %s." % (player_two))
            print("==============")

            if choice == 'b':
                column = MCTS_move(board)
                # time.sleep(0.5)
            else:
                column = A_star_move(board)
                time.sleep(0.5)

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