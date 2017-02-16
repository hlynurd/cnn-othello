import os
import random
import numpy as np
import tensorflow as tf

class REINFORCEothello(object):

  def __init__(self, session,
                     optimizer,
                     learn_rate,
                     loss,
                     policy_network,
                     taken_actions,
                     states,
                     eta = 3e-6,
                     discount_factor=1, # discount future rewards
                    ):

    # tensorflow machinery
    self.session        = session
    self.optimizer      = optimizer
    self.learn_rate     = learn_rate
    self.eta            = eta
    # model components
    self.policy_network  = policy_network
    
    self.loss            = loss 
    self.gradients       = self.optimizer.compute_gradients(self.loss)
    self.states          = states
    self.policy_outputs  = policy_network
    self.taken_actions   = taken_actions
    # training parameters
    self.discount_factor = discount_factor

    # counters
    self.train_iteration = 0

    # rollout buffer
    self.state_buffer  = []
    self.reward_buffer = []
    self.action_buffer = []

    # record reward history for normalization
    self.all_rewards = []
    self.max_reward_length = 1000000
    # create and initialize variables
    self.create_variables()
    var_lists = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
    self.session.run(tf.variables_initializer(var_lists))

    # make sure all variables are initialized
    self.session.run(tf.assert_variables_initialized())


  def create_variables(self):
    self.discounted_rewards = tf.placeholder(tf.float32, (None,), name="op1")
    # compute policy gradients
    for i, (grad, var) in enumerate(self.gradients):
      if grad is not None:
        self.gradients[i] = (grad * self.discounted_rewards, var)

    # training update
    # apply gradients to update policy network
    self.train_op = self.optimizer.apply_gradients(self.gradients)
    self.no_op = tf.no_op()

  def updateModel(self):

    N = len(self.reward_buffer)
    r = 0 # use discounted reward to approximate Q value

    # compute discounted future rewards
    discounted_rewards = np.zeros(N)
    for t in reversed(xrange(N)):
      # future discounted reward from now on
      r = self.reward_buffer[t] #+ self.discount_factor * r
      
      discounted_rewards[t] = r
    # reduce gradient variance by normalization
    self.all_rewards += discounted_rewards.tolist()
    self.all_rewards = self.all_rewards[:self.max_reward_length]
    #discounted_rewards -= np.mean(self.all_rewards)
    #discounted_rewards /= np.std(self.all_rewards)


    # update policy network with the rollout in batches
    for t in xrange(N-1):

      # prepare inputs
      states  = self.state_buffer[t][np.newaxis, :]
      actions = np.array([self.action_buffer[t]])
       
      rewards = np.array([discounted_rewards[t]])
      #print(rewards)
      #print(len(discounted_rewards))
      # evaluate gradients
      grad_evals = [grad for grad, var in self.gradients]
      _, summary_str = self.session.run([
        self.train_op,
        self.no_op
      ], {
        self.states:              states,
        self.taken_actions:      actions,
        self.discounted_rewards: rewards,
                
        self.learn_rate :       self.eta
      })

    self.train_iteration += 1
    # clean up
    self.cleanUp()

  def storeRollout(self, state, action, reward):
    self.action_buffer.append(action)
    self.reward_buffer.append(reward)
    self.state_buffer.append(state)

  def cleanUp(self):
    self.state_buffer  = []
    self.reward_buffer = []
    self.action_buffer = []
