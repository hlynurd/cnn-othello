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
import time
from datetime import datetime
from example_states import *
from training_utils import *
from reinforcement_utils import *
import random
tf.logging.set_verbosity(tf.logging.FATAL)
np.set_printoptions(precision=2)

batches = 2000
games_per_batch = 128
tf_graph_1 = tf.Graph()
with tf_graph_1.as_default():
    img_1, train_step_1, adam_1, ground_truth_1, loss_1, pred_1, learn_rate_1, score_1 = create_no_graph()
sess_1 = tf.Session(graph=tf_graph_1)
    
tf_graph_2 = tf.Graph()
with tf_graph_2.as_default():
    img_2, train_step_2, adam_2, ground_truth_2, loss_2, pred_2, learn_rate_2, score_2 = create_no_graph()
sess_2 = tf.Session(graph=tf_graph_2)

with sess_1.as_default():
    with tf_graph_1.as_default():
        rl_reinforce_1 = REINFORCEothello(sess_1, adam_1, learn_rate_1, loss_1, score_1, ground_truth_1, img_1)
        tf.global_variables_initializer().run()
        saver_1 = tf.train.Saver(tf.global_variables(), max_to_keep=9999)
        model_1 = "supervised/models/layers8filters64.ckpt"
        if os.path.isfile(model_1 + ".meta"):
            saver_1.restore(sess_1, model_1)
            print("loaded graph 1 as " + model_1)
            
for batch in range(batches):
    if batch > 0:
        log_message = reinforcement_log(model_1, model_2, wins_1, wins_2, games_per_batch, "logs_rl.txt")
        rl_reinforce_1.updateModel()
        save_path = saver_1.save(sess_1, "/storage/hlynur/models/reinforcement_drill/drill_" + str(batch) + ".ckpt")
    with sess_2.as_default():
        with tf_graph_2.as_default():
            tf.global_variables_initializer().run()
            saver_2 = tf.train.Saver(tf.global_variables())
            model_2 = choose_opponent(batch)
            if os.path.isfile(model_2 + ".meta"):
                saver_2.restore(sess_2, model_2) 
                print("loaded graph 2 as " + model_2)
    graph_1, graph_2 = (-1, 1)
    wins_1, wins_2 = (0, 0)
    fails = 0
    for n in range(games_per_batch):
        board, player, previous_moves = initialize_game_full()
        winner = 0
        prev_move = '00'
        input_batch, label_batch = ([], [])
        graph_1, graph_2 = switch_sides(graph_1, graph_2)
        while True:
            legal_moves = find_legal_moves_c(board, player)
            if len(legal_moves) == 0:
                stop, wins_1, wins_2, fails, winner = end_check(board, wins_1, wins_2, graph_1, graph_2, fails)
                if winner is 1 or winner is -1:
                    if random.random() < 0.4:
                        for j in range(len(input_batch)):                
                            state, action, reward = prep_rl_rollout(input_batch, label_batch, winner, j)
                            rl_reinforce_1.storeRollout(state, action, reward)
                if stop:
                    break
                player = player*(-1)
                continue
            features = board_to_input_c(board, player, previous_moves)
            input_batch.append(features)
            if player is graph_1:
                prediction = sess_1.run(pred_1, feed_dict={img_1:[features]})
            else:
                prediction = sess_2.run(pred_2, feed_dict={img_2:[features]})
            sampled_move = sample_action(board, player, prediction)
            if illegal_move_check(prev_move, sampled_move, prediction) > 0:
                break
            prev_move = sampled_move
            label = prepare_data(move_to_label(sampled_move))
            label_batch.append(label)
            board = make_move(board, sampled_move, player)
            player, legal_moves, previous_moves = update_states(player, board, sampled_move, previous_moves)
print("done")
