# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 17:06:51 2020

@author: Estudio
"""
import pygame
from random import *
from time import sleep
from time import time


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
        self.currentLevel = 0
        pygame.init()
        window_width = 840
        window_height = 840
        win = pygame.display.set_mode((window_width, window_height))
        self.window = win
        self.menu()
        self.play()
        pygame.quit()
        
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
        while not (self.game_over() or self.quit):
            self.control()
        
        pygame.quit()
            
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
        """funcao que processar os cliques no tabuleiro do jogo"""
        while not (self.game_over() or self.quit):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.play()
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
                                    self.move(i,j)
                                    self.selected = None
                                print(i,j)
                                self.draw()
                                return

    def move(self, i, j):
        """funcao para validar e executar uma jogada"""
        piece = self.board[self.selected[0]][self.selected[1]]
        if piece == 0:
            return
        elif piece.player != self.active_player:
            print("it's not your turn", piece.player, self.active_player)
            return
        elif self.board[i][j] != 0:
            if piece.player == self.board[i][j].player:
                print("can't capture your own pieces")
                return
        if i==self.selected[0] and piece.direction == 0:
            if piece.master == False:
                if (i + j - sum(self.selected))%2 == 0:
                    print("must choose a different color")
                    return
            if j < self.selected[1]:
                spaces_between = [self.board[i][y] for y in range(j+1, self.selected[1])]
            else:
                spaces_between = [self.board[i][y] for y in range(self.selected[1]+1, j)]
            print(spaces_between)
            for p in spaces_between:
                if p != 0:
                    print("can't jump pieces")
                    return
            piece.direction = 1
            self.board[i][j] = piece
            self.board[self.selected[0]][self.selected[1]] = 0
        elif j==self.selected[1] and piece.direction == 1:
            if piece.master == False:
                if (i + j - sum(self.selected))%2 == 0:
                    print("must choose a different color")
                    return
            if i < self.selected[0]:
                spaces_between = [self.board[x][j] for x in range(i+1, self.selected[0])]
            else:
                spaces_between = [self.board[x][j] for x in range(self.selected[0]+1, i)]  
            print(spaces_between)
            for p in spaces_between:
                if p != 0:
                    print("can't jump pieces")
                    return
            piece.direction = 0
            self.board[i][j] = piece
            self.board[self.selected[0]][self.selected[1]] = 0
        else:
            print("Invalid movement")
            return
        if self.board[i][j] == 0:
            print("Something wrong happened")
            return
        elif (i==0 or i==7) and (j==0 or j==7):
            self.board[i][j].master = True
        self.active_player = (self.active_player+1)%2
        return

    def game_over(self):
        """verificar se o jogo acabou"""
        red = 0
        blue = 0
        for row in self.board:
            for piece in row:
                if piece != 0:
                    if not piece.master:
                        return False
                    else:
                        if piece.player:
                            blue += 1
                        else:
                            red += 1
        print('Game over')
        if red > blue:
            self.winner = "Red"
        elif blue > red:
            self.winner = "Blue"
        else:
            self.winner = "Nobody"
        self.game_over_screen()
        return True







    
Game()