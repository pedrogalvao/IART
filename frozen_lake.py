# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:26:51 2020

@author: Estudio
"""


import numpy as np
import gym
import random
from gym.envs.registration import register
try:
    register(
         id='a2-v0',
         entry_point='gym.envs.toy_text:FrozenLeakeEnv',
         kwargs={'map_name' : '4x4', 'is_slippery': True},
         max_episode_steps=100,
         reward_threshold=0.8196, # optimum = .8196, changing this seems have no influence
     )
except:
    pass
env = gym.make("a2-v0")
action_size = env.action_space.n
state_size = env.observation_space.n
print(f'aciton size: {action_size}, state size: {state_size}')
state = env.observation_space
qtable = np.zeros((state_size, action_size))
print(qtable)

# @hyperparameters
total_episodes = 500        # Total episodes
learning_rate = 0.8           # Learning rate
max_steps = 99                # Max steps per episode
gamma = 0.95                  # Discounting rate

# Exploration parameters
epsilon = 1.0                 # Exploration rate
max_epsilon = 1.0             # Exploration probability at start
min_epsilon = 0.00001            # Minimum exploration probability 
decay_rate = 0.001             # Exponential decay rate for exploration prob
#I find that decay_rate=0.001 works much better than 0.01

# List of rewards
rewards = []

# 2 For life or until learning is stopped
for episode in range(total_episodes):
    # Reset the environment
    state = env.reset()
#     print(f"state: {state}")
    step = 0
    done = False
    total_rewards = 0
    
    for step in range(max_steps):
#         print(f"start step...")
        # 3. Choose an action a in the current world state (s)
        ## First we randomize a number
        exp_exp_tradeoff = random.uniform(0, 1)
        
#         print(f"exp_exp_tradeoff: {exp_exp_tradeoff}")
        
        ## If this number > greater than epsilon --> exploitation 
        #(taking the biggest Q value for this state)
        if exp_exp_tradeoff > epsilon:
            #print("exploitation")
#             print(f"qtable[state,:] {qtable[state,:]}")
            action = np.argmax(qtable[state,:])

        # Else doing a random choice --> exploration
        else:
            #print("exploration")
            action = env.action_space.sample()
            
#         print(f"action is {action}")

        # Take the action (a) and observe the outcome state(s') and reward (r)
        new_state, reward, done, info = env.step(action)
        
        #print(f"new_state: {new_state}, reward: {reward}, done: {done}, info: {info}")

        # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
        # qtable[new_state,:] : all the actions we can take from new state
        qtable[state, action] = qtable[state, action] + learning_rate * (reward + gamma * np.max(qtable[new_state, :]) - qtable[state, action])
        
#         print(f'qtable: {qtable}')
        
        total_rewards = total_rewards + reward
        
#         print(f'total_rewards {total_rewards}')
        
        # Our new state is state
        state = new_state
        
#         print(f'new state: {state}')
        
        # If done (if we're dead) : finish episode
        if done == True: 
            break
        
    episode += 1
    # Reduce epsilon (because we need less and less exploration)
    epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode) 
    rewards.append(total_rewards)

print ("Score over time: " +  str(sum(rewards)/total_episodes))
print(qtable)
print(epsilon)

# Print the action in every place
#LEFT = 0 DOWN = 1 RIGHT = 2 UP = 3

env.reset()
env.render()
print(np.argmax(qtable,axis=1).reshape(4,4))

#All the episoded is the same
# taking the maximum of Qtable value every time.
env.reset()

for episode in range(1):
    state = env.reset()
    step = 0
    done = False
    print("****************************************************")
    print("EPISODE ", episode)

    for step in range(max_steps):
       # env.render()
        # Take the action (index) that have the maximum expected future reward given that state
        action = np.argmax(qtable[state,:])
        
        new_state, reward, done, info = env.step(action)
        
        if done:
            break
        state = new_state
env.close()