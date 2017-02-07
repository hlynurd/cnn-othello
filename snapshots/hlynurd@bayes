#!/usr/bin/python
# -*- coding: utf-8 -*-
# from othello_rules import *
from othello_net import *
from tensorflow.python.framework import ops
from datetime import datetime
from example_states import *
from feature_extractor import *
from training_utils import *
import numpy as np
def avg_error(data_path, sess):
    errors = []
    validation_matches = get_all_matches(data_path)
    #XXX: Delete this line when testing is faster
    validation_matches = validation_matches[0:2]
    for i in range(len(validation_matches)):
        match = validation_matches[i]
        raw_match_movelist = match[8:]
        unpacked_movelist = unpack('b'*60, raw_match_movelist)
        board = initialize_game()
        player = -1
        previous_moves_avg = [56, 56, 56, 56]
        for move in unpacked_movelist:
            if move == 0:
                break
            features = board_to_input(board, player, previous_moves_avg)
            label = prepare_data(move_to_label(move))
                
            input_batch = [features]
            label_batch = [label]
            error = sess.run(loss, feed_dict={img_data:input_batch, ground_truths: label_batch, keep_prob:1.0, training:False})
            errors.append(error)
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
            previous_moves_avg[3] = previous_moves_avg[2]
            previous_moves_avg[2] = previous_moves_avg[1]
            previous_moves_avg[1] = previous_moves_avg[0]
            previous_moves_avg[0] = move
            #input_batch = prepare_data(board * )
            #label_batch = prepare_data(move_to_label(move))
    return np.sum(errors) / len(errors)

def prediction_accuracy(data_path, len_games=2):
    lengths = []
    successes = []
    validation_matches = get_all_matches(data_path)
    #XXX: Delete this line when testing is faster
    validation_matches = validation_matches[0:len_games]
    for i in range(len_games):
        test_match = validation_matches[i]
        board = initialize_game()
        #print(board)
        #print('\n')
        player = -1
        success = 0
        length = 0
        #test_match = matches[i]
        raw_match_movelist = test_match[8:]
        unpacked_movelist = unpack('b'*60, raw_match_movelist)
        previous_moves_pred = [56, 56, 56, 56]
        for move in unpacked_movelist:
            length += 1
            if move == 0:
                winner = get_winner(board, 1, -1)
                break

            '''
            feature_path = 'cache/validation/features/features_' + str(i) + "_" + str(move) + ".npy"
            label_path = 'cache/validation/labels/labels_' + str(i) + "_" + str(move) + ".npy"
            if not os.path.isfile(feature_path) and os.path.isfile(label_path):
                features = np.load(feature_path)
                label = np.load(label_path)
            else:
                features = board_to_input(board, player, previous_moves_pred)
                label = prepare_data(move_to_label(move))
            '''
            features = board_to_input(board, player, previous_moves_pred)
            label = prepare_data(move_to_label(move))
                
            input_batch = [features]
            label_batch = [label]
            prediction = sess.run(pred_up, feed_dict={img_data:input_batch, ground_truths: label_batch, keep_prob:1.0, training:False})
            np.set_printoptions(precision=2)
            prediction = np.transpose(prediction[0])
            prediction = np.transpose(prediction[1])
            legal_moves = find_legal_moves(board, player)
            cleaned_predictions = zero_illegal_moves(prediction, legal_moves)
            i,j = np.unravel_index(cleaned_predictions.argmax(), cleaned_predictions.shape)
            move_argmax = str((i+1) * 10 + (j+1))
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
        previous_moves_pred[3] = previous_moves_pred[2]
        previous_moves_pred[2] = previous_moves_pred[1]
        previous_moves_pred[1] = previous_moves_pred[0]
        previous_moves_pred[0] = move
        legal_moves = find_legal_moves(board, player)
        winner = get_winner(board, 1, -1)
        successes.append(success)
        lengths.append(length)
    
    return np.mean(successes)
