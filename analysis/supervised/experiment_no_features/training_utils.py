#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import numpy as np
import os
from struct import *
from feature_extractor import *
from othello_rules import *
from datetime import datetime

def prediction_accuracy(sess, img_data, ground_truths, pred_up, data_path, len_games=4):
    successes = []
    validation_matches = get_all_matches(data_path)
    #validation_matches = validation_matches[0:len_games]
    for i in range(len(validation_matches)):
        unpacked_movelist = unpack_movelist(validation_matches[i])
        board, player, previous_moves_pred = initialize_game_full()
        success= 0
        for move in unpacked_movelist:
            if move == 0:
                break
            feature_path = '/storage/hlynur/cache/validation/features/features_' + str(i) + "_" + str(move) + ".npy"
            label_path = '/storage/hlynur/cache/validation/labels/labels_' + str(i) + "_" + str(move) + ".npy"
            features, label = fetch_planes(move, feature_path, label_path)
            features = np.transpose(features)
            features = features[4:7,:,:]
            features = np.transpose(features)
            input_batch = [features]
            label_batch = [label]
            prediction = sess.run(pred_up, feed_dict={img_data:input_batch, ground_truths: label_batch})
            prediction = np.transpose(prediction[0])
            prediction = np.transpose(prediction[1])
            cleaned_predictions = zero_illegal_moves(prediction, find_legal_moves(board, player))
            pred_row, pred_col = np.unravel_index(cleaned_predictions.argmax(), cleaned_predictions.shape)
            move_argmax = str((pred_row+1) * 10 + (pred_col+1))
            if str(move) == str(move_argmax):
                success += 1
            success = check_rotational_invariance(board, move, move_argmax, success)
            board = make_move(board, move, player)
            player, legal_moves, previous_moves_pred = update_states(player, board, move, previous_moves_pred)
        successes.append(success)
    return np.mean(successes)

def avg_error(data_path, sess, img_data, ground_truths, loss, len_games = 4):
    errors = []
    validation_matches = get_all_matches(data_path)
    #validation_matches = validation_matches[0:len_games]
    for i in range(len(validation_matches)):
        unpacked_movelist = unpack_movelist(validation_matches[i])
        board, player, previous_moves_avg = initialize_game_full()
        for move in unpacked_movelist:
            if move == 0:
                break
            feature_path = '/storage/hlynur/cache/validation/features/features_' + str(i) + "_" + str(move) + ".npy"
            label_path = '/storage/hlynur/cache/validation/labels/labels_' + str(i) + "_" + str(move) + ".npy"
            features, label = fetch_or_calculate_planes(board, player, previous_moves_avg, move,
                                                        feature_path, label_path, fetch=True)
            features = np.transpose(features)
            features = features[4:7,:,:]
            features = np.transpose(features)
            input_batch = [features]
            label_batch = [label]
            error = sess.run(loss, feed_dict={img_data:input_batch, ground_truths: label_batch})
            errors.append(error)
            board = make_move(board, move, player)
            player, legal_moves, previous_moves_avg = update_states(player, board, move, previous_moves_avg)
    return np.mean(errors)

def prep_and_append_training_batch(step, action_batch, action, features_batch, state, player):
        feature_path = 'cache/training/features/features_' + str(step) + "_" + str(action) + ".npy"
        label_path = 'cache/training/labels/labels_' + str(step) + "_" + str(action) + ".npy"
        if os.path.isfile(feature_path) and os.path.isfile(label_path):
            try:
                features = np.load(feature_path)
                label = np.load(label_path)
            except:
                print("data corruption in match " + str(i))
                features = board_to_input(state, player)
                label = prepare_data(move_to_label(action))
        else:
            features = board_to_input(state, player)
            label = prepare_data(move_to_label(action))
        features_batch.append(features)
        action_batch.append(label)
        # Now we add 3 reflections of the game state
        # which is done by flipping the board over one diagonal        
        move_upright = flip_move_upright(action)
        features_upright = flip_features(features, 'upright')
        features_batch.append(features_upright)
        action_batch.append(prepare_data(move_to_label(move_upright)))
        
        # Then the other diagonal
        move_upleft = flip_move_upleft(action)
        features_upleft = flip_features(features, 'upleft')
        features_batch.append(features_upleft)
        action_batch.append(prepare_data(move_to_label(move_upleft)))
        
        # Then both diagonals
        move_both = flip_move_upright(flip_move_upleft(action))
        features_both = flip_features(features, 'both')
        features_batch.append(features_both)
        action_batch.append(prepare_data(move_to_label(move_both)))
        return features_batch, action_batch

