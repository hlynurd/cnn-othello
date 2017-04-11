#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import numpy as np
from othello_rules import *
import ctypes
from numpy.ctypeslib import ndpointer
from collections import deque

zebralogic = ctypes.CDLL('/home/hlynur/convothello/zebralogic.so')
zebralogic.get_stability.restype = ndpointer(dtype=ctypes.c_int, shape=(100,))
zebralogic.get_mobility.restype = ndpointer(dtype=ctypes.c_int, shape=(100,))
#zebralogic.count_stables.restype = ndpointer(dtype=ctypes.c_int, shape=(1))


def opponent_mobility_after_move(board, move, player):
    #print("working")
    board = make_move(board, move, player)
    return len(find_legal_moves(board, player * (-1)))



def corner_board():
    corners = np.zeros((8,8))
    corners[0][0] = 1
    corners[7][0] = 1
    corners[0][7] = 1
    corners[7][7] = 1
    return corners

def c_squares():
    c_squares = np.zeros((8,8))
    c_squares[0][1] = 1
    c_squares[1][0] = 1
    c_squares[6][0] = 1
    c_squares[0][6] = 1
    c_squares[7][1] = 1
    c_squares[1][7] = 1
    return c_squares

def edges_board_a():
    edges_a = np.zeros((8,8))
    edges_a[2][0] = 1
    edges_a[5][0] = 1
    edges_a[0][2] = 1
    edges_a[0][5] = 1
    edges_a[7][2] = 1
    edges_a[7][5] = 1
    edges_a[2][7] = 1
    edges_a[5][7] = 1
    return edges_a

def edges_board_b():
    edges_b = np.zeros((8,8))
    edges_b[3][0] = 1
    edges_b[4][0] = 1
    edges_b[0][3] = 1
    edges_b[0][4] = 1
    edges_b[7][3] = 1
    edges_b[7][4] = 1
    edges_b[3][7] = 1
    edges_b[4][7] = 1
    return edges_b


    


# TODO: Write edges_board_A og aðgreina frá B
    
# Returns vector [v0, v1, ..., v7]
# where v0 = 0 if row 1 is full, otherwise 0
# Rows are marked 
# 0 0 0 0 0 0 0 0
# 1 1 1 1 1 1 1 1
# 2 2 2 2 2 2 2 2
# 3 3 3 3 3 3 3 3 
# 4 4 4 4 4 4 4 4
# 5 5 5 5 5 5 5 5
# 6 6 6 6 6 6 6 6
# 7 7 7 7 7 7 7 7
def filled_rows(board):
    rows = np.ones(8)
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                rows[i] = 0
                break
    return rows

def get_filled_row_features(rows):
    board = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            if rows[i] == 1:
                board[i][j] = 1
            else:
                break
    return board

# Returns vector [v0, v1, ..., v7]
# where v0 = 0 if column 1 is full, otherwise 0
# Rows are marked 
# 0 1 2 3 4 5 6 7
# 0 1 2 3 4 5 6 7
# 0 1 2 3 4 5 6 7
# 0 1 2 3 4 5 6 7
# 0 1 2 3 4 5 6 7
# 0 1 2 3 4 5 6 7
# 0 1 2 3 4 5 6 7
# 0 1 2 3 4 5 6 7
def filled_columns(board):
    columns = np.ones(8)
    for j in range(8):
        for i in range(8):
            if board[i][j] == 0:
                columns[j] = 0
                break
    return columns

def get_filled_column_features(columns):
    board = np.zeros((8,8))
    for j in range(8):
        for i in range(8):
            if columns[j] == 1:
                board[i][j] = 1
            else:
                break
    return board

# Returns vector [v_a, v_b, ..., v_o]
# where v_x = 0 if diagonal x is full, otherwise 0
# Diagonals are defined
# a b c d e f g h
# b c d e f g h i
# c d e f g h i j
# d e f g h i j k
# e f g h i j k l
# f g h i j k l m
# g h i j k l m n
# h i j k l m n o
def filled_NE(board):
    diags_NE = np.ones(15)
    for row in range(8):
        i = 0
        j = row
        while True:
            if board[i][j] == 0:
                diags_NE[row] = 0
                break
            if j == 0:
                break
            j -= 1
            i += 1
    for column in range(1, 8):
        i = 7
        j = column
        while True:
            if board[i][j] == 0:
                diags_NE[(column+7)] = 0
                break
            if j == 7:
                break
            i -= 1
            j += 1
    return diags_NE

