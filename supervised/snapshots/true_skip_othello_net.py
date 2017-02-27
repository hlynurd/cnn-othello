# CP HERE :
import tensorflow as tf
from tensorflow.contrib.layers.python.layers import batch_norm as batch_norm

def conv_biases(o):
    shape = [o]
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv(input, kernel, p="SAME"):
    return tf.nn.conv2d(input, kernel, strides=[1, 1, 1, 1], padding=p)

def conv_nonparams(tensor_input, conv_weights, conv_biases, prev_conv):
    conv_in = conv(tensor_input, conv_weights)
    conv_relu = tf.nn.relu(conv_in + conv_biases + prev_conv)
    return conv_relu

def final_conv_nonparams(tensor_input, conv_weights, conv_biases):
    conv_in = conv(tensor_input, conv_weights)
    return conv_in

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


def create_true_skip_othello_net():
    #use_batch_normalization = False
    img_data = tf.placeholder(tf.float32, shape=[None, 8, 8, 43], name="img_data")
    training = tf.placeholder(tf.bool, name="training")
    #convolutional layers 
    i = 43; o = 64;
    conv1_weights = conv_weights(i, o)
    conv1_biases = conv_biases(o)
    #conv1_out = conv_nonparams(img_data, conv1_weights, conv1_biases, training)
    conv1_in = conv(img_data, conv1_weights)
    conv1_out = tf.nn.relu(conv1_in + conv1_biases)
    
    i = o
    conv2_weights = conv_weights(i, o)
    conv2_biases = conv_biases(o)
    conv2_in = conv(conv1_out, conv2_weights)
    conv2_out = tf.nn.relu(conv2_in + conv2_biases)
    

    conv3_weights = conv_weights(i, o)
    conv3_biases = conv_biases(o)
    conv3_out = conv_nonparams(conv2_out, conv3_weights, conv3_biases, conv2_out)
    
    
    conv4_weights = conv_weights(i, o)
    conv4_biases = conv_biases(o)
    conv4_out = conv_nonparams(conv3_out, conv4_weights, conv4_biases, conv3_out)
    #XXX: Use conv4_out into score_out for fast-net
    
    
    conv5_weights = conv_weights(i, o)
    conv5_biases = conv_biases(o)
    conv5_out = conv_nonparams(conv4_out, conv5_weights, conv5_biases, conv4_out)
    
    
    conv6_weights = conv_weights(i, o)
    conv6_biases = conv_biases(o)
    conv6_out = conv_nonparams(conv5_out, conv6_weights, conv6_biases, conv5_out)
    
    
    conv7_weights = conv_weights(i, o)
    conv7_biases = conv_biases(o)
    conv7_out = conv_nonparams(conv6_out, conv7_weights, conv7_biases, conv6_out)

    
    conv8_weights = conv_weights(i, o)
    conv8_biases = conv_biases(o)
    conv8_out = conv_nonparams(conv7_out, conv8_weights, conv8_biases, conv7_out)
   
    conv9_weights = conv_weights(i, o)
    conv9_biases = conv_biases(o)
    conv9_out = conv_nonparams(conv8_out, conv9_weights, conv9_biases, conv8_out)

    
    conv10_weights = conv_weights(i, o)
    conv10_biases = conv_biases(o)
    conv10_out = conv_nonparams(conv9_out, conv10_weights, conv10_biases, conv9_out)
    #scoring layer
    k = 1; i = o; o = 2;
    score_weights = weight_variable([k, k, i, o])
    score_biases = bias_variable([o])
    score_out = final_conv_nonparams(conv10_out, score_weights, score_biases)

    #final layer
    predictions = softmax(score_out, o)

    #training block:
    labels = tf.placeholder(tf.int64, shape=[None, 8, 8, 1], name="ground_truths")
    learn_rate = tf.placeholder(tf.float32, name="eta")
    
    
    loss = semantic_loss(score_out, labels, o)    
    optimizer = tf.train.AdamOptimizer(learn_rate)
    train_step = optimizer.minimize(loss)
    
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
    
    return sess.graph, img_data, train_step, optimizer, labels, loss, predictions, learn_rate, score_out
    
