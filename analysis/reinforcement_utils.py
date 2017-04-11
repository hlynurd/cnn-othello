#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import random
from training_utils import *
moves = ['0'] * 64
for i in range(8):
    for j in range(8):
        moves[i*8 + j] = str((i+1) * 10 + (j+1))

def sample_action(board, player, prediction):
    prediction = np.transpose(prediction[0])
    prediction = np.transpose(prediction[1])
    legal_moves = find_legal_moves_c(board, player)
    if len(legal_moves) < 1:
        return 'Pass'
    
    cleaned_predictions = zero_illegal_moves(prediction, legal_moves)
    cleaned_predictions = cleaned_predictions / np.sum(cleaned_predictions)
    #print(cleaned_predictions)
    p = cleaned_predictions.flatten()
    p = p / np.sum(p)
    sample_index = np.flatnonzero( np.random.multinomial(1,p,1) )[0]
    sampled_move = moves[sample_index]
    return sampled_move

def illegal_move_check(prev_move, sampled_move, prediction):
    if prev_move == sampled_move:
        print("ILLEGAL MOVE SAMPLED")
        prediction = np.transpose(prediction[0])
        prediction = np.transpose(prediction[1])
        print("total probabilities are: " + str(np.sum(prediction)))
        return 1
    else:
        return -1

def get_reward(winner, timestep):
    if winner is -1:
        reward = 1 if timestep % 2 is 0 else -0.2
    else:
        reward = -0.2 if timestep % 2 is 0 else 1
    return reward

def end_check(board, graph_1_wins, graph_2_wins, graph_1, graph_2, failcount):
    stop_game = False
    winner = get_winner(board, 1, -1)
    if winner is graph_1:
        graph_1_wins += 1
        stop_game = True
    elif winner is graph_2:
        graph_2_wins += 1
        stop_game = True
    else:
        failcount = failcount + 1
    if failcount > 3:
        stop_game = True
    return stop_game, graph_1_wins, graph_2_wins, failcount, winner

def reinforcement_log(model_1, model_2, wins_1, wins_2, N, log_file):
    current_time = datetime.now().strftime("%d. %H:%M:%S")
    log_message = '%s  %s wr: %.2f, %s wr: %.2f' % (current_time, model_1[14:], wins_1/float(N), model_2[14:], wins_2/float(N))
    print(log_message)
    with open("rl_logs.txt", "a") as myfile:
       myfile.write(log_message)
       myfile.write("\n")
        
def prep_rl_rollout(input_batch, label_batch, winner, j):
    state = input_batch[j]
    action = label_batch[j]
    reward = get_reward(winner, j)
    return state, action, reward
    
def switch_sides(graph_1, graph_2):
    return graph_1 * (-1), graph_2 * (-1)
    
def choose_opponent(batch):
    #if batch % test_game_batch == 0:
    if batch == 0:
        model_2 = 'supervised/models2/layers8filters64.ckpt'
    else:
        all_files = os.listdir("models/reinforcement_drill/")
        no_meta = [i for i in all_files if not ('meta' in i or 'checkpoint' in i or 'data' in i)]
        model_2 = 'models/reinforcement_drill/' + random.choice(no_meta)
    return model_2[:-6]