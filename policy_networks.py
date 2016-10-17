# CP HERE :
import tensorflow as tf
from othello_net import *

def policy_net_4_layers(filters):
    img_data = tf.placeholder(tf.float32, shape=[None, 8, 8, 28], name="img_data")
    keep_prob = tf.placeholder(tf.float32, name="keep_prob")
    
    #convolutional layers 
    i = 28; o = filters;
    conv1_weights = conv_weights(i, o)
    conv1_biases = conv_biases(o)
    conv1_out = conv_nonparams(img_data, conv1_weights, conv1_biases, keep_prob)
    
    i = o
    conv2_weights = conv_weights(i, o)
    conv2_biases = conv_biases(o)
    conv2_out = conv_nonparams(conv1_out, conv2_weights, conv2_biases, keep_prob)
    
    conv3_weights = conv_weights(i, o)
    conv3_biases = conv_biases(o)
    conv3_out = conv_nonparams(conv2_out, conv3_weights, conv3_biases, keep_prob)
    
    conv4_weights = conv_weights(i, o)
    conv4_biases = conv_biases(o)
    conv4_out = conv_nonparams(conv3_out, conv4_weights, conv4_biases, keep_prob)
    #XXX: Use conv4_out into score_out for fast-net
    
    #scoring layer
    k = 1; i = o; o = 2;
    score_weights = weight_variable([k, k, i, o])
    score_biases = bias_variable([o])
    score_out = conv_nonparams(conv4_out, score_weights, score_biases, keep_prob)


    #final layer
    predictions = softmax(score_out, o)

    #training block:
    labels = tf.placeholder(tf.int64, shape=[None, 8, 8, 1], name="ground_truths")
    learn_rate = tf.placeholder(tf.float32, name="eta")
    
    
    loss = semantic_loss(score_out, labels, o)    
    optimizer = tf.train.AdamOptimizer(learn_rate)
    train_step = optimizer.minimize(loss)
    
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
    
    return sess.graph, img_data, train_step, optimizer, labels, loss, predictions, keep_prob, learn_rate, score_out
    
def policy_net_5_layers(filters):
    img_data = tf.placeholder(tf.float32, shape=[None, 8, 8, 28], name="img_data")
    keep_prob = tf.placeholder(tf.float32, name="keep_prob")
    
    #convolutional layers 
    i = 28; o = filters;
    conv1_weights = conv_weights(i, o)
    conv1_biases = conv_biases(o)
    conv1_out = conv_nonparams(img_data, conv1_weights, conv1_biases, keep_prob)
    
    i = o
    conv2_weights = conv_weights(i, o)
    conv2_biases = conv_biases(o)
    conv2_out = conv_nonparams(conv1_out, conv2_weights, conv2_biases, keep_prob)
    
    conv3_weights = conv_weights(i, o)
    conv3_biases = conv_biases(o)
    conv3_out = conv_nonparams(conv2_out, conv3_weights, conv3_biases, keep_prob)
    
    conv4_weights = conv_weights(i, o)
    conv4_biases = conv_biases(o)
    conv4_out = conv_nonparams(conv3_out, conv4_weights, conv4_biases, keep_prob)
    
    conv5_weights = conv_weights(i, o)
    conv5_biases = conv_biases(o)
    conv5_out = conv_nonparams(conv4_out, conv5_weights, conv5_biases, keep_prob)

    #scoring layer
    k = 1; i = o; o = 2;
    score_weights = weight_variable([k, k, i, o])
    score_biases = bias_variable([o])
    score_out = conv_nonparams(conv5_out, score_weights, score_biases, keep_prob)


    #final layer
    predictions = softmax(score_out, o)

    #training block:
    labels = tf.placeholder(tf.int64, shape=[None, 8, 8, 1], name="ground_truths")
    learn_rate = tf.placeholder(tf.float32, name="eta")
    
    
    loss = semantic_loss(score_out, labels, o)    
    optimizer = tf.train.AdamOptimizer(learn_rate)
    train_step = optimizer.minimize(loss)
    
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
    
    return sess.graph, img_data, train_step, optimizer, labels, loss, predictions, keep_prob, learn_rate, score_out
    
def policy_net_6_layers(filters):
    img_data = tf.placeholder(tf.float32, shape=[None, 8, 8, 28], name="img_data")
    keep_prob = tf.placeholder(tf.float32, name="keep_prob")
    
    #convolutional layers 
    i = 28; o = filters;
    conv1_weights = conv_weights(i, o)
    conv1_biases = conv_biases(o)
    conv1_out = conv_nonparams(img_data, conv1_weights, conv1_biases, keep_prob)
    
    i = o
    conv2_weights = conv_weights(i, o)
    conv2_biases = conv_biases(o)
    conv2_out = conv_nonparams(conv1_out, conv2_weights, conv2_biases, keep_prob)
    
    conv3_weights = conv_weights(i, o)
    conv3_biases = conv_biases(o)
    conv3_out = conv_nonparams(conv2_out, conv3_weights, conv3_biases, keep_prob)
    
    conv4_weights = conv_weights(i, o)
    conv4_biases = conv_biases(o)
    conv4_out = conv_nonparams(conv3_out, conv4_weights, conv4_biases, keep_prob)
    
    conv5_weights = conv_weights(i, o)
    conv5_biases = conv_biases(o)
    conv5_out = conv_nonparams(conv4_out, conv5_weights, conv5_biases, keep_prob)
    
    conv6_weights = conv_weights(i, o)
    conv6_biases = conv_biases(o)
    conv6_out = conv_nonparams(conv5_out, conv6_weights, conv6_biases, keep_prob)
    
    #scoring layer
    k = 1; i = o; o = 2;
    score_weights = weight_variable([k, k, i, o])
    score_biases = bias_variable([o])
    score_out = conv_nonparams(conv6_out, score_weights, score_biases, keep_prob)


    #final layer
    predictions = softmax(score_out, o)

    #training block:
    labels = tf.placeholder(tf.int64, shape=[None, 8, 8, 1], name="ground_truths")
    learn_rate = tf.placeholder(tf.float32, name="eta")
    
    
    loss = semantic_loss(score_out, labels, o)    
    optimizer = tf.train.AdamOptimizer(learn_rate)
    train_step = optimizer.minimize(loss)
    
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
    
    return sess.graph, img_data, train_step, optimizer, labels, loss, predictions, keep_prob, learn_rate, score_out
    
    