def get_filled_NE_features(diags_NE):
    board = np.zeros((8,8))
    for row in range(8):
        i = 0
        j = row
        while True:
            if diags_NE[row] == 1:
                board[i][j] = 1
            else:
                break
            if j == 0:
                break
            j -= 1
            i += 1
    for column in range(1, 8):
        i = 7
        j = column
        while True:
            if diags_NE[column+7] == 1:
                board[i][j] = 1
            else:
                break
            if j == 7:
                break
            i -= 1
            j += 1
    return board


# Returns vector [v_a, v_b, ..., v_o]
# where v_x = 0 if diagonal x is full, otherwise 0
# Rows are marked 
# h g f e d c b a
# i h g f e d c b
# j i h g f e d c  
# k j i h g f e d  
# l k j i h g f e
# m l k j i h g f
# n m l k j i h g
# o n m l k j i h
def filled_NW(board):
    diags_NW = np.ones(15)
    cnt = 0
    for column in range(7, -1, -1):
        i = 0
        j = column
        while True:
            if board[i][j] == 0:
                diags_NW[cnt] = 0
                break
            if j == 7:
                break
            j += 1
            i += 1
        cnt += 1
    for row in range(1, 8):
        i = row
        j = 0
        while True:
            if board[i][j] == 0:
                diags_NW[row+7] = 0
                break
            if i == 7:
                break
            j += 1
            i += 1
    return diags_NW

def get_filled_NW_features(diags_NW):
    board = np.zeros((8,8))
    cnt = 0
    for column in range(7, -1, -1):
        i = 0
        j = column
        while True:
            if diags_NW[cnt] == 1:
                board[i][j] = 1
            else:
                break
            if j == 7:
                break
            j += 1
            i += 1
        cnt += 1
    for row in range(1, 8):
        i = row
        j = 0
        while True:
            if diags_NW[row+7] == 1:
                board[i][j] = 1
            else:
                break
            if i == 7:
                break
            j += 1
            i += 1
    return board

# Returns a list of adjacent friendly cells as well as their respective directions
# 1 2 3 
# 0 x 0
# 3 2 1 
def find_friendly_neighbors(board, cell, color):
    i = cell[0] # Row
    j = cell[1] # Column
    friends = []
    directions = []
    if i > 0:
        if board[i-1][j] == color:
            friends.append((i-1, j))
            directions.append(2)
        if j > 0:
            if board[i-1][j-1] == color:
                friends.append((i-1, j-1))
                directions.append(1)
        if j < 7:
            if board[i-1][j+1] == color:
                friends.append((i-1, j+1))
                directions.append(3)
    if i < 7:
        if board[i+1][j] == color:
            friends.append((i+1, j))
            directions.append(2)
        if j > 0:
            if board[i+1][j-1] == color:
                friends.append((i+1, j-1))
                directions.append(3)
        if j < 7:
            if board[i+1][j+1] == color:
                friends.append((i+1, j+1))
                directions.append(1)
    if j > 0:
        if board[i][j-1] == color:
            friends.append((i, j-1))
            directions.append(0)
    if j < 7:
        if board[i][j+1] == color:
            friends.append((i, j+1))
            directions.append(0)
    return friends, directions
        
# 1 2 3 
# 0 x 0
# 3 2 1 
def is_stable(board, stability, NW, NE, columns, rows, cell, color):
    friends, directions = find_friendly_neighbors(board, cell, color)
    i = cell[0]
    j = cell[1]
    conc = np.concatenate((rows[:,:,None], NW[:,:,None], columns[:,:,None], NE[:,:,None]), axis=2)    
    for k in range(len(friends)):
        row = friends[k][0]
        column = friends[k][1]
        if stability[row][column] == 1:
            conc[i][j][directions[k]] = 1
    if conc[i][j][0] == 1 and conc[i][j][1] == 1 and conc[i][j][2] == 1 and conc[i][j][3] == 1:
        return True
    return False

