
import gym
from gym import spaces
import copy
import numpy as np
from Game import Piece

def board_to_box(board):
    red_hor = []
    red_ver = []
    blue_hor = []
    blue_ver = []
    masters = []
    state = [red_hor]+[red_ver]+[blue_hor]+[blue_ver]+[masters]
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
    print("ss:",len(state))
    return state
                    
                
def box_to_board(box):
    board = []
    red_hor = box[0]
    red_ver = box[1]
    blue_hor = box[2]
    blue_ver = box[3]
    masters = box[4]
    for i in range(len(box[0][0])):
        board.append([])
        for j in range(len(box[0][0])):
            if red_hor[i][j]==1:
                if masters[i][j]==1:
                    board[-1].append(Piece(0,0,1))
                else:
                    board[-1].append(Piece(0,0,0))
            elif red_ver[i][j]==1:
                if masters[i][j]==1:
                    board[-1].append(Piece(0,1,1))
                else:
                    board[-1].append(Piece(0,1,0))
            elif blue_hor[i][j]==1:
                if masters[i][j]==1:
                    board[-1].append(Piece(1,0,1))
                else:
                    board[-1].append(Piece(1,0,0))
            elif blue_ver[i][j]==1:
                if masters[i][j]==1:
                    board[-1].append(Piece(1,1,1))
                else:
                    board[-1].append(Piece(1,1,0))
            else:
                board[-1].append(0)
    return board
                    
                    
                    
                    
                







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
        if action == None:
            return self.state, -10, True, {}
        # Execute one time step within the environment
        done  = False
        reward = []
        new_state = []
        prev_score = sum([sum(i) for i in self.red_ver])+sum([sum(i) for i in self.red_hor])-sum([sum(i) for i in self.blue_hor])-sum([sum(i) for i in self.blue_ver])
        
        x1=action[0][0]
        y1=action[0][1]
        if (x1==0 or x1==len(self.masters)-1) and (y1==0 or y1==len(self.masters)-1):
            print("MASTER")
            self.masters[x1][y1] = 1
        if self.active_player==0:    
            #move a red piece
            if self.red_hor[action[0][0]][action[0][1]]:
                self.red_hor[action[0][0]][action[0][1]] = 0
                self.red_ver[action[1][0]][action[1][1]] = 1
            elif self.red_ver[action[0][0]][action[0][1]]:
                self.red_hor[action[1][0]][action[1][1]] = 1
                self.red_ver[action[0][0]][action[0][1]] = 0
            #capture a blue piece
            if self.blue_hor[action[1][0]][action[1][1]]:
                self.blue_hor[action[1][0]][action[1][1]] = 0
            elif self.blue_ver[action[1][0]][action[1][1]]:
                self.blue_ver[action[1][0]][action[1][1]] = 0
        else:
            prev_score *= -1
            #move a blue piece
            if self.blue_hor[action[0][0]][action[0][1]]:
                self.blue_hor[action[0][0]][action[0][1]] = 0
                self.blue_ver[action[1][0]][action[1][1]] = 1
            elif self.blue_ver[action[0][0]][action[0][1]]:
                self.blue_hor[action[1][0]][action[1][1]] = 1
                self.blue_ver[action[0][0]][action[0][1]] = 0
            #capture a red piece
            if self.red_hor[action[1][0]][action[1][1]]:
                self.red_hor[action[1][0]][action[1][1]] = 0
            elif self.red_ver[action[1][0]][action[1][1]]:
                self.red_ver[action[1][0]][action[1][1]] = 0
        #move a master
        if self.masters[action[0][0]][action[0][1]]:
            self.masters[action[0][0]][action[0][1]] = 0
            self.masters[action[1][0]][action[1][1]] = 1
        #capture a master
        if self.masters[action[1][0]][action[1][1]]:
            self.masters[action[1][0]][action[1][1]] = 0
        new_score = sum([sum(i) for i in self.red_ver])+sum([sum(i) for i in self.red_hor])-sum([sum(i) for i in self.blue_hor])-sum([sum(i) for i in self.blue_ver])
        if self.active_player==1:
            new_score *= -1
        reward = new_score - prev_score
        new_state = [self.red_hor, self.red_ver, self.blue_hor, self.blue_ver, self.masters]
        
        if sum([sum(i) for i in self.red_ver])+sum([sum(i) for i in self.red_hor]) == 0 \
            or sum([sum(i) for i in self.blue_hor])+sum([sum(i) for i in self.blue_ver]) == 0 \
                or sum([sum(i) for i in self.red_ver])+sum([sum(i) for i in self.red_hor]) \
                    + sum([sum(i) for i in self.blue_hor])+sum([sum(i) for i in self.blue_ver]) == sum([sum(i) for i in self.masters]):
            print("DONE__________________________________________")
            done = True
        
        self.active_player = not self.active_player
        return np.array(new_state), reward, done, {}
        
    
        
        
    def reset(self):
        # Reset the state of the environment to an initial state
        self.red_hor = [[0 for i in range(self.board_size)]]+[[j%2]+[0 for i in range(self.board_size-2)]+[j%2] for j in range(self.board_size-2)]+[[0 for i in range(self.board_size)]]
        self.red_ver = [[0]+[i%2 for i in range(self.board_size-2)]+[0]]+[[0 for i in range(self.board_size)] for j in range(self.board_size-2)]+[[0]+[i%2 for i in range(self.board_size-2)]+[0]]
        self.blue_hor = [[0 for i in range(self.board_size)]]+[[(j+1)%2]+[0 for i in range(self.board_size-2)]+[(j+1)%2] for j in range(self.board_size-2)]+[[0 for i in range(self.board_size)]]
        self.blue_ver = [[0]+[(i+1)%2 for i in range(self.board_size-2)]+[0]]+[[0 for i in range(self.board_size)] for j in range(self.board_size-2)]+[[0]+[(i+1)%2 for i in range(self.board_size-2)]+[0]]
        self.masters = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        self.state = [self.red_hor]+[self.red_ver]+[self.blue_hor]+[self.blue_ver]+[self.masters]
        return self.state
    
    def render(self, mode='human', close=False):
        # Render the environment to the screen
        pass