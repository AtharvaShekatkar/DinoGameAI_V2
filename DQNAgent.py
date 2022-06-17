#Implementing Deep Q Learning
import tensorflow as tf
import pandas as pd
import numpy as np
from collections import deque
import random
from Globals import *

class DQNAgent:
    def __init__(self) -> None:
        # creating the main model
        # used for fitting at each step

        self.model = self.create_model()

        # creating the target model
        # used for predicting at each step
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        # memory that is kept to learn from
        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

        # counter for updating the target model
        self.target_update_counter = 0

    
    def create_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Input(shape=(5,)))
        # model.add(tf.keras.layers.Dropout(0.2))
        # model.add(tf.keras.layers.Dense(4, activation='relu'))
        # model.add(tf.keras.layers.Dropout(0.2))
        model.add(tf.keras.layers.Dense(3))

        model.compile(
            optimizer='adam',
            loss=tf.keras.losses.MeanSquaredError(),
            metrics=['accuracy']
        )

        return model
    

    # Update the memory store
    def update_replay_memory(self, transition):
        # if len(self.replay_memory) > 50_000:
        #     self.replay_memory.clear()
        self.replay_memory.append(transition)
    

    # Get the q values for the given state
    def get_qs(self, state):
        return self.model(np.array([state]), training=False)[0]
    

    # train the neural networks
    def train(self, terminal_state, step):
        # Start training only if a certain number of examples is available in memory
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return
        
        # Get a minibatch of random samples from memory
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        # Get current states for minibatch and then query the NN for Q values
        current_states = np.array([transition[0] for transition in minibatch])
        current_qs_list = self.model(current_states, training=False).numpy()

        # Get future states for minibatch and then query the target NN for Q values

        new_current_states = np.array([transition[3] for transition in minibatch])
        future_qs_list = self.target_model(new_current_states, training=False).numpy()

        X = []
        y = []

        # enumerate minibatch

        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):
            # If not a terminal state, get a new Q value from future states, else we set it to 0
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q
            else:
                new_q = reward
            

            # update q value for a given state
            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            X.append(current_state)
            y.append(current_qs)

        
        # Fit on all samples as one batch
        self.model.fit(np.array(X), np.array(y), batch_size=MINIBATCH_SIZE, shuffle=False, verbose=0)

        # Update target network every episode
        if terminal_state:
            self.target_update_counter += 1
        
        # If counter crosses threshold, update target network with the weights of the main network
        if self.target_update_counter > UPDATE_TARGET_THRESH:
            # print(self.target_update_counter)
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0
            # print(self.target_update_counter)