def get_stability_features(board, color, rows, columns, NW, NE):
    stability = np.zeros((8,8))
    #stability = np.array(initial_stability)
    #print("partytime")
    #print(stability)
    #stability = np.zeros((8,8))
    # The corners are always stable
    if board[0][0] == color:
        stability[0][0] = 1
    if board[0][7] == color:
        stability[0][7] = 1
    if board[7][0] == color:
        stability[7][0] = 1
    if board[7][7] == color:
        stability[7][7] = 1
    # The edges have stability in the direction of their walls
    for j in range(8):
        rows[j][0] = 1
        rows[j][7] = 1
        columns[0][j] = 1
        columns[7][j] = 1
        for i in(0, 7):
            NW[i][j] = 1
            NW[j][i] = 1
            NE[i][j] = 1
            NE[j][i] = 1
    # Next find the requirement of someone being in a full "row" ini all four directions
    for i in range(8):
        for j in range(8):
            if NW[i][j] == 1 and NE[i][j] == 1 and columns[i][j] == 1 and rows[i][j] == 1 and board[i][j] == color:
                stability[i][j] = 1
    #print("initial stability for player " + str(color))
    #print(stability)
    # Now iterate through all the stable pieces and see if their neighbours
    # have some combination of being adjacent to a friendly, stable piece -or- 
    # being in a filled "row" in all four directions
    #Find stable cells so far
    for XXX in range(2):
        stable_nonzeros = np.nonzero(stability)
        visited_cells = []
        stable_cells = []
        for i in range(len(stable_nonzeros[0])):
            row = stable_nonzeros[0][i]
            column = stable_nonzeros[1][i]
            #move_string = str((row+1)*10+(column+1))
            stable_cells.append((row, column))
        visited_cells += stable_cells
        stable_candidates = deque([])
        for cell in stable_cells:
            #Find_friendly_neighbors
            stable_neighbors, directions = find_friendly_neighbors(board, cell, color)
            for neighbor in stable_neighbors:
                if neighbor not in visited_cells:
                    stable_candidates.append(neighbor)
        while len(stable_candidates) > 0:
            if XXX % 2 == 0:
                candidate = stable_candidates.popleft()
            else:
                candidate = stable_candidates.pop()
            if candidate in visited_cells:
                continue
            #Determines is_stable with "row" and friendly-neighbor in four direction criteria
            if is_stable(board, stability, NW, NE, columns, rows, candidate, color):
                #Update_stability_grid
                stability[candidate[0]][candidate[1]] = 1
                stable_neighbors, directions = find_friendly_neighbors(board, candidate, color)
                for neighbor in stable_neighbors:
                    if neighbor not in visited_cells:
                        if neighbor not in stable_candidates:
                            stable_candidates.append(neighbor)
            visited_cells += [candidate]
    return stability

def calculate_frontier(board, cell):
    i = cell[0] # Row
    j = cell[1] # Column
    neighbor_sum = 0
    if i > 0:
        if board[i-1][j] == 0:
            neighbor_sum += 1
        if j > 0:
            if board[i-1][j-1] == 0:
                neighbor_sum += 1
        if j < 7:
            if board[i-1][j+1] == 0:
                neighbor_sum += 1
    if i < 7:
        if board[i+1][j] == 0:
            neighbor_sum += 1
        if j > 0:
            if board[i+1][j-1] == 0:
                neighbor_sum += 1
        if j < 7:
            if board[i+1][j+1] == 0:
                neighbor_sum += 1
    if j > 0:
        if board[i][j-1] == 0:
            neighbor_sum += 1
    if j < 7:
        if board[i][j+1] == 0:
            neighbor_sum += 1
    return neighbor_sum

def corner_2x4():
    corner_2x4 = np.zeros((8,8))
    corner_2x4[0, 0] = 1
    corner_2x4[0, 1] = 1
    corner_2x4[1, 0] = 1
    corner_2x4[1, 1] = 1
    corner_2x4[2, 0] = 1
    corner_2x4[2, 1] = 1
    corner_2x4[3, 0] = 1
    corner_2x4[3, 1] = 1
    return corner_2x4

def to_onehot_8vals(array):
    onehot1 = np.zeros((8,8))
    onehot2 = np.zeros((8,8))
    onehot3 = np.zeros((8,8))
    onehot4 = np.zeros((8,8))
    onehot5 = np.zeros((8,8))
    onehot6 = np.zeros((8,8))
    onehot7 = np.zeros((8,8))
    onehot8 = np.zeros((8,8))
    for i in range(0, 8):
        for j in range(0, 8):
            val = array[i, j]
            if val == 0:
                onehot1[i, j] = 1
            if val == 1:
                onehot2[i, j] = 1
            if val == 2:
                onehot3[i, j] = 1
            if val == 3:
                onehot4[i, j] = 1
            if val == 4:
                onehot5[i, j] = 1
            if val == 5:
                onehot6[i, j] = 1
            if val == 6:
                onehot7[i, j] = 1
            if val >= 7:
                onehot8[i, j] = 1
    return np.dstack((onehot1, onehot2, onehot3, onehot4, onehot5, onehot6, onehot7, onehot8))
    
