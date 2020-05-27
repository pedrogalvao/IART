# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:19:35 2020

@author: Estudio
"""
from collections import deque
import numpy as np
import random
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Conv2DTranspose
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Reshape
from tensorflow.keras.layers import Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

def action_format(action, board_size):
    output = [[[0 for i in range(board_size)] for j in range(board_size)]]+[[[0 for i in range(board_size)] for j in range(board_size)]]
    output[0][action[0][0]][action[0][1]] = 1
    output[1][action[1][0]][action[1][1]] = 1
    return transpose_input(np.array(output))
    
def transpose_input(board):
    return np.transpose(board, (1, 2, 0))


# Deep Q-learning Agent
class DQNAgent:
    def __init__(self, board_size, action_size):
        self.board_size = board_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning 
        model = Sequential()
        model.add(Conv2D(32, kernel_size=3, activation='relu', input_shape=(self.board_size,self.board_size,5)))
        model.add(Conv2D(16, kernel_size=3, activation='relu'))
        model.add(Conv2DTranspose(16, kernel_size=3, activation='relu'))
        model.add(Conv2DTranspose(16, kernel_size=3, activation='relu'))
        model.add(Flatten())
        model.add(Dense(2*self.board_size**2, activation='softmax'))
        model.add(Reshape((self.board_size, self.board_size, 2)))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def save_model(self):
        self.model.save(self.weight_backup)

    def memorize(self, state, action, reward, next_state, done):
        state = transpose_input(state)
        next_state = transpose_input(next_state)
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        #if np.random.rand() <= self.epsilon:
         #   return random.randrange(self.action_size)
        state = transpose_input(state)
        act_values = self.model.predict(np.array([state]))
        act_values = np.transpose(act_values[0], (2, 0, 1))
        orig = np.unravel_index(np.argmax(act_values[0], axis=None), act_values[0].shape)
        dest = np.unravel_index(np.argmax(act_values[1], axis=None), act_values[1].shape)
        return [orig, dest]  # returns action

    def replay(self, batch_size):
        batch_size = min(batch_size, len(self.memory))
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            value = reward
            state = np.array([state])
            next_state = np.array([next_state])
            # if not done:
            #     value = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
           # target_f = self.model.predict(state)
            #print("target_f:",target_f)
            #target_f[0][action[0][0]][action[0][1]] *= (target +1)
            target = action_format(action, self.board_size)*(value+1)
            print("input:", state)
            print("target:", target)
            self.model.fit(state, np.array([target]), epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay