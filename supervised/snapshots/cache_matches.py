#!/usr/bin/python
# -*- coding: utf-8 -*-
from othello_rules import *
from othello_net import *
from tensorflow.python.framework import ops
from datetime import datetime
from example_states import *
from feature_extractor import *
from training_utils import *
import numpy as np
# Following function iterates through each match from the training
# data set and then calculates and saves the features of each match
# without rotations
def create_cached_features(match_list, destination):
    for i in range(0, len(match_list)):
        if i % 500 is 0:
            print(str(datetime.now()) + " current i is " + str(i)) 
        current_match = match_list[i]
        raw_match_movelist = current_match[8:]
        unpacked_movelist = unpack('b'*60, raw_match_movelist)
        board = initialize_game()
        training_stability = np.zeros((8,8))
        player = -1
        # One training batch is all the data from one match
        input_batch = []
        label_batch = []
        previous_moves = [56, 56, 56, 56]
        for move in unpacked_movelist:
            feature_path = destination + '/features/features_' + str(i) + "_" + str(move) + ".npy"
            label_path = destination +  '/labels/labels_' + str(i) + "_" + str(move) + ".npy"
            '''
            if os.path.isfile(feature_path):
                os.remove(feature_path)
            if os.path.isfile(label_path):
                os.remove(label_path)
                continue
            else:
                continue
            '''
            
            
            if not os.path.isfile(feature_path):
                if move == 0:
                    break
                features = board_to_input(board, player,previous_moves)
                label = prepare_data(move_to_label(move))            
                #features = (features - np.mean(features)) / np.std(features)
                np.save(feature_path, features)
                #print(features)
                np.save(label_path, label)
                board = make_move(board, move, player)
                if player is 1:
                    player = -1
                else:
                    player = 1
                legal_moves = find_legal_moves(board, player)
                if len(legal_moves) == 0:
                    if player is 1:
                        player = -1
                    else:
                        player = 1
                previous_moves[3] = previous_moves[2]
                previous_moves[2] = previous_moves[1]
                previous_moves[1] = previous_moves[0]
                previous_moves[0] = move

print("doing work")
validation_matches = get_all_matches('/storage/hlynur/unprocessed/validation/')
print(len(validation_matches))
validation_dest = '/storage/hlynur/cache/validation/'
create_cached_features(validation_matches, validation_dest)
training_matches = get_all_matches('/storage/hlynur/unprocessed/training/')
print(len(training_matches))
training_dest = '/storage/hlynur/cache/training'
create_cached_features(training_matches, training_dest)
print("done")
