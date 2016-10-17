#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import numpy as np
from othello_rules import *

from collections import deque
def opponent_mobility_after_move(board, move, player):
    #print("working")
    board = make_move(board, 56, player)
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

def board_to_input(board, player):
    #TODO: Add a lot more heuristics!
    opponent = player * (-1)
    player_grid =  np.zeros((8,8))
    opponent_grid =  np.zeros((8,8))
    empties =  np.zeros((8,8))
    player_constant = np.zeros((8,8))
    zeros = np.zeros((8,8))
    legal_move_grid = np.zeros((8,8))
    ones = np.ones((8,8))
    corners = corner_board()
    x_squares = np.zeros((8,8))
    c_grid = c_squares()
    mobility = np.zeros((8,8))
    edges_a = edges_board_a()
    edges_b = edges_board_b()
    frontier = np.zeros((8,8))
    sum_player_stability = np.zeros((8,8))
    sum_opponent_stability = np.zeros((8,8))
    coin_parity = np.zeros((8,8))
    main_diagonal_1 = np.identity(8)
    main_diagonal_2 = np.fliplr(np.identity(8))
    
    corner_2x4_1 = corner_2x4()
    corner_2x4_2 = np.rot90(corner_2x4_1)
    corner_2x4_3 = np.rot90(corner_2x4_2)
    corner_2x4_4 = np.rot90(corner_2x4_3)
    corner_2x4_5 = np.transpose(corner_2x4_1)
    corner_2x4_6 = np.transpose(corner_2x4_2)
    corner_2x4_7 = np.transpose(corner_2x4_3)
    corner_2x4_8 = np.transpose(corner_2x4_4)
    
    
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
        coin_parity[row, column] = np.sum(board_after_player_move == player) - np.sum(board_after_player_move == player*(-1))
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
    #TODO: Add these features again after speeding up the stability calculations
    #current_player_stability = get_stability_features(board, player, stability, rows, columns, NW, NE)
    #current_opponent_stability = get_stability_features(board, opponent, stability, rows, columns, NW, NE)
    x_squares[1][1] = 1
    x_squares[6][1] = 1
    x_squares[6][6] = 1
    x_squares[1][6] = 1
    
    

    return np.concatenate((player_grid[:,:,None], opponent_grid[:,:,None], empties[:,:,None],
                           player_constant[:,:,None], zeros[:,:,None], legal_move_grid[:,:,None],
                          corners[:,:,None], x_squares[:,:,None], c_grid[:,:,None],
                          ones[:,:,None], mobility[:,:,None], edges_a[:,:,None], edges_b[:,:,None],
                          sum_player_stability[:,:,None], sum_opponent_stability[:,:,None],
                          current_stability[:,:,None], frontier[:,:,None], coin_parity[:,:,None],
                          main_diagonal_1[:,:,None], main_diagonal_2[:,:,None], corner_2x4_1[:,:,None],
                          corner_2x4_2[:,:,None], corner_2x4_3[:,:,None], corner_2x4_4[:,:,None],
                          corner_2x4_5[:,:,None], corner_2x4_6[:,:,None], corner_2x4_7[:,:,None],
                          corner_2x4_8[:,:,None]), axis=2)