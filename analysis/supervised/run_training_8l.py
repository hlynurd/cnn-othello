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
ops.reset_default_graph()
graph, img_data, train_step, optimizer, ground_truths, loss, pred_up, learn_rate, score_out = create_othello_net_8l_43()
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
init_op = tf.global_variables_initializer()
sess.run(init_op)
current_model = "models/convothello_reg_8l.ckpt"
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
logfile = "logfile_sl_8l_reg"
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
    if i is 0:
        log_time = datetime.now().strftime("%d. %b %H:%M:%S")
        log_acc = prediction_accuracy(sess, img_data, ground_truths, pred_up, validation_path)/float(60)
        log_loss = avg_error(validation_path, sess, img_data, ground_truths, loss)
        log_experiment(logfile + ".txt", log_time, log_acc, log_loss, i)
        log_experiment(logfile + "_train.txt", log_time, 0, np.mean(train_losses), i)
        save_path = saver.save(sess, current_model)
        train_losses = []

print("done")

