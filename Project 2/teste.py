# -*- coding: utf-8 -*-
"""
Created on Tue May 26 09:07:49 2020

@author: Estudio
"""
import gym
import numpy as np
from DQNAgent import DQNAgent
from bot import Bot
from PivitEnv import *

class Test:
    def __init__(self):
        self.sample_batch_size = 32
        self.episodes          = 1
        self.env               = PivitEnv(6)

        self.state_size        = 6#self.env.observation_space.shape[0]
        self.action_size       = 6#self.env.action_space.n
        self.dqnagent          = DQNAgent(self.state_size, self.action_size)
        self.minimax           = Bot()
           
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
#                    self.env.render()
                 #action = self.agent.act(state)
                 action = self.minimax.act(box_to_board(state),1,1)
                 print(state)
                 print(action)
                 next_state, reward, done, _ = self.env.step(action)
                 minmax_points += reward
                 state = next_state
                 
                 action = self.dqnagent.act(state)
                 print(state)
                 print(action)
                 next_state, reward, done, _ = self.env.step(action)
                 dqn_points += reward
                 state = next_state
                 
                 index += 1
        return minimax_points, dqn_points
                
            
    def run(self):
            try:
                for index_episode in range(self.episodes):
                    state = self.env.reset()
                    #state = np.reshape(state, [1, self.state_size])
                    done = False
                    index = 0
                    while not done:
                         print('.')
    #                    self.env.render()
                         #action = self.agent.act(state)
                         action = self.minimax.act(box_to_board(state),1,index%2)
                         next_state, reward, done, _ = self.env.step(action)
                         #next_state = np.reshape(next_state, [1, self.state_size])    
                         self.dqnagent.memorize(state, action, reward, next_state, done)
                         state = next_state
                         index += 1
                         #print(index)
                         if index==100:
                             break
                    print("Episode", index_episode, "Number of moves:", index + 1)
                    #self.dqnagent.replay(self.sample_batch_size)
                    
    #             for index_episode in range(self.episodes):
    #                 state = self.env.reset()
    #                 #state = np.reshape(state, [1, self.state_size])
    #                 done = False
    #                 index = 0
    #                 while not done:
    # #                    self.env.render()
    #                      #action = self.agent.act(state)
    #                      action = self.dqnagent.act(state)
    #                      next_state, reward, done, _ = self.env.step(action)
    #                      #next_state = np.reshape(next_state, [1, self.state_size])    
    #                      self.dqnagent.memorize(state, action, reward, next_state, done)
    #                      state = next_state
    #                      index += 1
    #                      #print(index)
    #                      if index==100:
    #                          break
    #                 print(state)
    #                 print("Episode", index_episode, "Number of moves:", index + 1)
    #                 self.dqnagent.replay(self.sample_batch_size)
            finally:
                self.dqnagent.save_model()
                
if __name__ == "__main__":
    test = Test()
    test.run()