
import gym
from gym import spaces
import copy
import numpy as np


def board_to_box(board):
    blue_hor = []
    blue_ver = []
    red_ver = []
    red_hor = []
    masters = []
    state = [red_hor]+[red_ver]+[blue_ver]+[blue_hor]+[masters]
    for row in board:
        for i in state:
            i.append([])
        for p in row:
            for i in state:
                i[-1].append(0)
            if p==0:
                continue
            elif p.player==0:
                if p.direction==0:
                    red_hor[-1][-1] = 1
                else:
                    red_ver[-1][-1] = 1
            else:
                if p.direction==0:
                    blue_hor[-1][-1] = 1
                else:
                    blue_ver[-1][-1] = 1
            if p.master:
                masters[-1][-1] = 1
    return state
                    
                
def box_to_board(box):
    board = []
    for i in range(box[0][0]):
        for j in range(box[0][0]):
            pass







class PivitEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    #metadata = {'render.modes': ['human']}

    def __init__(self, board_size):
        super(PivitEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.active_player=0
        self.board_size = board_size
        self.observation_space = spaces.Box(low=0, high=1, shape=(board_size, board_size, 5), dtype=np.uint8)
        self.action_space = spaces.Box(low=0, high=1, shape=(board_size, board_size, 2), dtype=np.uint8)
        self.reset()
        # Example for using image as input:

    def step(self, action):
        # Execute one time step within the environment
        if self.active_player==0:    
            #prev_score = sum(self.red_ver)+sum(self.red_hor)-sum(self.blue_hor)-sum(self.blue_ver)
            if self.red_hor[action[0][0]][action[0][1]] == 1:
                self.red_hor[action[0][0]][action[0][1]] = 0
                self.red_ver[action[1][0]][action[1][1]] = 1
            if self.red_ver[action[0][0]][action[0][1]] == 1:
                self.red_hor[action[1][0]][action[1][1]] = 1
                self.red_ver[action[0][0]][action[0][1]] = 0
        else:
            if self.blue_hor[action[0][0]][action[0][1]] == 1:
                print('blue')
                self.blue_hor[action[0][0]][action[0][1]] = 0
                self.blue_ver[action[1][0]][action[1][1]] = 1
            if self.blue_ver[action[0][0]][action[0][1]] == 1:
                self.blue_hor[action[1][0]][action[1][1]] = 1
                self.blue_ver[action[0][0]][action[0][1]] = 0
        self.active_player = not self.active_player
    
        
        
    def reset(self):
        # Reset the state of the environment to an initial state
        self.red_hor = [[0 for i in range(self.board_size)]]+[[j%2]+[0 for i in range(self.board_size-2)]+[j%2] for j in range(self.board_size-2)]+[[0 for i in range(self.board_size)]]
        self.red_ver = [[0]+[i%2 for i in range(self.board_size-2)]+[0]]+[[0 for i in range(self.board_size)] for j in range(self.board_size-2)]+[[0]+[i%2 for i in range(self.board_size-2)]+[0]]
        self.blue_hor = [[0 for i in range(self.board_size)]]+[[(j+1)%2]+[0 for i in range(self.board_size-2)]+[(j+1)%2] for j in range(self.board_size-2)]+[[0 for i in range(self.board_size)]]
        self.blue_ver = [[0]+[(i+1)%2 for i in range(self.board_size-2)]+[0]]+[[0 for i in range(self.board_size)] for j in range(self.board_size-2)]+[[0]+[(i+1)%2 for i in range(self.board_size-2)]+[0]]
        self.masters = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        self.state = [self.red_hor]+[self.red_ver]+[self.blue_ver]+[self.blue_hor]+[self.masters]
        return self.observation_space.sample()
    
    def render(self, mode='human', close=False):
        # Render the environment to the screen
        pass