def policy_loss(data_path, test_sess, test_features, test_actions, test_keep, test_loss, test_pred, games=10):
    errors = []
    validation_matches = get_all_matches(data_path)
    #XXX: Delete this line when testing is faster
    validation_matches = validation_matches[0:games]
    successes = []
    for i in range(len(validation_matches)):
        match = validation_matches[i]
        raw_match_movelist = match[8:]
        unpacked_movelist = unpack('b'*60, raw_match_movelist)
        board = initialize_game()
        player = -1
        success = 0
        for move in unpacked_movelist:
            if move == 0:
                break
            feature_path = 'cache/validation/features/features_' + str(i) + "_" + str(move) + ".npy"
            label_path = 'cache/validation/labels/labels_' + str(i) + "_" + str(move) + ".npy"
            if os.path.isfile(feature_path) and os.path.isfile(label_path):
                features = np.load(feature_path)
                label = np.load(label_path)
            else:
                features = board_to_input(board, player)
                label = prepare_data(move_to_label(move))
                
            input_batch = [features]
            label_batch = [label]
            error = test_sess.run(test_loss, feed_dict={test_features:input_batch, test_actions: label_batch, test_keep:1.0})
            errors.append(error)
            prediction = test_sess.run(test_pred, feed_dict={test_features:input_batch, test_actions: label_batch, test_keep:1.0})
            prediction = np.transpose(prediction[0])
            prediction = np.transpose(prediction[1])
            legal_moves = find_legal_moves(board, player)
            cleaned_predictions = zero_illegal_moves(prediction, legal_moves)
            unravel_i,unravel_j = np.unravel_index(cleaned_predictions.argmax(), cleaned_predictions.shape)
            move_argmax = str((unravel_i+1) * 10 + (unravel_j+1))
            if str(move) == str(move_argmax):
                success += 1
            original_board = np.array(board)
            board_upright = np.transpose(original_board)
            board_upleft = np.rot90(np.rot90(board_upright))
            board_both_flips = np.transpose(board_upleft)
            if np.array_equal(board, board_upright):
                if str(move_argmax) == flip_move_upright(move):
                    success += 1
            if np.array_equal(board, board_upleft):
                if str(move_argmax) == flip_move_upleft(move):
                    success += 1
            if np.array_equal(board, board_both_flips):
                if str(move_argmax) == flip_move_upright(flip_move_upleft(move)):
                    success += 1
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
        successes.append(success)
    return np.sum(errors) / len(errors), (np.mean(successes) / float(60))


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

def add_flips(inputs, labels, feature_planes, next_move):
    # Now we add 3 reflections of the game state
    # which is done by flipping the board over one diagonal        
    move_upright = flip_move_upright(next_move)
    features_upright = flip_features(feature_planes, 'upright')
    inputs.append(features_upright)
    labels.append(prepare_data(move_to_label(move_upright)))

    # Then the other diagonal
    move_upleft = flip_move_upleft(next_move)
    features_upleft = flip_features(feature_planes, 'upleft')
    inputs.append(features_upleft)
    labels.append(prepare_data(move_to_label(move_upleft)))

    # Then both diagonals
    move_both = flip_move_upright(flip_move_upleft(next_move))
    features_both = flip_features(feature_planes, 'both')
    inputs.append(features_both)
    labels.append(prepare_data(move_to_label(move_both)))
    return inputs, labels

def fetch_or_calculate_planes(board, player, previous_moves, move, feature_path, label_path, fetch):
    if fetch:
        if os.path.isfile(feature_path) and os.path.isfile(label_path):
            try:
                features = np.load(feature_path)
                label = np.load(label_path)
            except:
                print("problem loading cached matchs")
                features = board_to_input(board, player, previous_moves)
                label = prepare_data(move_to_label(move))
        else:
            print("trying to load uncached match")
            features = board_to_input(board, player, previous_moves)
            label = prepare_data(move_to_label(move))
    else:
        features = board_to_input(board, player, previous_moves)
        label = prepare_data(move_to_label(move))
    return features, label

def fetch_planes(move, feature_path, label_path, board = False, player = False):
    if os.path.isfile(feature_path) and os.path.isfile(label_path):
        try:
            features = np.load(feature_path)
            label = np.load(label_path)
        except:
            print("problem loading cached matchs")
            features = "Error"
            label = "Error"
            #features = board_to_input(board, player, previous_moves)
            #label = prepare_data(move_to_label(move))
    else:
        print("trying to load uncached match")
        features = board_to_input(board, player, previous_moves)
        label = prepare_data(move_to_label(move))
    return features, label

def check_rotational_invariance(board, move, move_argmax, success):
    original_board = np.array(board)
    board_upright = np.transpose(original_board)
    board_upleft = np.rot90(np.rot90(board_upright))
    board_both_flips = np.transpose(board_upleft)
    if np.array_equal(board, board_upright):
        if str(move_argmax) == flip_move_upright(move):
            success += 1
        if np.array_equal(board, board_upleft):
            if str(move_argmax) == flip_move_upleft(move):
                success += 1
        if np.array_equal(board, board_both_flips):
            if str(move_argmax) == flip_move_upright(flip_move_upleft(move)):
                success += 1
    return success

def log_experiment(log_file, log_time, log_acc, log_loss, i):
    print('%s, Step %d, Accuracy = %.3f, Loss = %.3f' % (log_time, i, log_acc, log_loss))
    with open(log_file, "a") as myfile:
        myfile.write(log_time)
        myfile.write(", Step ")
        myfile.write(str(i))
        myfile.write(": ")
        myfile.write(str(log_acc))
        myfile.write(" ")
        myfile.write(str(log_loss))
        myfile.write("\n")
