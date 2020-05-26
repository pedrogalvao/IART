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
import numpy as np

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
        self.times = []
        self.number_of_games = 0
        self.red_victories = 0
        self.blue_victories = 0
        pygame.init()
        self.quit = False
        window_width = 840
        window_height = 840
        win = pygame.display.set_mode((window_width, window_height))
        self.window = win
        self.bot = Bot()
        self.game_mode = self.menu()
        #self.game_mode = 'HxC'
        self.board_size = self.size_menu()
        self.play()
        print("Tempo medio:",np.mean(self.times))
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
        if self.quit:
            return
        game_type= self.game_mode[0]
        difficulty= self.game_mode[1]
        ini = time()
        self.board = [[0]+[Piece(i%2,1) for i in range(self.board_size-2)]+[0]]+[[Piece(i%2,0)]+[0 for i in range(self.board_size-2)]+[Piece(i%2,0)] for i in range(self.board_size-2)]+[[0]+[Piece(i%2,1) for i in range(self.board_size-2)]+[0]]
        self.buttons = [[i for i in range(self.board_size)] for j in range(self.board_size)]
        self.selected = None
        self.active_player = 0
        self.quit = False
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.buttons[i][j] = pygame.draw.rect(self.window, ((i+j)%2*255, (i+j)%2*255, (i+j)%2*255), (20+j*100, 20+i*100, 100, 100))
        self.draw()
        if game_type==1:
            self.play_pvp()
        elif game_type==2:
            self.play_pvc(difficulty)
        elif game_type==3:
            difficulty2 = self.game_mode[2]
            self.play_cvc(difficulty, difficulty2)


    def play_pvp(self):
        while not (self.game_over() or self.quit):
            self.control()
        #pygame.quit()

    def play_pvc(self, difficulty):
        self.bot_move(difficulty, False)
        while not (self.game_over() or self.quit):
            if self.control():
                if self.game_over() or self.quit:
                    break
                self.bot_move(difficulty, False)
        #pygame.quit()
        
    def play_cvc(self, difficulty, difficulty2):
        i=0
        while not (self.game_over() or self.quit):
            self.bot_move(difficulty, i%2)
            i+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.play()
                    elif event.key == pygame.K_t:
                        self.tip()
                    elif event.key == pygame.K_m:
                        self.__init__()
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
                elif event.type == pygame.KEYDOWN:
                    if evenvt.key == pygame.K_r:
                        self.play()
                    elif event.key == pygame.K_t:
                        self.tip()
                    elif event.key == pygame.K_m:
                        self.__init__()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for i in range(len(self.menu_buttons)):
                            if self.menu_buttons[i].collidepoint(pos):
                                y_pos=pos[1]
                                difficulty=0
                                if y_pos<=300 and y_pos>=200:
                                    return [1,difficulty]
                                elif y_pos<=420 and y_pos>=320:
                                    difficulty=self.difficulty_menu("Computer difficulty:")
                                    return [2,difficulty]
                                elif y_pos<=540 and y_pos>=420:
                                    difficulty_bot1=self.difficulty_menu("Computer 1 difficulty:")
                                    difficulty_bot2=self.difficulty_menu("Computer 2 difficulty:")
                                    return [3,difficulty_bot1, difficulty_bot2]
                                
   
    def difficulty_menu(self, title):
        if self.quit:
            return
        self.font = pygame.font.SysFont("comicsansms", 72)
        i = 0
        self.window.fill((60,50,20))
        self.menu_buttons = [0,0,0,0,0]
        for i in range(5):
            self.menu_buttons[i] = pygame.draw.rect(self.window, (255, 255, 255), (250, 200+i*120, 400, 100))  
        
        text = self.font.render(title, True, (0, 128, 0))
        self.window.blit(text, (30, 100))
        text = self.font.render("Very Easy", True, (0, 200, 0))
        self.window.blit(text, (290, 200))
        text = self.font.render("Easy", True, (100, 200, 0))
        self.window.blit(text, (330, 320))
        text = self.font.render("Normal", True, (200, 200, 0))
        self.window.blit(text, (330, 440))
        text = self.font.render("Hard", True, (255, 100, 0))
        self.window.blit(text, (330, 560))
        text = self.font.render("Very Hard", True, (255, 0, 0))
        self.window.blit(text, (290, 680))
        pygame.display.flip()
        while not self.quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.play()
                    elif event.key == pygame.K_t:
                        self.tip()
                    elif event.key == pygame.K_m:
                        self.__init__()
        
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for i in range(len(self.menu_buttons)):
                            if self.menu_buttons[i].collidepoint(pos):
                                y_pos=pos[1]
                                if y_pos<=300 and y_pos>=200:
                                    return 1
                                elif y_pos<=420 and y_pos>=320:
                                    return 2
                                elif y_pos<=540 and y_pos>=420:
                                    return 3
                                elif y_pos<=660 and y_pos>=540:
                                    return 4
                                elif y_pos<=780 and y_pos>=660:
                                    return 5

    def size_menu(self):
        if self.quit:
            return
        self.font = pygame.font.SysFont("comicsansms", 72)
        i = 0
        self.window.fill((60,50,20))
        self.menu_buttons = [0,0,0,0]
        for i in range(2):
            self.menu_buttons[i] = pygame.draw.rect(self.window, (255, 255, 255), (270, 200+i*120, 300, 100))  
        
        text = self.font.render("Board size", True, (0, 128, 0))
        self.window.blit(text, (30, 100))
        text = self.font.render("6x6", True, (0, 128, 0))
        self.window.blit(text, (330, 200))
        text = self.font.render("8x8", True, (0, 128, 0))
        self.window.blit(text, (330, 320))
        pygame.display.flip()
        while not self.quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.play()
                    elif event.key == pygame.K_t:
                        self.tip()
                    elif event.key == pygame.K_m:
                        self.__init__()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for i in range(len(self.menu_buttons)):
                            if self.menu_buttons[i].collidepoint(pos):
                                y_pos=pos[1]
                                if y_pos<=300 and y_pos>=200:
                                    return 6
                                elif y_pos<=420 and y_pos>=320:
                                    return 8


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
        while not self.quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                    return
                if event.type == pygame.QUIT:
                    self.quit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.play()
                    elif event.key == pygame.K_t:
                        self.tip()
                    elif event.key == pygame.K_m:
                        self.__init__()
        
        
    def control(self):
        """funcao que processa os cliques no tabuleiro do jogo"""
        while not (self.game_over() or self.quit):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.play()
                    elif event.key == pygame.K_m:
                        self.__init__()
                    elif event.key == pygame.K_LEFT and len(self.sequence)>=2:
                        self.sequence.pop()
                        self.board = self.sequence.pop()
                        self.draw()
                    elif event.key == pygame.K_1:
                        self.tip(1)
                    elif event.key == pygame.K_2:
                        self.tip(2)
                    elif event.key == pygame.K_3:
                        self.tip(3)
                    elif event.key == pygame.K_4:
                        self.tip(4)
                    elif event.key == pygame.K_5:
                        self.tip(5)
                        
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
        elif (i==0 or i==self.board_size-1) and (j==0 or j==self.board_size-1):
            self.board[i][j].master = True
        self.active_player = (self.active_player+1)%2
        self.sequence += [board_cpy]
        return True

    def bot_move(self, depth, player=True):        
        self.sequence += [copy.deepcopy(self.board)]
        ini = time()
        print("Value:", self.bot.choose_move(self.board, depth, player))
        print("time to move:", time() - ini)
        self.times += [time()-ini]
        self.board = self.bot.best_move
        self.active_player = (self.active_player+1)%2
        sleep(0.5)
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
            self.red_victories += 1
            self.number_of_games +=1
            self.game_over_screen()
            return True
        elif red_minion + red_master == 0:
            self.winner = "Blue"
            self.blue_victories += 1
            self.number_of_games +=1
            self.game_over_screen()
            return True
        elif only_masters:
            if red_master > blue_master:
                self.winner = "Red"
                self.red_victories += 1
            elif blue_master > red_master:
                self.winner = "Blue"
                self.blue_victories += 1
            else:
                self.winner = "Nobody"
            self.number_of_games +=1
            self.game_over_screen()
            return True
        
        return False
    
    def tip(self, level):
        board = copy.deepcopy(self.board)
        self.bot.choose_move(self.board, level, self.active_player)
        self.board = self.bot.best_move
        print("best move:", self.board)
        self.draw()
        pygame.event.get()
        sleep(1)
        self.board = board
        self.draw()
        return



    
G = Game()

if G.number_of_games > 0:
    print("Tempo medio:", np.mean(G.times))
    print("Desvio padrao:", np.std(G.times))
    print("Numero de jogadas contadas:", len(G.times))
    print("Numero de jogadas por partida:", len(G.times)/G.number_of_games)
    print("Numero de partidas:", G.number_of_games)
    print("Vermelho:", G.red_victories)
    print("Azul:", G.blue_victories)
    print("Empates:", G.number_of_games-G.red_victories-G.blue_victories)

