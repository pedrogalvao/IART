# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:19:35 2020

@author: Estudio
"""
from collections import deque
import numpy as np
import random
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Conv2DTranspose
from tensorflow.keras.layers import Maximum
from tensorflow.keras.layers import Minimum
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Reshape
from tensorflow.keras.layers import Concatenate
from tensorflow.keras.layers import Softmax
from tensorflow.keras.layers import Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model


def action_format(action, board_size):
    output = [[[0 for i in range(board_size)] for j in range(board_size)]]+[[[0 for i in range(board_size)] for j in range(board_size)]]
    output[0][action[0][0]][action[0][1]] = 1
    output[1][action[1][0]][action[1][1]] = 1
    return transpose_input(np.array(output))
    
def transpose_input(board):
    return np.transpose(board, (1, 2, 0))

def change_colors(box):
    box=np.array(box)
    return np.array([box[2],box[3],box[0],box[1],box[4]])
    

# Deep Q-learning Agent
class DQNAgent:
    def __init__(self, board_size):
        self.board_size = board_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning 
        input_ = Input(shape=(self.board_size,self.board_size,5))
        print("input:",input_.shape)
        red = Maximum()([input_[:,:,:,0],input_[:,:,:,1]])
        print("red:",red.shape)
        #blue = Maximum()([input_[:,:,2],input_[:,:,3]])
        conv_1 = Conv2D(32, kernel_size=3, activation='relu')(input_)
        conv_2 = Conv2D(32, kernel_size=3, activation='relu')(conv_1)
        deconv_3 = Conv2DTranspose(32, kernel_size=3, activation='relu')(conv_2)
        deconv_4 = Conv2DTranspose(32, kernel_size=3, activation='relu')(deconv_3)
        flatten_1 = Flatten()(deconv_4)
        print("flatten:", flatten_1.shape)
        dense_6a = Dense(self.board_size**2, activation='relu')(flatten_1[:,0:self.board_size**2])
        dense_6b = Dense(self.board_size**2, activation='relu')(flatten_1[:,self.board_size**2:])
        print("dense:", dense_6b.shape)
        reshape_7a = Reshape((self.board_size, self.board_size))(dense_6a)
        print("reshape a:", reshape_7a.shape)
        reshape_7b = Reshape((self.board_size, self.board_size,1))(dense_6b)
        print("reshape b:",reshape_7b.shape)
        # flatten_red = Flatten()(red)
        # print("flatten red b:",flatten_red.shape)
        #reshape_red = Reshape((self.board_size, self.board_size,1))(flatten_red)
        #print("reshape red:", reshape_red.shape)
        min_a = Minimum()([reshape_7a, red])
        print("min:",min_a.shape)
        
        flatten_2a = Flatten()(min_a)
        print("flatten a:", flatten_2a.shape)
        softmax_a = Softmax(axis=1)(flatten_2a)
        print("softmax_a:", softmax_a.shape)
        
        flatten_2b = Flatten()(reshape_7b)
        print("flatten b:", flatten_2b.shape)
        softmax_b = Softmax(axis=1)(flatten_2b)
        print("softmax_b:", softmax_a.shape)
        
        reshape_a = Reshape((self.board_size, self.board_size,1))(softmax_a)
        reshape_b = Reshape((self.board_size, self.board_size,1))(softmax_b)
        print("reshape a:",reshape_a.shape)
        concat = Concatenate(axis=-1)([reshape_a, reshape_b])
        model = Model(inputs=input_, outputs=concat)
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def save_model(self):
        self.model.save("model")
    
    def load_model(self):
        self.model = load_model("model")

    def memorize(self, state, action, reward, next_state, done):
        print('mem')
        state = transpose_input(state)
        next_state = transpose_input(next_state)
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, player=None):
        #if np.random.rand() <= self.epsilon:
         #   return random.randrange(self.action_size)
        if player == 1:
            state = change_colors(state)
        state = transpose_input(state)
        act_values = self.model.predict(np.array([state]))
        act_values = np.transpose(act_values[0], (2, 0, 1))
        orig = np.unravel_index(np.argmax(act_values[0], axis=None), act_values[0].shape)
        dest = np.unravel_index(np.argmax(act_values[1], axis=None), act_values[1].shape)
        print(orig)
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
            self.model.fit(state, np.array([target]), epochs=1, verbose=0)
            print('.')
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay