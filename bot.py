# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 10:42:50 2020

@author: Estudio
"""
#import pivit
from queue import PriorityQueue

class Bot(object):
    def __init__(self):
        self.alpha = -1e+10
        self.beta = 1e+10
        self.queue = PriorityQueue() #usar priority queue
        self.player_number = 1
        
    def choose_move(self, state):
        pass
    
    def open_node(self):
        node_to_open = self.queue.get()
        board = node_to_open[1]
        for x in range(len(board)):
            for y in range(len(board[x])):
                p = board[x][y]
                if p != 0 and p.player == self.player_number:
                    if p.direction == 0:
                        for i in range(1,8):
                            if x+i >= len(board):
                                break
                            elif board[x+i][y] == 0:
                                return (x+i,y)
                            elif board[x+i][y].player != self.player_number:
                                self.queue.put((x+i,y))
                            else:
                                break
            

    def evaluate(self, state):
        value = 0
        for row in state:
            for piece in row:
                if piece != 0:
                    if self.player_number == piece.player:
                        value += 1+piece.master
                    else:
                        value -= 1+piece.master
        return value