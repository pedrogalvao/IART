# -*- coding: utf-8 -*-
"""
Created on Tue May 26 09:07:49 2020

@author: Estudio
"""
import gym
import numpy as np
from DQNAgent import DQNAgent
from PivitEnv import PivitEnv

class Test:
    def __init__(self):
        self.sample_batch_size = 32
        self.episodes          = 10000
        self.env               = PivitEnv(6)

        self.state_size        = 6#self.env.observation_space.shape[0]
        self.action_size       = 6#self.env.action_space.n
        self.agent             = DQNAgent(self.state_size, self.action_size)
            
            
    def run(self):
            try:
                for index_episode in range(self.episodes):
                    state = self.env.reset()
                    #state = np.reshape(state, [1, self.state_size])
                    done = False
                    index = 0
                    while not done:
    #                    self.env.render()
                         action = self.agent.act(state)
                         next_state, reward, done, _ = self.env.step(action)
                         next_state = np.reshape(next_state, [1, self.state_size])
                         self.agent.remember(state, action, reward, next_state, done)
                         state = next_state
                         index += 1
                    print("Episode {}# Score: {}".format(index_episode, index + 1))
                    self.agent.replay(self.sample_batch_size)
            finally:
                pass
                #self.agent.save_model()
                
if __name__ == "__main__":
    test = Test()
    test.run()