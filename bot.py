# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 10:42:50 2020

@author: Estudio
"""
#import pivit
from queue import PriorityQueue
import copy

from pivit import Piece

class Bot(object):
    def __init__(self):
        self.alpha = -1e+10
        self.beta = 1e+10
        self.queue = PriorityQueue()
        self.player_number = 1
        self.active_player = 0
        
    def choose_move(self, state):
        pass
    
    def move(self, board1, x1, y1, x2, y2):
        board = copy.deepcopy(board1)
        print("       ",x1,y1,x2,y2)
        piece = board[x1][y1]
        board[x2][y2] = piece
        board[x1][y1] = 0
        board[x2][y2].direction = not board[x2][y2].direction
        if (x2==0 or x2==7) and (y2==0 or y2==7):
            board[x2][y2].master = True
        self.active_player = (self.active_player+1)%2
        return board
    
    def minmax(self, state):
        pass
    
    def open_node(self):
        node_to_open = self.queue.get()
        board = node_to_open[1]
        for x in range(len(board)):
            for y in range(len(board[x])):
                p = board[x][y]
                print(p)
                if p != 0 and p.player == self.player_number:
                    print("    ok")
                    if p.direction == 0:
                        print("direction 0")
                        for i in range(1,5):
                            if y+i >= len(board[x]):
                                print("OOOOO")
                                break
                            elif board[x][y+i] == 0:
                                print("move ",self.move(board,x,y,x,y+1))
                                self.queue.put((1,self.move(board,x,y,x,y+i)))
                            elif board[x][y+i].player != self.player_number:
                                print("move ",self.move(board, x,y,x,y+i))
                                self.queue.put((1,self.move(board,x,y,x,y+i)))
                                break
                            else:
                                print("OOOOO1")
                                break
                    else:
                        for i in range(1,5):
                            if x+i >= len(board):
                                print("OOOOO2")
                                break
                            elif board[x+i][y] == 0:
                                print("move ",self.move(board,x,y,x+i,y))
                                self.queue.put((1,self.move(board,x,y,x+i,y)))
                            elif board[x+i][y].player != self.player_number:
                                print("move ",self.move(board,x,y,x+i,y))
                                self.queue.put((1,self.move(board,x,y,x+i,y)))
                            else:
                                print("OOOOO3")
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
        print(state)
        print("Value:",value)
        return value
    
    def value(self, board, depth=2, player=False):
        print(" "*(3-depth)*2+str(depth)+".")
        if depth == 0:
            return self.evaluate(board)
        for x in range(len(board)):
            for y in range(len(board[x])):
                p = board[x][y]
                if p != 0 and p.player == player:
                    player = not player
                    #print("ok")
                    if p.direction == 0:
                        #print("direction 0")
                        for i in range(1,5):
                            if y+i >= len(board[x]):
                                #print("OOOOO")
                                break
                            elif board[x][y+i] == 0:
                                #print("move ", self.move(board,x,y,x,y+i))
                                -self.value(self.move(board,x,y,x,y+i),  depth-1, player)
                            elif board[x][y+i].player != self.player_number:
                                #print("move ",self.move(board, x,y,x,y+i))
                                -self.value(self.move(board,x,y,x,y+i), depth-1, player)
                                break
                            else:
                                #print("OOOOO1")
                                break
                        for i in range(-1,-5,-1):
                            print(i)
                            if y+i < 0:
                                #print("OOOOO")
                                break
                            elif board[x][y+i] == 0:
                                #print("move ", self.move(board,x,y,x,y+i))
                                self.value(self.move(board,x,y,x,y+i), depth-1, player)
                            elif board[x][y+i].player != self.player_number:
                                #print("move ",self.move(board, x,y,x,y+i))
                                self.value(self.move(board,x,y,x,y+i), depth-1, player)
                                break
                            else:
                                #print("OOOOO1")
                                break
                    else:
                        for i in range(1,5):
                            if x+i >= len(board):
                                #print("OOOOO2")
                                break
                            elif board[x+i][y] == 0:
                                #print("move ",self.move(board,x,y,x+i,y))
                                self.value(self.move(board,x,y,x+i,y), depth-1, player)
                            elif board[x+i][y].player != self.player_number:
                                #print("move ",self.move(board,x,y,x+i,y))
                                self.value(self.move(board,x,y,x+i,y), depth-1, player)
                                break
                            else:
                                #print("OOOOO3")
                                break
                        for i in range(-1,-5,-1):
                            print(i)
                            if x+i < 0:
                                #print("OOOOO2")
                                break
                            elif board[x+i][y] == 0:
                                #print("move ",self.move(board,x,y,x+i,y))
                                self.value(self.move(board,x,y,x+i,y), depth-1, player)
                            elif board[x+i][y].player != self.player_number:
                                #print("move ",self.move(board,x,y,x+i,y))
                                self.value(self.move(board,x,y,x+i,y), depth-1, player)
                                break
                            else:
                                #print("OOOOO3")
                                break
        
    


b = Bot()
b.queue.put((1, [[pivit.Piece(1,0,0), 0, pivit.Piece(0,0,0)],[0,0,0],[0,0,0]]))
#b.open_node()
b.value([[0]+[Piece(i%2,1) for i in range(6)]+[0]]+[[Piece(i%2,0)]+[0 for i in range(6)]+[Piece(i%2,0)] for i in range(6)]+[[0]+[Piece(i%2,1) for i in range(6)]+[0]])


