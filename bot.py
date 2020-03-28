# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 10:42:50 2020

@author: Estudio
"""
#import pivit
from queue import PriorityQueue
import copy
import random
from time import time

#from pivit import Piece

class Piece(object):
    def __init__(self, player = 0, direction=0, master=False):
        self.player = player
        self.direction = direction
        self.master = master
        
    def __repr__(self):
        if self.master:
            m = " M"
        else:
            m=""
        return "P"+str(self.player)+" "+str(self.direction)+m

class Bot(object):
    def __init__(self):
        self.best_move = None
        self.initial_time = time()
            
    def move(self, board1, x1, y1, x2, y2):
        board = copy.deepcopy(board1)
        piece = board[x1][y1]
        board[x2][y2] = piece
        board[x1][y1] = 0
        board[x2][y2].direction = not board[x2][y2].direction
        if (x2==0 or x2==7) and (y2==0 or y2==7):
            board[x2][y2].master = True
        return board
    
    def evaluate(self, board, player):
        value = 0
        for row in board:
            for piece in row:
                if piece != 0:
                    if player == piece.player:
                        value += 2+piece.master
                    else:
                        value -= 2+piece.master
        return value

    def list_moves(self, board, player):
        moves = []
        cap_moves = []
        for x in range(len(board)):
            for y in range(len(board[x])):
                p = board[x][y]
                if p != 0 and p.player == player:
                    if p.direction == 0:
                        for i in range(1,9):
                            if y+i >= len(board[x]):
                                break
                            elif board[x][y+i] == 0:
                                if p.master or i%2 == 1:
                                    move = self.move(board,x,y,x,y+i)
                                    moves += [move]
                            elif board[x][y+i].player != player:
                                if p.master or i%2 == 1:
                                    move = self.move(board,x,y,x,y+i)
                                    cap_moves += [move]
                                break
                            else:
                                break
                        for i in range(-1,-9,-1):
                            if y+i < 0:
                                break
                            elif board[x][y+i] == 0:
                                if p.master or i%2 == 1:
                                    move = self.move(board,x,y,x,y+i)
                                    moves += [move]
                            elif board[x][y+i].player != player:
                                if p.master or i%2 == 1:
                                    move = self.move(board,x,y,x,y+i)
                                    cap_moves += [move]
                                break
                            else:
                                break
                    else:
                        for i in range(1,9):
                            if x+i >= len(board):
                                break
                            elif board[x+i][y] == 0:
                                if p.master or i%2 == 1:
                                    move = self.move(board,x,y,x+i,y)
                                    moves += [move]
                            elif board[x+i][y].player != player:
                                if p.master or i%2 == 1:
                                    move = self.move(board,x,y,x+i,y)
                                    cap_moves += [move]
                                break
                            else:
                                break
                        for i in range(-1,-9,-1):
                            if x+i < 0:
                                break
                            elif board[x+i][y] == 0:
                                if p.master or i%2 == 1:
                                    move = self.move(board,x,y,x+i,y)
                                    moves += [move]
                            elif board[x+i][y].player != player:
                                if p.master or i%2 == 1:
                                    move = self.move(board,x,y,x+i,y)
                                    cap_moves += [move]
                                break
                            else:
                                break
        random.shuffle(moves)
        random.shuffle(cap_moves)
        return cap_moves + moves
    
    
    def minimax(self, board, depth, player, alpha, beta):
        if depth == 0:
            return self.evaluate(board, player)
        list_of_moves = self.list_moves(board, player)
        if len(list_of_moves) == 0:
            return -10e+5
        if player:
            value = -10e+5
            for next_board in list_of_moves:
                value = max(value, self.minimax(next_board, depth-1, not player, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
                if time() - self.initial_time > 0.5:
                    break
            return value
        else:
            value = 10e+5
            for next_board in list_of_moves:
                value = min(value, self.minimax(next_board, depth-1, not player, alpha, beta))
                beta = min(beta, value)
                if alpha >= beta:
                    break
                if time() - self.initial_time > 0.5:
                    break
            return value
    
    def choose_move(self, board, depth=2, player=True):
        self.initial_time = time()
        if depth == 0:
            return self.evaluate( board, player)
        alpha = -10e+5
        beta = 10e+5
        list_of_moves = self.list_moves(board, player)
        if len(list_of_moves) == 0:
            return -10e+5
        if player:
            value = -10e+5
            for next_board in list_of_moves:
                value = max(value, self.minimax(next_board, depth-1, not player, alpha, beta))
                if alpha < value:
                    alpha = value
                    self.best_move = next_board
                if alpha >= beta:
                    break
                if time() - self.initial_time > 0.5:
                    break
            return value
        else:
            value = 10e+5
            for next_board in list_of_moves:
                value = min(value, self.minimax(next_board, depth-1, not player, alpha, beta))
                if beta > value:
                    beta = value
                    self.best_move = next_board
                if alpha >= beta:
                    break
                if time() - self.initial_time > 0.5:
                    break
            return value
    


b = Bot()
#b.open_node()
#best = b.minimax([[0]+[Piece(i%2,1) for i in range(4)]+[0]]+[[Piece(i%2,0)]+[0 for i in range(4)]+[Piece(i%2,0)] for i in range(4)]+[[0]+[Piece(i%2,1) for i in range(4)]+[0]],4,False)
board = [[0, Piece(1,1),0,0],[0,Piece(0,1),0,0],[0,0,0,0],[0,0,0,0]]
print(board)
#best = b.minimax(board,5,True)
#print(best)
for brd in b.list_moves(board,0):
    print(brd)
#def print_board(board):
#    for ro in board:
#        for p in row:
#            if p == 0:
#                s += " "
#            elif p.player 