def history_stack(move_history):
    history0 = np.zeros((8,8))
    prev_move = str(move_history[0])
    row = int(prev_move[0]) - 1
    column = int(prev_move[1]) - 1
    history0[row, column] = 1
    
    history1 = np.zeros((8,8))
    prev_move = str(move_history[1])
    row = int(prev_move[0]) - 1
    column = int(prev_move[1]) - 1
    history1[row, column] = 1
    
    history2 = np.zeros((8,8))
    prev_move = str(move_history[2])
    row = int(prev_move[0]) - 1
    column = int(prev_move[1]) - 1
    history2[row, column] = 1
    
    history3 = np.zeros((8,8))
    prev_move = str(move_history[3])
    row = int(prev_move[0]) - 1
    column = int(prev_move[1]) - 1
    history3[row, column] = 1
    return np.dstack((history0, history1, history2, history3))

#TODO: Delete this function
def board_to_input(board, player, prev_moves):
    print("XXX: Use board_to_input_c instead!")
    opponent = player * (-1)
    player_grid =  np.zeros((8,8))
    opponent_grid =  np.zeros((8,8))
    empties =  np.zeros((8,8))
    player_constant = np.zeros((8,8))
    zeros = np.zeros((8,8))
    legal_move_grid = np.zeros((8,8))
    ones = np.ones((8,8))
    mobility = np.ones((8,8)) * (-1)
    frontier = np.ones((8,8)) * (-1)
    sum_player_stability = np.zeros((8,8))
    sum_opponent_stability = np.zeros((8,8))
    
    #TODO: Makee this into a function!
    history = history_stack(prev_moves)
    
    #stability = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            #move_string = str((i+1)*10+j)
            #mobility[i][j] = opponent_mobility_after_move(board, move_string, player)
            if player == -1:
                player_constant[i][j] = 1
            if board[i][j] == player:
                player_grid[i][j] = 1
            elif board[i][j] != 0:
                opponent_grid[i][j] = 1
            else:
                empties[i][j] = 1

    for move in find_legal_moves(board, player):
        move = str(move)
        row = int(move[0]) - 1
        column = int(move[1]) - 1
        legal_move_grid[row][column] = 1
        mobility[row][column] = opponent_mobility_after_move(board, move, player)
        board_after_player_move = make_move(board, move, player)
        #coin_parity[row, column] = np.sum(board_after_player_move == player) - np.sum(board_after_player_move == player*(-1))
        board_after_opponent_move = make_move(board, move, opponent)
        frontier[row, column] = calculate_frontier(board, (row, column))
        # Only calculate stability if any of the twelve indicated corner cells are occupied
        if board[0][0] != 0 or board[0][1] != 0 or board[1][0] != 0 or board[7][7] != 0 or board[6][7] != 0 or board[7][6] != 0 or board[0][7] != 0 or board[1][7] != 0 or board[0][6] != 0 or board[7][0] != 0 or board[7][1] != 0 or board[6][0] != 0:
            # Add feature plane that shows sum of stable friendly pieces
            # if current player places a move in legal move cell - and another
            # which shows sum of stable opponent pieces if opponent moves there
            ind_rows  = filled_rows(board_after_player_move)
            initial_rows = get_filled_row_features(ind_rows)
            ind_columns = filled_columns(board_after_player_move)
            ind_NW = filled_NW(board_after_player_move)
            ind_NE = filled_NE(board_after_player_move)
            initial_columns = get_filled_column_features(ind_columns)
            initial_NW = get_filled_NW_features(ind_NW)
            initial_NE = get_filled_NE_features(ind_NE)
            #TODO: Speed up stability calculations such that it utilizes it being monotonically increasing
            potential_player_stability = get_stability_features(board_after_player_move, player, initial_rows, initial_columns, initial_NW, initial_NE)
            potential_opponent_stability = get_stability_features(board_after_opponent_move, opponent, initial_rows, initial_columns, initial_NW, initial_NE)
            sum_player_stability[row][column] = np.sum(potential_player_stability)
            sum_opponent_stability[row][column] = np.sum(potential_opponent_stability)
    
    ind_rows  = filled_rows(board)    
    ind_columns = filled_columns(board)
    ind_NW = filled_NW(board)
    ind_NE = filled_NE(board)
    initial_rows = get_filled_row_features(ind_rows)
    initial_columns = get_filled_column_features(ind_columns)
    initial_NW = get_filled_NW_features(ind_NW)
    initial_NE = get_filled_NE_features(ind_NE)
    current_stability = get_stability_features(board, player, initial_rows, initial_columns, initial_NW, initial_NE)
    current_opponent_stability = get_stability_features(board, opponent, initial_rows, initial_columns, initial_NW, initial_NE)
    
    #TODO: Add these features again after speeding up the stability calculations
    #current_player_stability = get_stability_features(board, player, stability, rows, columns, NW, NE)
    #current_opponent_stability = get_stability_features(board, opponent, stability, rows, columns, NW, NE)

    player_stability_gained = sum_player_stability - np.sum(current_stability)
    opponent_stability_gained = sum_opponent_stability - np.sum(current_opponent_stability)
    player_stability_gained = player_stability_gained.clip(min=0)
    opponent_stability_gained = opponent_stability_gained.clip(min=0)
    print("feature player_stability_gained")
    print(player_stability_gained)
    #print np.unique(player_stability_gained)
    #print np.unique(opponent_stability_gained)
    return np.dstack((history, player_grid, opponent_grid, empties, player_constant, zeros, legal_move_grid, ones, to_onehot_8vals(mobility), to_onehot_8vals(player_stability_gained), to_onehot_8vals(opponent_stability_gained), to_onehot_8vals(frontier)))

