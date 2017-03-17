#!/usr/bin/python
# -*- coding: utf-8 -*-
# from othello_rules import *
from othello_net import *
from named_nets import *
from tensorflow.python.framework import ops
from datetime import datetime
from feature_extractor import *
from training_utils import *
import numpy as np
import hashlib, random
import ConfigParser
import operator

config = ConfigParser.ConfigParser()
config.read("config.ini")
start_eta = config.get("myvars", "start_eta")
iterations = int(config.get("myvars", "iterations"))
batch_size = int(config.get("myvars", "batch_size"))
def avg_error(data_path, sess, len_games = 4):
    errors = []
    validation_matches = get_all_matches(data_path)
    validation_matches = validation_matches[0:len_games]
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

def prediction_accuracy(sess, img_data, ground_truths, pred_up, data_path, len_games=4):
    successes = []
    validation_matches = get_all_matches(data_path)
    validation_matches = validation_matches[0:len_games]
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

ops.reset_default_graph()
graph, img_data, train_step, optimizer, ground_truths, loss, pred_up, learn_rate, score_out = create_othello_net_7l_3()
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
init_op = tf.global_variables_initializer()
sess.run(init_op)
current_model = "models/convothello_exp_7l.ckpt"
saver = tf.train.Saver()
if os.path.isfile(current_model + ".meta"):
    print("locked and loaded")
    saver.restore(sess, current_model)
validation_path = "/storage/hlynur/unprocessed/validation/"
matches = get_all_matches('/storage/hlynur/unprocessed/training/')
lenmatches = len(matches)
print("start training")
input_batch = []
label_batch = []
train_losses = []
logfile = "logfile_sl_7l_exp"
print(lenmatches)
print(iterations)
print(lenmatches*iterations)
with open(logfile + ".txt", "a") as myfile:
        myfile.write(start_eta)
        myfile.write("\n")
with open(logfile + "_train.txt", "a") as myfile:
        myfile.write(start_eta)
        myfile.write("\n")
for ite in range(int(iterations*lenmatches)):
    i = ite % lenmatches
    unpacked_movelist = unpack_movelist(matches[i]) 
    # One training batch is all the data from one match
    for move in unpacked_movelist:
        if move == 0:
            break
        if random.random() < 0.95:
            continue
        feature_path = '/storage/hlynur/cache/training/features/features_' + str(i) + "_" + str(move) + ".npy"
        label_path = '/storage/hlynur/cache/training/labels/labels_' + str(i) + "_" + str(move) + ".npy"
        features, label = fetch_planes(move, feature_path, label_path)
        features = np.transpose(features)
        features = features[4:7,:,:]
        features = np.transpose(features)
        if features == "Error" or label == "Error":
            continue
        input_batch.append(features)
        label_batch.append(label)
        input_batch, label_batch = add_flips(input_batch, label_batch, features, move)
        #board = make_move(board, move, player)
        #player, legal_moves, previous_moves = update_states(player, board, move, previous_moves)
    eta = start_eta
    if len(input_batch) >= batch_size:        
        _, train_loss = sess.run([train_step, loss], feed_dict={img_data:input_batch[:batch_size],
                                  ground_truths: label_batch[:batch_size], learn_rate:eta})
        input_batch = input_batch[batch_size:]
        label_batch = label_batch[batch_size:]
        train_losses.append(np.mean(train_loss))
        
    #if (i % 100 is 0) and (i > 0 and i < 0) or (i+1) == (iterations+prev_stop) or (i % 24000 is 0):  
    if i%100 is 0:
        log_time = datetime.now().strftime("%d. %b %H:%M:%S")
        log_acc = prediction_accuracy(sess, img_data, ground_truths, pred_up, validation_path)/float(60)
        log_loss = avg_error(validation_path, sess)
        log_experiment(logfile + ".txt", log_time, log_acc, log_loss, i)
        log_experiment(logfile + "_train.txt", log_time, 0, np.mean(train_losses), i)
        save_path = saver.save(sess, current_model)
        train_losses = []

print("done")

