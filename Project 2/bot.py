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

def get_move(first, second):
    """Difference (move) between two boards"""
    orig=0
    dest=0
    try:
        for i in range(len(first)):
            for j in range(len(first[0])):
                if first[i][j] == second[i][j]:
                    continue
                elif first[i][j] == 0:
                    dest = copy.copy((i,j))
                elif second[i][j] == 0:
                    orig = copy.copy((i,j))
                else:
                    dest = copy.copy((i,j))
    except:
        print("ERROR")
        print(first)
        print(second)
    if orig==0:
        print("no moves")
    return [orig,dest]
                


class Piece(object):
    def __init__(self, player = 0, direction=0, master=False):
        self.player = player
        self.direction = direction
        self.master = master
        
    def __repr__(self):
        if self.direction==1:
            d="|"
        elif self.direction==0:
            d="-"
        if self.master:
            m = "M"
        else:
            m=" "
        return " P"+str(self.player)+d+m

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
        if (x2==0 or x2==len(board)-1) and (y2==0 or y2==len(board)-1):
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
    
    def terminal_node(self, board, player):
        red_minion = 0
        blue_minion = 0
        red_master = 0
        blue_master = 0
        only_masters = True
        for row in board:
            for piece in row:
                if piece != 0:
                    if not piece.master:
                        if piece.player:
                            blue_minion += 1
                        else:
                            red_minion += 1
                        only_masters = False
                    else:
                        if piece.player:
                            blue_master += 1
                        else:
                            red_master += 1
        if blue_minion + blue_master == 0:
            self.winner = 0 #vermelho
            return True
        elif red_minion + red_master == 0:
            self.winner = 1 #azul
            return True
        elif only_masters:
            if red_master > blue_master:
                self.winner = 0 #vermelho
            elif blue_master > red_master:
                self.winner = 1 #azul
            else:
                self.winner = 2 #empate
            return True
        return False
        

    def list_cap_moves(self, board, player):
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
                                continue
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
                                continue
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
                                continue
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
                                continue
                            elif board[x+i][y].player != player:
                                if p.master or i%2 == 1:
                                    move = self.move(board,x,y,x+i,y)
                                    cap_moves += [move]
                                break
                            else:
                                break
        random.shuffle(cap_moves)
        return cap_moves

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
        self.initial_time = time()
        if self.terminal_node(board, player):
            if self.winner == player:
                return 10e+5
            elif self.winner == 2:
                return 0
            else:
                return -10e+5
        if depth == 0:
            list_of_moves = self.list_cap_moves(board, player)        
            if len(list_of_moves) == 0:
                return self.evaluate(board, player)
            else:
                depth=1
        else:
            list_of_moves = self.list_moves(board, player)
            if len(list_of_moves) == 0:
                return -10e+5
        for next_board in list_of_moves:
            score = -self.minimax(next_board, depth-1, not player, -beta, -alpha);
            if score >= beta:
                return beta   #  fail hard beta-cutoff
            if score > alpha:
                alpha = score # alpha acts like max in MiniMax
        return alpha
    
    def choose_move(self, board, depth, player=True):
        self.initial_time = time()
        if self.terminal_node(board, player):
            if self.winner == player:
                return None
            elif self.winner == 2:
                print("EMPATE")
                return None
            else:
                return None
        if depth == 0:
            list_of_moves = self.list_cap_moves(board, player)
            if len(list_of_moves) == 0:
                return None
        else:
            list_of_moves = self.list_moves(board, player)
            if len(list_of_moves) == 0:
                return None
        alpha = -10e+5
        beta = 10e+5
        for next_board in list_of_moves:
            score = -self.minimax(next_board, depth-1, not player, -beta, -alpha);
            if score >= beta:
                self.best_move = copy.deepcopy(next_board)
                return self.best_move   #  fail hard beta-cutoff
            if score > alpha:
                alpha = score # alpha acts like max in MiniMax
                self.best_move = copy.deepcopy(next_board)
        return self.best_move
    
    def act(self, board, depth=1, player=0):
        self.choose_move(board, depth, player)
        new_board = self.best_move
        action = get_move(board, new_board)
        if action[0]==0 or action[1]==0:
            return None
        else:
            return action

def print_board(board):
    if board==None:
        return
    for row in board:
        s=''
        for p in row:
            if p == 0:
                s += " ... "
            else:
                s += str(p)
        print(s)


#b = Bot()
#b.open_node()
#best = b.minimax([[0]+[Piece(i%2,1) for i in range(4)]+[0]]+[[Piece(i%2,0)]+[0 for i in range(4)]+[Piece(i%2,0)] for i in range(4)]+[[0]+[Piece(i%2,1) for i in range(4)]+[0]],4,False)
#board = [[0, Piece(1,1),0,0],[0,Piece(0,1),0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
#print("Board:",board)
#best = b.minimax(board,5,True)
#print(best)
#for brd in b.list_moves(board,1):
#    print(brd, b.evaluate(brd,1))
#b.choose_move(board,15,1)
#print("Best move:")
#print_board(b.best_move)
#print("value:",b.choose_move(board,15,1))