# Ræsum graphið fyrir tensorflow
ops.reset_default_graph()
graph, img_data, train_step, optimizer, ground_truths, loss, pred_up, keep_prob, learn_rate, score_out, training = create_othello_net()
saver = tf.train.Saver()
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
init_op = tf.global_variables_initializer()
sess.run(init_op)
#current_model = "models/deleteme_4.ckpt"
#if os.path.isfile(current_model):
#    saver.restore(sess, current_model)
validation_path = "/storage/hlynur/unprocessed/validation/"
matches = get_all_matches('/storage/hlynur/unprocessed/training/')
lenmatches = len(matches)
print(lenmatches)

# Byrjum þjálfunina
print("start training")
#print("starting error:" + str(avg_error(validation_path, sess)))
#print('%s: Step %d: Prediction accuracy = %.2f' % (datetime.now(), 0,
#                                                      prediction_accuracy()/float(60)))
iterations = 5000
prev_stop = 0
probs = 1
batch_multiplier = 1
input_batch = []
label_batch = []
for i in range(prev_stop, prev_stop+iterations):
    #TODO: Skrifa þetta fall
    #input_batch, label_batch = prepare_train_batch(train_ids, batch_size, do_flips, do_rots, data_path)
    current_match = matches[i]
    raw_match_movelist = current_match[8:]
    unpacked_movelist = unpack('b'*60, raw_match_movelist)    
    board = initialize_game()
    training_stability = np.zeros((8,8))
    player = -1
    # One training batch is all the data from one match
    previous_moves = [56, 56, 56, 56]
    for move in unpacked_movelist:
        if move == 0:
            break
        # TODO: Athuga hvernig rotation sé löglegt og bæta þeim svo við
        feature_path = '/storage/hlynur/cache/training/features/features_' + str(i) + "_" + str(move) + ".npy"
        label_path = '/storage/hlynur/cache/training/labels/labels_' + str(i) + "_" + str(move) + ".npy"
        #XXX: Virðist vera helvíti böggað ef ég tek 'not' í burtu frá hér fyrir neðan!
        
        if  os.path.isfile(feature_path) and os.path.isfile(label_path):
            try:
                features = np.load(feature_path)
                label = np.load(label_path)
            except:
                print("data corruption in match " + str(i))
                features = board_to_input(board, player, previous_moves)
                label = prepare_data(move_to_label(move))
        else:
            features = board_to_input(board, player, previous_moves)
            label = prepare_data(move_to_label(move))
        
       # features = board_to_input(board, player, previous_moves)
       # label = prepare_data(move_to_label(move))
        input_batch.append(features)
        label_batch.append(label)
        # Now we add 3 reflections of the game state
        # which is done by flipping the board over one diagonal        
        move_upright = flip_move_upright(move)
        features_upright = flip_features(features, 'upright')
        input_batch.append(features_upright)
        label_batch.append(prepare_data(move_to_label(move_upright)))

        # Then the other diagonal
        move_upleft = flip_move_upleft(move)
        features_upleft = flip_features(features, 'upleft')
        input_batch.append(features_upleft)
        label_batch.append(prepare_data(move_to_label(move_upleft)))

        # Then both diagonals
        move_both = flip_move_upright(flip_move_upleft(move))
        features_both = flip_features(features, 'both')
        input_batch.append(features_both)
        label_batch.append(prepare_data(move_to_label(move_both)))


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
    start = 6e-4
    eta = start
    if i % batch_multiplier is 0:
        train_step.run(session=sess, feed_dict={img_data:input_batch,
                                                ground_truths: label_batch,
                                                keep_prob:probs,
                                                learn_rate:eta,
                                                training:True})
        input_batch = []
        label_batch = []
        games_to_batch = 0

    if (i % 10 is 0) and (i > 0 and i < 51) or (i+1) == (iterations+prev_stop) or (i % 50 is 0):  
        with open("logs.txt", "a") as myfile:
                myfile.write(datetime.now().strftime("%d. %b %H:%M:%S"))
                myfile.write(", Step ")
                myfile.write(str(i))
                myfile.write(": ")
                myfile.write(str(prediction_accuracy(validation_path) / float(60)))
                myfile.write(" ")
                myfile.write(str(avg_error(validation_path, sess)))
                myfile.write("\n")
        #save_path = saver.save(sess, current_model)

print("done")
