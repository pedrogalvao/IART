
import gym
from gym import spaces
import copy
import numpy as np
from Game import Piece

def board_to_box(board):
    blue_hor = []
    blue_ver = []
    red_ver = []
    red_hor = []
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
    return state
                    
                
def box_to_board(box):
    board = []
    blue_hor = box[2]
    blue_ver = box[3]
    red_ver = box[1]
    red_hor = box[0]
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
                    
                    
                    
    def validMove(action):
           
           board = self.box_to_board((red_hor, red_ver, blue_hor, blue_ver))
           
           board_cpy = copy.deepcopy(board)
           piece = board[action[0][0]][action[0][1]]
           if piece == 0:
               return False
           elif piece.player != self.active_player:
               return False
           elif board[action[1][0]][action[1][1]] != 0:
              if piece.player == board[action[1][0]][action[1][1]].player:
                   return False
           if action[1][0]==action[0][0] and piece.direction == 0:
               if piece.master == False:
                   if ((action[1][0] + action[1][1]) - sum(action[0][0], action[0][1]))%2 == 0:
                       return False
               if action[1][1] < action[0][1]:
                   spaces_between = [board[action[1][0]][y] for y in range(action[1][1]+1, action[0][1])]
               else:
                   spaces_between = [self.board[i][y] for y in range(action[0][1]+1, action[1][1])]
               for p in spaces_between:
                   if p != 0:
                       return False
               piece.direction = 1
               board[action[1][0]][action[1][1]] = piece
               board[action[0][0]][action[0][1]] = 0
           elif action[1][1]==action[0][1] and piece.direction == 1:
               if piece.master == False:
                   if (action[0][1] + action[1][1] - sum(action[0][0], action[0][1]))%2 == 0:
                       return False
               if action[1][0] < action[0][0]:
                   spaces_between = [board[x][action[1][1]] for x in range(action[1][0]+1, action[0][0])]
               else:
                   spaces_between = [board[x][action[1][1]] for x in range(action[0][0]+1, action[1][0])]  
               print(spaces_between)
               for p in spaces_between:
                   if p != 0:
                       return False
               piece.direction = 0
               board[action[1][0]][action[1][1]] = piece
               board[action[0][0]][action[0][1]] = 0
           else:
               return False
           if board[action[1][0]][action[1][1]] == 0:
               return False
           elif (action[1][0]==0 or i==self.board_size-1) and (action[1][1]==0 or j==self.board_size-1):
               board[action[1][0]][action[1][1]].master = True
           return True              
                







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
        done  = False
        reward = []
        new_state = []
        prev_num_minions_red = sum([sum(i) for i in self.red_ver])+sum([sum(i) for i in self.red_hor])
        prev_num_minions_blue = sum([sum(i) for i in self.blue_ver])+sum([sum(i) for i in self.blue_hor])
        
        if validMove(action) == False:
            print("Invalid Move")
            return (self.red_hor, self.red_ver, self.blue_hor, self.blue_ver), 0, False
        
        if self.active_player==0:    
            prev_score = sum([sum(i) for i in self.red_ver])+sum([sum(i) for i in self.red_hor])-sum([sum(i) for i in self.blue_hor])-sum([sum(i) for i in self.blue_ver])
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
         
        num_minions_red = sum([sum(i) for i in self.red_ver])+sum([sum(i) for i in self.red_hor])
        num_minions_blue = sum([sum(i) for i in self.blue_ver])+sum([sum(i) for i in self.blue_hor])
        
        if prev_num_minions_blue < num_minions_blue or prev_num_minions_red < num_minions_red :
            reward = sum([sum(i) for i in self.red_ver])+sum([sum(i) for i in self.red_hor])-sum([sum(i) for i in self.blue_hor])-sum([sum(i) for i in self.blue_ver]) - prev_score
        else:
            reward = -0.5 
            
        
        new_state = (self.red_hor, self.red_ver, self.blue_hor, self.blue_ver)
        
        if sum([sum(i) for i in self.red_ver])+sum([sum(i) for i in self.red_hor]) == 0 or sum([sum(i) for i in self.blue_hor])+sum([sum(i) for i in self.blue_ver]) == 0 or sum([sum(i) for i in self.red_ver])+sum([sum(i) for i in self.red_hor]) + sum([sum(i) for i in self.blue_hor])+sum([sum(i) for i in self.blue_ver]) == 0:
            done = True
        
        self.active_player = not self.active_player
        
        return new_state, reward, done
        
    
        
        
    def reset(self):
        # Reset the state of the environment to an initial state
        self.red_hor = [[0 for i in range(self.board_size)]]+[[j%2]+[0 for i in range(self.board_size-2)]+[j%2] for j in range(self.board_size-2)]+[[0 for i in range(self.board_size)]]
        self.red_ver = [[0]+[i%2 for i in range(self.board_size-2)]+[0]]+[[0 for i in range(self.board_size)] for j in range(self.board_size-2)]+[[0]+[i%2 for i in range(self.board_size-2)]+[0]]
        self.blue_hor = [[0 for i in range(self.board_size)]]+[[(j+1)%2]+[0 for i in range(self.board_size-2)]+[(j+1)%2] for j in range(self.board_size-2)]+[[0 for i in range(self.board_size)]]
        self.blue_ver = [[0]+[(i+1)%2 for i in range(self.board_size-2)]+[0]]+[[0 for i in range(self.board_size)] for j in range(self.board_size-2)]+[[0]+[(i+1)%2 for i in range(self.board_size-2)]+[0]]
        self.masters = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        self.state = [self.red_hor]+[self.red_ver]+[self.blue_hor]+[self.blue_ver]+[self.masters]
        return self.observation_space.sample()
    
    def render(self, mode='human', close=False):
        # Render the environment to the screen
        pass
