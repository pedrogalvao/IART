# -*- coding: utf-8 -*-
"""
Created on Tue May 26 09:07:49 2020

@author: Estudio
"""
import gym
import numpy as np
from DQNAgent import *
from bot import Bot
from PivitEnv import *

class Test:
    def __init__(self):
        self.sample_batch_size = 32
        self.episodes          = 10
        self.env               = PivitEnv(6)

        self.state_size        = 6#self.env.observation_space.shape[0]
        self.action_size       = 6#self.env.action_space.n
        self.dqnagent          = DQNAgent(self.state_size)
        self.minimax           = Bot()
           
    def testDQN(self):
        """Testar DQN jogando contra si"""
        dqn_points=0
        for index_episode in range(self.episodes):
            state = self.env.reset()
            #state = np.reshape(state, [1, self.state_size])
            done = False
            index = 0
            while not done:
                 action = self.dqnagent.act(state,index%2)
                 if action == None:
                     break
                 next_state, reward, done, _ = self.env.step(action)
                 if reward>=0:
                     print("DQNAgent made a valid move")
                     reward=1
                 self.dqnagent.memorize(change_colors(state), action, reward, change_colors(next_state), done)
                 dqn_points += reward
                 state = next_state
                 index += 1
                 if index==100:
                    break
        self.dqnagent.replay(self.sample_batch_size)
        return dqn_points
           
    def testMinimaxDQN(self):
        """Testar DQN jogando contra MinMax"""
        dqn_points=0
        minmax_points=0
        for index_episode in range(self.episodes):
            state = self.env.reset()
            #state = np.reshape(state, [1, self.state_size])
            done = False
            index = 0
            while not done:
                 action = self.minimax.act(box_to_board(state), 1, 0)
                 if action == None:
                     break
                 next_state, reward, done, _ = self.env.step(action)
                 self.dqnagent.memorize(state, action, reward+1, next_state, done)
                 minmax_points += reward
                 state = next_state
                 action = self.dqnagent.act(state,1)
                 if action == None:
                     break
                 next_state, reward, done, _ = self.env.step(action)
                 if reward>=0:
                     print("DQNAgent made a valid move")
                     reward=1
                 self.dqnagent.memorize(change_colors(state), action, reward, change_colors(next_state), done)
                 dqn_points += reward
                 state = next_state
                 
                 index += 1
                 if index==100:
                    break
        self.dqnagent.replay(self.sample_batch_size)
        return minmax_points, dqn_points
                
            
    def testMinimax(self):
            try:
                for index_episode in range(self.episodes):
                    state = self.env.reset()
                    done = False
                    index = 0
                    while not done:
                         action = self.minimax.act(box_to_board(state),1,index%2)
                         if action == None:
                             break
                         next_state, reward, done, _ = self.env.step(action)
                         
                         self.dqnagent.memorize(state, action, reward, next_state, done)
                         state = next_state
                         index += 1
                         if index==100:
                             break
                    print("Episode", index_episode, "Number of moves:", index + 1)
                    self.dqnagent.replay(self.sample_batch_size)
            finally:
                self.dqnagent.save_model()
                
if __name__ == "__main__":
    test = Test()
    test.testMinimaxDQN()