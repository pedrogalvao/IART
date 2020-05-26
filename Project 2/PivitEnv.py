
import gym
from gym import spaces
import copy
import numpy as np

class PivitEnv(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self, board_size):
    super(PivitEnv, self).__init__()
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions:
    self.board_size = board_size
    self.observation_space = spaces.Box(low=0, high=1, shape=(board_size, board_size, 5), dtype=np.uint8)
    self.reset()
    basic_space = spaces.Tuple([spaces.MultiBinary(board_size) for i in range(board_size)])
    self.action_space = spaces.Tuple([copy.deepcopy(basic_space) for i in range(board_size)])
    # Example for using image as input:

  def step(self, action):
    # Execute one time step within the environment
   pass
    #for subspace in self.state:
     #   subspace[action[0][0]][action[0][1]] = 0
    
    
  def reset(self):
    # Reset the state of the environment to an initial state
    self.red_hor = [[0 for i in range(self.board_size)]]+[[j%2]+[0 for i in range(self.board_size-2)]+[j%2] for j in range(self.board_size-2)]+[[0 for i in range(self.board_size)]]
    self.red_ver = [[0]+[i%2 for i in range(self.board_size)]+[0]]+[[0 for i in range(self.board_size)] for j in range(self.board_size-2)]+[[0]+[i%2 for i in range(self.board_size)]+[0]]
    self.blue_hor = [[0 for i in range(self.board_size)]]+[[(j+1)%2]+[0 for i in range(self.board_size-2)]+[(j+1)%2] for j in range(self.board_size-2)]+[[0 for i in range(self.board_size)]]
    self.blue_ver = [[0]+[(i+1)%2 for i in range(self.board_size)]+[0]]+[[0 for i in range(self.board_size)] for j in range(self.board_size-2)]+[[0]+[(i+1)%2 for i in range(self.board_size)]+[0]]
    self.masters = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
    self.state = [self.red_hor]+[self.red_ver]+[self.blue_ver]+[self.blue_hor]+[self.masters]
    return self.observation_space.sample()
    
  def render(self, mode='human', close=False):
    # Render the environment to the screen
    pass