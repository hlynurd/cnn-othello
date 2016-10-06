from itertools import product
import numpy as np

def initialize_game():
    board = np.zeros((8,8))
    board[3][3] = 1
    board[3][4] = -1
    board[4][3] = -1
    board[4][4] = 1
    return board

def make_move(board, move, player):
    private_board = np.array(board)
    move = str(move)
    row = int(move[0]) - 1
    column = int(move[1]) - 1
    private_board[row][column] = player
    private_board = do_takeovers(private_board, row, column, player)[0]
    return private_board

def get_winner(board, black, white):
    if get_points(board, black) > get_points(board, white):
        return black 
    if get_points(board, black) < get_points(board, white):
        return white 
    else:
        return False

def get_points(board, player):
    return np.count_nonzero(board == player)

def find_legal_moves(board, player):
    legal_moves = []
    for i in range(0, 8):
        for j in range(0, 8):
            if is_legal(board, i, j, player):
                legal_moves.append((i+1) * 10 + (j+1))
    return legal_moves

def do_takeovers(board, row, column, player):
    (down, board) = flip_down(board, row, column, player)
    (left, board) = flip_left(board, row, column, player)
    (up, board) = flip_up(board, row, column, player)
    (right, board) = flip_right(board, row, column, player)
    (downright, board) = flip_downright(board, row, column, player)
    (downleft, board) = flip_downleft(board, row, column, player)
    (upright, board) = flip_upright(board, row, column, player)
    (upleft, board) = flip_upleft(board, row, column, player)
    return (board, down, left, up, right, downright, downleft, upright, upleft)

def is_legal(board, row, column, player):
    if board[row][column] != 0:
        return False
    temp_board = np.array(board)
    temp_board[row][column] = player
    (temp_board, down, left, up, right,
            downright, downleft, upright, upleft) = do_takeovers(temp_board, row, column, player)
    if down:
        if board[row+1][column] != player:
            return True
    if up:
        if board[row-1][column] != player:
            return True
    if left:
        if board[row][column-1] != player:
            return True
    if right:
        if board[row][column+1] != player:
            return True
    if downleft:
        if board[row+1][column-1] != player:
            return True
    if downright:
        if board[row+1][column+1] != player:
            return True
    if upright:
        if board[row-1][column+1] != player:
            return True
    if upleft:
        if board[row-1][column-1] != player:
            return True
    return False


def flip_downright(board, row, column, player):
    i = row
    k = column
    while True:
        if i is 7 or k is 7:
            return False, board
        i += 1
        k += 1
        if board[i][k] == 0:
            return False, board
        if board[i][k] == player:
            h = column
            for j in range(row, i):
                board[j][h] = player
                h = h+1
            return True, board

def flip_right(board, row, column, player):
    i = column
    while True:
        if i is 7:
            return False, board
        i += 1
        if board[row][i] == 0:
            return False, board
        if board[row][i] == player:
            for j in range(column, i):
                board[row][j] = player
            return True, board

        
def flip_upright(board, row, column, player):
    i = row
    k = column
    while True:
        if i is 0 or k is 7:
            return False, board
        i -= 1
        k += 1
        if board[i][k] == 0:
            return False, board
        if board[i][k] == player:
            h = k
            for j in range(i, row):
                board[j][h] = player
                h = h-1
            return True, board
        
def flip_up(board, row, column, player):
    i = row
    while True:
        if i is 0:
            return False, board
        i -= 1
        if board[i][column] == 0:
            return False, board
        if board[i][column] == player:
            for j in range(i, row):
                board[j][column] = player
            return True, board
        
def flip_upleft(board, row, column, player):
    i = row
    k = column
    while True:
        if i is 0 or k is 0:
            return False, board
        i -= 1
        k -= 1
        if board[i][k] == 0:
            return False, board
        if board[i][k] == player:
            h = k
            for j in range(i, row):
                board[j][h] = player
                h = h+1
            return True, board
        
        
def flip_left(board, row, column, player):
    i = column
    while True:
        if i is 0:
            return False, board
        i -= 1
        if board[row][i] == 0:
            return False, board
        if board[row][i] == player:
            for j in range(i, column):
                board[row][j] = player
            return True, board
        
def flip_down(board, row, column, player):
    i = row
    while True:
        if i is 7:
            return False, board
        i += 1
        if board[i][column] == 0:
            return False, board
        if board[i][column] == player:
            for j in range(row, i):
                board[j][column] = player
            return True, board
        
def flip_downleft(board, row, column, player):
    i = row
    k = column
    while True:
        if i is 7 or k is 0:
            return False, board
        i += 1
        k -= 1
        if board[i][k] == 0:
            return False, board
        if board[i][k] == player:
            h = column
            for j in range(row, i):
                board[j][h] = player
                h = h-1
            return True, board