import time
import copy
import math
import random

LINES = 6
COLUMNS = 7
AI_CHIP = "🔵"
PLAYER_CHIP = "🔴"
NUMERO_DE_SIMULACOES = 500


class Node:
    def __init__(self, estado, pai=None):
        self.estado = estado
        self.pai = pai
        self.filhos = []
        self.visitas = 0
        self.vitorias = 0
    
    def __str__(self):
        return f'''{self.estado}

        numero_de_visitas{self.visitas}

        numero_de_vitorias{self.vitorias}'''
        
def MCTS_move(tabuleiro):
    estado_raiz = copy.deepcopy(tabuleiro)
    node_raiz = Node(estado_raiz)
    player = AI_CHIP

    for i in range(NUMERO_DE_SIMULACOES):  # número de simulações (alterar para obter resultados diferentes)
        node_a_expandir = select_node_to_expand(node_raiz)
        if node_a_expandir == None:
            break
        expandir(node_a_expandir)
        for node in node_a_expandir.filhos:
            player = aux_expandir(node)
            for _ in range (5):
                resultado_simulacao = simulacao(node.estado, player)
                retropropagacao(node, resultado_simulacao)
        print(i)
    melhor_filho = selecionar_melhor_filho(node_raiz)
    return comparar_tab(tabuleiro, melhor_filho.estado)


def comparar_tab(atual,futuro):
    for c in range (7):
        for r in range (6):
            if atual[r][c] != futuro[r][c]:
                return c


def find_leafs(node):
    if not node.filhos:
        return [node]
    leafs = []
    for filho in node.filhos:
        leafs.extend(find_leafs(filho))
    return leafs


def select_node_to_expand(tree):
    leaf_nodes = find_leafs(tree)
    ucb1_best = -float("inf")
    node_to_expand = None
    for node in leaf_nodes:
        player = aux_expandir(node)
        if terminal(node.estado) == False:
            if node.visitas == 0:
                return node  # Tratar nós não visitados como tendo um valor UCB1 alto
            elif player == AI_CHIP:
                ucb1 = node.vitorias / node.visitas + 0.8 *math.sqrt( math.log(node.pai.visitas) / node.visitas)
            elif player == PLAYER_CHIP:
                ucb1 = (1 - (node.vitorias / node.visitas)) + 0.8 *math.sqrt( math.log(node.pai.visitas) / node.visitas)
            if ucb1 > ucb1_best:
                node_to_expand = node
                ucb1_best = ucb1
    return node_to_expand


def expandir(node):
    player = aux_expandir(node)
    for i in movimentos_validos(node.estado):
        linha = proxima_linha_disponivel(node.estado, i)
        estado_next = copy.deepcopy(node.estado)
        estado_next[linha][i] = player
        next_node = Node(estado_next)
        next_node.pai = node
        node.filhos.append(next_node)

        
def aux_expandir(node):
    n_ai = 0
    n_player = 0
    for line in node.estado:
        for element in line:
            if element == AI_CHIP:
                n_ai += 1
            elif element == PLAYER_CHIP:
                n_player += 1
    if n_ai == n_player:
        return PLAYER_CHIP
    elif n_ai < n_player:
        return AI_CHIP


def terminal(estado):
    # Ver se alguém ganhou
    return check_winner(estado, AI_CHIP) or check_winner(estado, PLAYER_CHIP) or is_board_full(estado)


def movimentos_validos(estado):
    # Retorna uma lista de colunas válidas onde um chip pode ser colocado
    valid_moves = []
    for coluna in range(COLUMNS):
        if estado[0][coluna] == "🔲":
            valid_moves.append(coluna)
    return valid_moves


def proxima_linha_disponivel(estado, coluna):
    # Encontra a próxima linha válida numa coluna
    for linha in range(LINES-1, -1, -1):
        if estado[linha][coluna] == "🔲":
            return linha
    return None


def resultado(estado):
    if check_winner(estado, AI_CHIP):
        return 1  # AI ganha
    elif check_winner(estado, PLAYER_CHIP):
        return -1  # Oponente ganha
    else:
        return 0  # Empate


def simulacao(estado, jogador_atual):
    estado_simulado = copy.deepcopy(estado)
    while not terminal(estado_simulado):
        movimentos_possiveis = movimentos_validos(estado_simulado)
        movimento = random.choice(movimentos_possiveis)
        linha = proxima_linha_disponivel(estado_simulado, movimento)
        estado_simulado[linha][movimento] = jogador_atual
        jogador_atual = PLAYER_CHIP if jogador_atual == AI_CHIP else AI_CHIP
    return resultado(estado_simulado)


def retropropagacao(node, resul):
    while node is not None:
        node.visitas += 1
        node.vitorias += resul
        node = node.pai


def selecionar_melhor_filho(node):
    melhor_filho = None
    super_max = -float('inf')
    for filho in (node.filhos):
        valor = filho.vitorias/filho.visitas
        if valor > super_max:
            super_max = valor
            melhor_filho = filho
    return melhor_filho


def check_winner(board, chip):
    # 4 EM LINHA HORIZONTAL
    for c in range(7 - 3):  # Iterate over columns, leaving room for a winning sequence
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
        for r in range(6 - 3):  # Iterate over rows, leaving room for a winning sequence
            if (
                board[r][c] == chip
                and board[r + 1][c] == chip
                and board[r + 2][c] == chip
                and board[r + 3][c] == chip
            ):
                return True

    # 4 EM LINHA DIAGONAL (pos)
    for c in range(7 - 3):  # Iterate over columns, leaving room for a winning sequence
        for r in range(6 - 3):  # Iterate over rows, leaving room for a winning sequence
            if (
                board[r][c] == chip
                and board[r + 1][c + 1] == chip
                and board[r + 2][c + 2] == chip
                and board[r + 3][c + 3] == chip
            ):
                return True

    # 4 EM LINHA DIAGONAL (neg)
    for c in range(7 - 3):  # Iterate over columns, leaving room for a winning sequence
        for r in range(3, 6):  # Iterate over rows, leaving room for a winning sequence
            if (
                board[r][c] == chip
                and board[r - 1][c + 1] == chip
                and board[r - 2][c + 2] == chip
                and board[r - 3][c + 3] == chip
            ):
                return True

    return False


def is_board_full(board):
    for row in board:
        if "🔲" in row:
            return False
    return True