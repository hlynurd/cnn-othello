from __future__ import print_function
from collections import deque
from tensorflow.python.framework import ops
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
import numpy as np
test = policy_gradient_example()
test = np.transpose(test)
board = test
player = -1

tf.logging.set_verbosity(tf.logging.FATAL)
total_time = datetime.now() - datetime.now()
np.set_printoptions(precision=2)
tf.reset_default_graph()

tf_graph_1 = tf.Graph()
with tf_graph_1.as_default():
    img_1, train_step_1, adam_1, ground_truth_1, loss_1, pred_1, learn_rate_1, score_1 = create_no_graph()
sess_1 = tf.Session(graph=tf_graph_1)

with sess_1.as_default():
    with tf_graph_1.as_default():
        tf.global_variables_initializer().run()
        saver_1 = tf.train.Saver(tf.global_variables(), max_to_keep=9999)
for i in range(1000):
    if i % 100 is 0:
        print(i)
    start = datetime.now()
    features = [board_to_input_c_small(test, -1, ['45', '67', '12', '41'])]
    prediction = sess_1.run(pred_1, feed_dict={img_1:features})
    end = datetime.now()
    #print("time taken: " + str(end - start))
    total_time = total_time + end - start
print("total_time: "  + str(total_time))