def flat_to_square(carr):
    pyarr = np.zeros((8,8))
    for i in range(1, 9):
        for j in range(1, 9): 
            pyarr[i-1,j-1] = carr[i*10+j]
    return pyarr
def square_to_flat(pyarr):
    carr = [-1] * 100
    for i in range(1, 9):
        for j in range(1, 9):
            carr[i*10+j] = int(pyarr[i-1, j-1])
    return carr

def board_to_input_c(board, player, prev_moves):
    opponent = player * (-1)
    player_grid =  np.zeros((8,8))
    opponent_grid =  np.zeros((8,8))
    empties =  np.zeros((8,8))
    player_constant = np.zeros((8,8))
    zeros = np.zeros((8,8))
    legal_move_grid = np.zeros((8,8))
    ones = np.ones((8,8))
    frontier = np.ones((8,8)) * (-1)
    history = history_stack(prev_moves)
    
    for i in range(8):
        for j in range(8):
            if player == -1:
                player_constant[i][j] = 1
            if board[i][j] == player:
                player_grid[i][j] = 1
            elif board[i][j] != 0:
                opponent_grid[i][j] = 1
            else:
                empties[i][j] = 1

    #TODO: Use Zebra to calculate find_legal_moves instead (change it in the Othello_rules file),
    #XXX: I'm sometimes generating "legal moves" that aren't legal at all!
    for move in find_legal_moves_c(board, player):
        move = str(move)
        row = int(move[0]) - 1
        column = int(move[1]) - 1
        legal_move_grid[row][column] = 1
        frontier[row, column] = calculate_frontier(board, (row, column))
    
    #TODO: Check if "Only calculate stability if any of the twelve indicated corner cells are occupied" is fulfilled
    flat_board = square_to_flat(board)
    arr = (ctypes.c_int * len(flat_board))(*flat_board)
    stabs = zebralogic.get_stability(arr, player)
    opp_stabs = zebralogic.get_stability(arr, opponent)
    mobs = zebralogic.get_mobility(arr, player)
    sum_player_stability = flat_to_square(stabs)
    sum_opponent_stability = flat_to_square(opp_stabs)
    mobility = flat_to_square(mobs)
   
    current_stability = zebralogic.count_stables(arr, player)
    current_opponent_stability = zebralogic.count_stables(arr, opponent)
    player_stability_gained = sum_player_stability - current_stability
    opponent_stability_gained = sum_opponent_stability - current_opponent_stability
    player_stability_gained = player_stability_gained.clip(min=0)
    opponent_stability_gained = opponent_stability_gained.clip(min=0)
    return np.dstack((history, player_grid, opponent_grid, empties, player_constant, zeros, legal_move_grid, ones, to_onehot_8vals(mobility), to_onehot_8vals(player_stability_gained), to_onehot_8vals(opponent_stability_gained), to_onehot_8vals(frontier)))

def board_to_input_c_small(board, player, prev_moves):
    opponent = player * (-1)
    player_grid =  np.zeros((8,8))
    opponent_grid =  np.zeros((8,8))
    empties =  np.zeros((8,8))
    
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                player_grid[i][j] = 1
            elif board[i][j] != 0:
                opponent_grid[i][j] = 1
            else:
                empties[i][j] = 1
    return np.dstack((player_grid, opponent_grid, empties))
