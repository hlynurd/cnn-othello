#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import numpy as np
from struct import *
from feature_extractor import *
from othello_rules import *
import os
def get_all_matches(data_root):
    matches = []
    for fname in os.listdir(data_root):
        _f = open(data_root + fname, 'rb')
        data = _f.read()
        #header = data[:16]
        #date_created = header[:4]
        i = 0
        while True:
            if len(data[(16+68*i):(16+68*(i+1))]) < 1:
                break
            matches.append(data[(16+68*i):(16+68*(i+1))])
            i = i+1
        _f.close()
    return matches

def move_to_label(move):
    label = np.zeros((8,8))
    label = make_move(label, move, 1)
    return label
def prepare_data(data):
    i = data
    i = [np.transpose(i)]
    i = np.transpose(i)
    return i
def zero_illegal_moves(board, movelist):
    new_board = np.zeros((8,8))
    for move in movelist:
        new_board += make_move(np.zeros((8,8)), move, 1)
    return np.multiply(new_board, board)

#(x, y) -> (y, x)
def flip_move_upright(move):
    move = str(move)
    row = int(move[0]) - 1
    column = int(move[1]) - 1
    return str((column+1) * 10 + (row+1))

#(x, y) -> (9-y, 9-x)
def flip_move_upleft(move):
    move = str(move)
    row = int(move[0]) - 1
    column = int(move[1]) - 1
    return str((8-column) * 10 + (8-row))

def flip_features(features, symmetry_action):
    flipped_features = np.array(features)
    for i in range(features.shape[2]):
        if symmetry_action == 'upright':
            flipped_features[:,:,i] = np.transpose(features[:,:,i])
        if symmetry_action == 'upleft':
            flipped_features[:,:,i] = np.rot90(np.rot90(np.transpose(features[:,:,i])))
        if symmetry_action == 'both':
            flipped_features[:,:,i] = np.transpose(np.rot90(np.rot90(np.transpose(features[:,:,i]))))
    return flipped_features