# CP HERE :
import tensorflow as tf
from tensorflow.contrib.layers.python.layers import batch_norm as batch_norm

def conv_biases(o):
    shape = [o]
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv(input, kernel, p="SAME"):
    return tf.nn.conv2d(input, kernel, strides=[1, 1, 1, 1], padding=p)

def conv_nonparams(tensor_input, conv_weights, conv_biases, keep_prob, training, use_bn):
    conv_in = conv(tensor_input, conv_weights)
    if use_bn:
        conv_bn = batch_norm_layer(conv_in + conv_biases, training)
        conv_relu = tf.nn.relu(conv_bn)        
    else:
        conv_relu = tf.nn.relu(conv_in + conv_biases)
    conv_drop = tf.nn.dropout(conv_relu, keep_prob)
    return conv_drop

def final_conv_nonparams(tensor_input, conv_weights, conv_biases, keep_prob):
    conv_in = conv(tensor_input, conv_weights)
    conv_drop = tf.nn.dropout(conv_in + conv_biases, keep_prob)
    return conv_drop

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv_weights(i, o):
    k = 3
    shape = [k, k, i, o]
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def softmax(tensor_input, o):
    input_reshaped = tf.reshape(tensor_input, [-1, o])
    predictions = tf.nn.softmax(input_reshaped)
    predictions_reshaped = tf.reshape(predictions, [1, 8, 8, o])
    return predictions_reshaped

def semantic_loss(logits, labels, o):
    logits_reshaped = tf.reshape(logits, [-1, o])
    labels_reshaped = tf.reshape(labels, [-1]) 
    loss = tf.nn.sparse_softmax_cross_entropy_with_logits(logits_reshaped, labels_reshaped)
    return loss

def batch_norm_layer(x,train_phase):
    bn_train = batch_norm(x, decay=0.9, center=True, scale=False,
    updates_collections=None,
    is_training=True)
    
    bn_inference = batch_norm(x, decay=0.9, center=True, scale=False,
    updates_collections=None,
    is_training=False)
    z = tf.cond(train_phase, lambda: bn_train, lambda: bn_inference)
    return z


def create_othello_net():
    use_batch_normalization = False
    img_data = tf.placeholder(tf.float32, shape=[None, 8, 8, 43], name="img_data")
    keep_prob = tf.placeholder(tf.float32, name="keep_prob")
    training = tf.placeholder(tf.bool, name="training")
    #convolutional layers 
    i = 43; o = 32;
    conv1_weights = conv_weights(i, o)
    conv1_biases = conv_biases(o)
    conv1_out = conv_nonparams(img_data, conv1_weights, conv1_biases, keep_prob, training, use_batch_normalization)
    
    i = o; o = 32;
    conv2_weights = conv_weights(i, o)
    conv2_biases = conv_biases(o)
    conv2_out = conv_nonparams(conv1_out, conv2_weights, conv2_biases, keep_prob, training, use_batch_normalization)
    
    i = o; o = 32;
    conv3_weights = conv_weights(i, o)
    conv3_biases = conv_biases(o)
    conv3_out = conv_nonparams(conv2_out, conv3_weights, conv3_biases, keep_prob, training, use_batch_normalization)
    
    #i = o; o = 32;
    #conv4_weights = conv_weights(i, o)
    #conv4_biases = conv_biases(o)
    #conv4_out = conv_nonparams(conv3_out, conv4_weights, conv4_biases, keep_prob)
    #XXX: Use conv4_out into score_out for fast-net
    
    #i = o; o = 32;
    #conv5_weights = conv_weights(i, o)
    #conv5_biases = conv_biases(o)
    #conv5_out = conv_nonparams(conv4_out, conv5_weights, conv5_biases, keep_prob)
    
    #i = o; o = 32 ;
    #conv6_weights = conv_weights(i, o)
    #conv6_biases = conv_biases(o)
    #conv6_out = conv_nonparams(conv5_out, conv6_weights, conv6_biases, keep_prob)
    
    #scoring layer
    k = 1; i = o; o = 2;
    score_weights = weight_variable([k, k, i, o])
    score_biases = bias_variable([o])
    score_out = final_conv_nonparams(conv3_out, score_weights, score_biases, keep_prob)


    #final layer
    predictions = softmax(score_out, o)

    #training block:
    labels = tf.placeholder(tf.int64, shape=[None, 8, 8, 1], name="ground_truths")
    learn_rate = tf.placeholder(tf.float32, name="eta")
    
    
    loss = semantic_loss(score_out, labels, o)    
    optimizer = tf.train.AdamOptimizer(learn_rate)
    train_step = optimizer.minimize(loss)
    
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
    
    return sess.graph, img_data, train_step, optimizer, labels, loss, predictions, keep_prob, learn_rate, score_out, training
    