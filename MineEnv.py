import random
import numpy as np
import pandas as pd
import pygame
import os
from pygame import *
from pprint import pprint
import pygame, sys
from pygame import *
import time
import random
class MinesweeperEnv(object):
    def __init__(self, cellmax=16, bombnumber=40,
        # based on https://github.com/jakejhansen/minesweeper_solver
        rewards={'win':1, 'lose':-1, 'progress':0.3, 'guess':-0.3, 'no_progress' : -0.3}):
        self.cellmax=cellmax
        self.bombnumber = bombnumber
        self.grid = self.init_grid()

        # self.board = self.get_board()
        self.state= self.init_state()
        self.n_clicks = 0
        self.n_progress = 0
        self.n_wins = 0
        self.listtoadd=[]
        self.rewards = rewards
        ####Visualization things
        self.width = 36*cellmax
        self.height = 36*cellmax
        self.FPS = 30
        self.initialadd=100
        self.screen = pygame.display.set_mode((self.width, self.height+self.initialadd),0,32)
        self.cellimg = pygame.image.load('cell.png')
        self.emptycell2 = pygame.image.load('emptycell2.png')
        self.bombimg = pygame.image.load("bomb.png")
        self.markedimg = pygame.image.load("marked.png")
        self.game_opening(self.width,self.height,self.screen,self.initialadd)
        self.font = pygame.font.Font('mine-sweeper.ttf', 18)
    def game_opening(self,width,height,screen,initialadd):
        # screen.blit()
        gray = (198, 198, 198)
        darkgray=(128,128,128)
        white=(255,255,255)
        pygame.display.update()
        # time.sleep(1)
        screen.fill(gray)
        self.visualize_state()
        pygame.display.update()
    def init_grid(self):

        machinegrid=[]
        for i in range(self.cellmax):
            bb=[]
            for j in range(self.cellmax):
                bb.append(0)
            machinegrid.append(bb)

        randbomb= [(i,j) for i in range(self.cellmax) for j in range(self.cellmax)]
        random.seed(5)
        randbomb= random.sample(randbomb,self.bombnumber)
        for i in randbomb:

            machinegrid[i[1]][i[0]]=-1

        for y,bs in enumerate(machinegrid):
            for x,value in enumerate(bs):
                if(value==0):
                    alllist=[]
                    toplist=[(i,y-1) for i in range(x-1,x+2) if i>=0 and i<=self.cellmax-1 and y-1>=0]
                    bottomlist=[(i,y+1) for i in range(x-1,x+2) if i>=0 and i<=self.cellmax-1 and y+1<self.cellmax-1]
                    middlelist=[(i,y) for i in range(x-1,x+2,2) if i>=0 and i<=self.cellmax-1]
                    alllist.extend(toplist)
                    alllist.extend(bottomlist)
                    alllist.extend(middlelist)
                    number=len([i for i in alllist if(machinegrid[i[1]][i[0]]==-1)])
                    machinegrid[y][x]=number
        return machinegrid

    def writenumber(self,screen,cellnumber,number):
        color1 = (0, 0, 255)
        blue = (0, 0, 128)
        

        # create a text surface object,
        # on which text is drawn on it.
        text = self.font.render(str(number), True,colors[number-1])  
        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()
        decay=18
        textRect.center = (cellnumber[0]*36+decay+2,cellnumber[1]*36+self.initialadd+decay)
        screen.blit(text, textRect)
        pygame.display.update()
    def visualize_state(self):
        for idxy,bs in enumerate(self.state):
            for idxx,x in enumerate(bs):
                if(x[0]==9):
                    self.screen.blit(self.cellimg, (idxx*36,idxy*36+self.initialadd))
                elif(x[0]==10):
                    self.screen.blit(self.markedimg, (idxx*36,idxy*36+self.initialadd))
                elif(x[0]==0):
                    self.screen.blit(self.emptycell2, (idxx*36,idxy*36+self.initialadd))
                else:
                    self.screen.blit(self.emptycell2,(idxx*36,idxy*36+self.initialadd))
                    self.writenumber(self.screen,(idxx,idxy),x[0])
        pygame.display.update()




    def init_state(self):
        state=[]
        for i in range(self.cellmax):
            bb=[]
            for j in range(self.cellmax):
                bb.append([9])
            state.append(bb)

        # state_im = self.get_state_im(state)

        return np.array(state)


    #     return f'color: {color}'

    def draw_state(self):
        grid=self.grid
        for idx,i in enumerate(self.state):
            print(str(np.reshape(i,-1))+"          "+str(grid[idx]))
           


    def reset(self):
        self.n_clicks = 0
        self.n_progress = 0
        self.grid = self.init_grid()
        # self.board = self.get_board()
        self.state = self.init_state()


    def winingcon(self):
        # state=self.state
        numnine=0
        for i in self.state:
            for j in i:
                if(j[0]==9):
                    numnine+=1
        if(numnine==self.bombnumber):
            return True
        return False

    def __eq__(self, otherstate):
        return  self.state == otherstate

    def emptyroll(self,action):
        if(action in self.listtoadd):
            return 0
        self.listtoadd.append(action)

        # print("in")
        if(self.grid[action[1]][action[0]]==-1):
            return 0
        elif(self.grid[action[1]][action[0]]!=0):

            # screen.blit(emptycell2,(cellnumber[0]*36,cellnumber[1]*36+initialadd))
            # pygame.display.update()
            # writenumber(screen,cellnumber,machinelist[index],initialadd)
            self.state[action[1]][action[0]][0]=self.grid[action[1]][action[0]]
            return 0
        else:
            self.state[action[1]][action[0]][0]=0
            ####Top Check
            if(action[1]-1>=0):
                self.emptyroll((action[0],action[1]-1))
            ####Bottom Check
            if(action[1]+1<self.cellmax):
                self.emptyroll((action[0],action[1]+1))
            #####Left Check
            if(action[0]-1>=0):
                self.emptyroll((action[0]-1,action[1]))
            #####Right Check
            if(action[0]+1<self.cellmax):
                self.emptyroll((action[0]+1,action[1]))
            return 0

    def neighborsnotrevealed(self,action):
        revealed=False
        alllist=[]
        x=action[0]
        y=action[1]
        toplist=[(i,y-1) for i in range(x-1,x+2) if i>=0 and i<=self.cellmax-1 and y-1>=0]
        bottomlist=[(i,y+1) for i in range(x-1,x+2) if i>=0 and i<=self.cellmax-1 and y+1<self.cellmax-1]
        middlelist=[(i,y) for i in range(x-1,x+2,2) if i>=0 and i<=self.cellmax-1]
        alllist.extend(toplist)
        alllist.extend(bottomlist)
        alllist.extend(middlelist)

        if(any([True for i in alllist if self.state[i[1]][i[0]]!=9])): revealed=True
        return revealed
    def mark(self, action):
        self.state[action]=10
    def step(self, action):
        state=self.state
        grid=self.grid
        statoti=0
        game_over=False
        # print(action)
        # print(grid[action[1]][action[0]])
        if(grid[action[1]][action[0]]==-1):
            reward=self.rewards['lose']
            game_over=True
            # grid[action[1]][action[0]]=-1
            # new_grid=grid
            statoti=0
        elif(self.winingcon()):
            reward = self.rewards['win']
            game_over = True
            self.n_progress += 1
            self.n_wins += 1
            statoti=1
        elif(state[action[1]][action[0]][0]!=9):

            reward = self.rewards['no_progress']
            statoti=2
        else:
            # if all(t==-0.125 for t in neighbors): # if guess (all neighbors are unsolved)
            #     reward = self.rewards['guess']
            # else:
            if(self.neighborsnotrevealed(action)):

                reward = self.rewards['guess']
                self.listtoadd=[]
                self.emptyroll(action)
                statoti=3
            else:

                reward = self.rewards['progress']
                self.n_progress += 1 # track n of non-isoloated clicks
                self.listtoadd=[]
                self.emptyroll(action)
                statoti=4

            # new_grid=grid


        return state, reward, game_over,statoti

