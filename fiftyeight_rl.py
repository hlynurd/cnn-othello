#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import deque
from tensorflow.python.framework import ops
from rl_reinforce import REINFORCEothello
from othello_net import *
from othello_rules import *
from feature_extractor import *
import os, random, sys
import tensorflow as tf
import numpy as np
from datetime import datetime
from example_states import *
from training_utils import *
np.set_printoptions(precision=2)

def sample_action(prediction):
    prediction = np.transpose(prediction[0])
    prediction = np.transpose(prediction[1])
    legal_moves = find_legal_moves_c(board, player)
    prediction = prediction / np.sum(prediction)
    cleaned_predictions = zero_illegal_moves(prediction, legal_moves)
    p = cleaned_predictions.flatten()
    p = p / np.sum(p)
    sample_index = np.flatnonzero( np.random.multinomial(1,p,1) )[0]
    sampled_move = moves[sample_index]
    if prev_move == sampled_move:
        print("action probabilities"); print(p); print(prediction); print(cleaned_predictions);
    return sampled_move

moves = ['0'] * 64
for i in range(8):
    for j in range(8):
        moves[i*8 + j] = str((i+1) * 10 + (j+1))
        

batches = 1200
games_per_batch = 128
print("starting rl policy network")

graph_2 = tf.Graph()

with graph_2.as_default():
    img_data_2, train_step_2, optimizer_2, ground_truths_2, loss_2, pred_up_2,  learn_rate_2, score_out_2 = create_no_graph()

graph_1 = tf.Graph()
with graph_1.as_default():
    img_data_1, train_step_1, optimizer_1, ground_truths_1, loss_1, pred_up_1, learn_rate_1, score_out_1 = create_no_graph()

sess_1 = tf.Session(graph=graph_1)
sess_2 = tf.Session(graph=graph_2)

with sess_1.as_default():
    with graph_1.as_default():
        rl_reinforce_1 = REINFORCEothello(sess_1,
                          optimizer_1,
                          learn_rate_1,
                          loss_1,
                          score_out_1,
                          ground_truths_1,
                          img_data_1)
        tf.global_variables_initializer().run()
        saver_1 = tf.train.Saver(tf.global_variables())
        model_1= "models/rl_models/rl_fiftyeight.ckpt"
        if os.path.isfile(model_1 + ".meta"):
            print("locked and loaded 1")
            saver_1.restore(sess_1, model_1)
            
with sess_2.as_default():
    with graph_2.as_default():
        tf.global_variables_initializer().run()
        saver_2 = tf.train.Saver(tf.global_variables())
        model_2= "supervised/models/layers8filters64.ckpt"
        if os.path.isfile(model_2 + ".meta"):
            print("locked and loaded 2")
            saver_2.restore(sess_2, model_2)    


for batch in range(batches):
    N = games_per_batch
    graph_1 = -1
    graph_2 = 1
    graph_1_wins = 0
    graph_2_wins = 0
    failcount = 0
    for n in range(N):
        board, player, previous_moves = initialize_game_full()
        winner = 0
        prev_move = '00'
        input_batch = []
        label_batch = []
        while True:
            legal_moves = find_legal_moves_c(board, player)
            if len(legal_moves) == 0:
                winner = get_winner(board, 1, -1)
                if winner is graph_1:
                    graph_1_wins += 1
                    break
                if winner is graph_2:
                    graph_2_wins += 1
                    break
                player = player*(-1)
                failcount = failcount + 1
                if failcount > 3:
                    winner = -3
                    break
                continue
            features = board_to_input_c(board, player, previous_moves)
            if player is graph_1:
                prediction = sess_1.run(pred_up_1, feed_dict={img_data_1:[features]})
            else:
                prediction = sess_2.run(pred_up_2, feed_dict={img_data_2:[features]})
            sampled_move = sample_action(prediction)
            if prev_move == sampled_move:
                #print("illegal action sampled:" + str(sampled_move) + " in state:"); print(board); break;
                print("illegal move sampled");break;winner=-3;
            prev_move = sampled_move
            label = prepare_data(move_to_label(sampled_move))
            input_batch.append(features)
            label_batch.append(label)
            board = make_move(board, sampled_move, player)
            player, legal_moves, previous_moves = update_states(player, board, sampled_move, previous_moves)
        if winner is not -3:
            for j in range(len(input_batch)):
                state = input_batch[j]
                action = label_batch[j]
                if winner is -1:
                    reward = 1 if j% 2 is 0 else -0.2
                else:
                    reward = -0.2 if j% 2 is 0 else 1
                rl_reinforce_1.storeRollout(state, action, reward)
        graph_1 = graph_1 * (-1); graph_2 = graph_2 * (-1);
        if n+1 is games_per_batch:
            print('%s  %s wr: %.2f, %s wr: %.2f' % (datetime.now().strftime("%d. %H:%M:%S"), model_1[14:], graph_1_wins/float(N), model_2[14:], graph_2_wins/float(N)))
            with open("rl_logs.txt", "a") as myfile:
               myfile.write(str(graph_1_wins / float(N)))
               myfile.write("\n")
            graph_1_wins = 0; graph_2_wins = 0;
            rl_reinforce_1.updateModel()
#            save_path = saver_1.save(sess_1, "models/rl_models/rl_fiftyeight.ckpt")
print("done")
