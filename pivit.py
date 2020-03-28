# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 17:06:51 2020

@author: Estudio
"""
import pygame
from random import *
from time import sleep
from time import time
from bot import Bot
import copy

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
        
        



class Game(object):
    def __init__(self):
        self.sequence = []
        pygame.init()
        window_width = 840
        window_height = 840
        win = pygame.display.set_mode((window_width, window_height))
        self.window = win
        self.bot = Bot()
        self.menu()
        self.game_mode = 'HxC'
        self.play()
        pygame.quit()
    
    def test(self):
        count = {'Red':0,'Blue':0,'Nobody':0}
        for i in range(10):
            ini = time()
            self.board = [[0]+[Piece(i%2,1) for i in range(6)]+[0]]+[[Piece(i%2,0)]+[0 for i in range(6)]+[Piece(i%2,0)] for i in range(6)]+[[0]+[Piece(i%2,1) for i in range(6)]+[0]]
            self.buttons = [[i for i in range(8)] for j in range(8)]
            self.selected = None
            self.active_player = 0
            self.quit = False
            self.play_cvc()
            print(self.winner)
            count[self.winner] += 1


    def play(self):
        """funcao que inicia o jogo"""
        ini = time()
        self.board = [[0]+[Piece(i%2,1) for i in range(6)]+[0]]+[[Piece(i%2,0)]+[0 for i in range(6)]+[Piece(i%2,0)] for i in range(6)]+[[0]+[Piece(i%2,1) for i in range(6)]+[0]]
        self.buttons = [[i for i in range(8)] for j in range(8)]
        self.selected = None
        self.active_player = 0
        self.quit = False
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.buttons[i][j] = pygame.draw.rect(self.window, ((i+j)%2*255, (i+j)%2*255, (i+j)%2*255), (20+j*100, 20+i*100, 100, 100))
        self.draw()
        self.play_pvc()

    def play_pvp(self):
        while not (self.game_over() or self.quit):
            self.control()
        #pygame.quit()

    def play_pvc(self):
        self.bot_move(False,4)
        while not (self.game_over() or self.quit):
            if self.control():
                if self.game_over() or self.quit:
                    break
                self.bot_move(False,4)
        #pygame.quit()
        
    def play_cvc(self):
        while not (self.game_over() or self.quit):
            self.bot_move(False,2)
            if self.game_over() or self.quit:
                break
            self.bot_move(True,3)
        #pygame.quit()
                
    def draw(self):
        """funcao que desenha o tabuleiro jogo"""
        i = 0
        self.window.fill((60,50,20))
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pygame.draw.rect(self.window, ((i+j)%2*255, (i+j)%2*255, (i+j)%2*255), (20+j*100, 20+i*100, 100, 100))
                if self.board[i][j] != 0:
                    if self.board[i][j].player == 0:
                        color = (200, 0, 0)
                    else:
                        color = (0, 0, 200)
                    if self.board[i][j].direction == 0:
                        pygame.draw.ellipse(self.window, color, (30+j*100, 40+i*100, 80, 60))
                    elif self.board[i][j].direction == 1:
                        pygame.draw.ellipse(self.window, color, (40+j*100, 30+i*100, 60, 80))
                    if self.board[i][j].master:
                        if self.board[i][j].direction == 0:
                            pygame.draw.ellipse(self.window, (255,255,0), (40+j*100, 50+i*100, 60, 40))
                            pygame.draw.ellipse(self.window, color, (45+j*100, 55+i*100, 50, 30))
                        elif self.board[i][j].direction == 1:
                            pygame.draw.ellipse(self.window, (255,255,0), (50+j*100, 40+i*100, 40, 60))
                            pygame.draw.ellipse(self.window, color, (55+j*100, 45+i*100, 30, 50))
                        
        if self.selected != None:
            pygame.draw.rect(self.window, (200, 200, 0), (20+self.selected[1]*100, 20+self.selected[0]*100, 100, 100), 5)
        pygame.display.flip()
    
    def menu(self):
        """funcao que desenha o menu e espera ate utilizador escolher uma opcao"""
        self.font = pygame.font.SysFont("comicsansms", 72)
        i = 0
        self.window.fill((60,50,20))
        self.menu_buttons = [0,0,0]
        for i in range(3):
            self.menu_buttons[i] = pygame.draw.rect(self.window, (255, 255, 255), (270, 200+i*120, 300, 100))            
        text = self.font.render("H x H", True, (0, 128, 0))
        self.window.blit(text, (330, 200))
        text = self.font.render("H x C", True, (0, 128, 0))
        self.window.blit(text, (330, 320))
        text = self.font.render("C x C", True, (0, 128, 0))
        self.window.blit(text, (330, 440))
        pygame.display.flip()
        while True:      
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for i in range(len(self.menu_buttons)):
                            if self.menu_buttons[i].collidepoint(pos):
                                return

    def game_over_screen(self):
        """funcao que desenha a tela de fim de jogo"""
        self.font = pygame.font.SysFont("comicsansms", 72)
        i = 0
        pygame.draw.rect(self.window, (60,50,20), (200, 200, 450, 300))
        text = self.font.render("Game Over", True, (0, 0, 0))
        self.window.blit(text, (240, 220))
        text = self.font.render(self.winner+" wins", True, (0, 0, 0))
        self.window.blit(text, (270, 330))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.play()
        
        
    def control(self):
        """funcao que processa os cliques no tabuleiro do jogo"""
        while not (self.game_over() or self.quit):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.play()
                    elif event.key == pygame.K_LEFT and len(self.sequence)>=2:
                        self.sequence.pop()
                        self.board = self.sequence.pop()
                        self.draw()
                        
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    ## if mouse is pressed get position of cursor ##
                    pos = pygame.mouse.get_pos()
                    ## check if cursor is on button ##
                    for i in range(len(self.buttons)):
                        for j in range(len(self.buttons[i])):
                            if self.buttons[i][j].collidepoint(pos):
                                if self.selected == None:
                                    self.selected = [i,j]
                                elif self.selected == [i,j]:
                                    self.selected = None
                                elif self.board[self.selected[0]][self.selected[1]]==0:
                                    self.selected = [i,j]
                                else:
                                    if self.move(i,j):
                                        self.selected = None
                                        self.draw()
                                        return True
                                    else:
                                        self.selected = None
                                        self.draw()
                                        return False
                                        
                                self.draw()
                                return False

    def move(self, i, j):
        """funcao para validar e executar uma jogada"""
        board_cpy = copy.deepcopy(self.board)
        piece = self.board[self.selected[0]][self.selected[1]]
        if piece == 0:
            return False
        elif piece.player != self.active_player:
            print("it's not your turn", piece.player, self.active_player)
            return False
        elif self.board[i][j] != 0:
            if piece.player == self.board[i][j].player:
                print("can't capture your own pieces")
                return False
        if i==self.selected[0] and piece.direction == 0:
            if piece.master == False:
                if (i + j - sum(self.selected))%2 == 0:
                    print("must choose a different color")
                    return False
            if j < self.selected[1]:
                spaces_between = [self.board[i][y] for y in range(j+1, self.selected[1])]
            else:
                spaces_between = [self.board[i][y] for y in range(self.selected[1]+1, j)]
            print(spaces_between)
            for p in spaces_between:
                if p != 0:
                    print("can't jump pieces")
                    return False
            piece.direction = 1
            self.board[i][j] = piece
            self.board[self.selected[0]][self.selected[1]] = 0
        elif j==self.selected[1] and piece.direction == 1:
            if piece.master == False:
                if (i + j - sum(self.selected))%2 == 0:
                    print("must choose a different color")
                    return False
            if i < self.selected[0]:
                spaces_between = [self.board[x][j] for x in range(i+1, self.selected[0])]
            else:
                spaces_between = [self.board[x][j] for x in range(self.selected[0]+1, i)]  
            print(spaces_between)
            for p in spaces_between:
                if p != 0:
                    print("can't jump pieces")
                    return False
            piece.direction = 0
            self.board[i][j] = piece
            self.board[self.selected[0]][self.selected[1]] = 0
        else:
            print("Invalid movement")
            return False
        if self.board[i][j] == 0:
            print("Something wrong happened")
            return False
        elif (i==0 or i==7) and (j==0 or j==7):
            self.board[i][j].master = True
        self.active_player = (self.active_player+1)%2
        self.sequence += [board_cpy]
        return True

    def bot_move(self, player=True, depth=3):        
        self.sequence += [copy.deepcopy(self.board)]
        ini = time()
        print("Value:", self.bot.choose_move(self.board, 3, player))
        print("time to move:", ini - time())
        self.board = self.bot.best_move
        self.active_player = (self.active_player+1)%2
        sleep(0.1)
        self.draw()
        return

    def game_over(self):
        """verificar se o jogo acabou"""
        red_minion = 0
        blue_minion = 0
        red_master = 0
        blue_master = 0
        only_masters = True
        for row in self.board:
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
            self.winner = "Red"
            self.game_over_screen()
            return True
        elif red_minion + red_master == 0:
            self.winner = "Blue"
            self.game_over_screen()
            return True
        elif only_masters:
            if red_master > blue_master:
                self.winner = "Red"
            elif blue_master > red_master:
                self.winner = "Blue"
            else:
                self.winner = "Nobody"
            self.game_over_screen()
            return True
        return False







    
Game()