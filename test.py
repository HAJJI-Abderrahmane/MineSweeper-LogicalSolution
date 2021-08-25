import pygame, sys
from pygame import *
import time
import random
cellimg = pygame.image.load('cell.png')
emptycell2 = pygame.image.load('emptycell2.png')
bombimg = pygame.image.load("bomb.png")
def game_opening(width,height,screen,initialadd):
    # screen.blit()
    gray = (198, 198, 198)
    darkgray=(128,128,128)
    white=(255,255,255)
    pygame.display.update()
    # time.sleep(1)
    screen.fill(gray)


    for i in range(0,width,36):
        for j in range(initialadd,height+initialadd,36):

            draw_1block(screen,(i,j))
    pygame.display.update()

def draw_1block(screen,point):
    screen.blit(cellimg, (point[0],point[1]))
    # pygame.display.update()
# run = True
# game_opening(initialadd)
def drawover(cellnumber,screen,initialadd):

    screen.blit(emptycell2,(cellnumber[0]*36,cellnumber[1]*36+initialadd))
    pygame.display.update()

def actualcoordtocellnumbers(point):
    return (int(point[0]/36),int(point[1]/36))


def clicklistener(screen,initialadd,cellmax,machinelist,playerlist):
    ev = pygame.event.get()
    # poceed events
    for event in ev:
        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            if(pygame.mouse.get_pos()[1]>100):
                x=pygame.mouse.get_pos()[0]
                y=pygame.mouse.get_pos()[1]-100
                actualx=int(x/36)*36
                actualy=int(y/36)*36

                cellnumber=actualcoordtocellnumbers((actualx,actualy))
                index=cellmax*cellnumber[1]+cellnumber[0]
                if(machinelist[index]==-1):
                    screen.blit(bombimg,(cellnumber[0]*36,cellnumber[1]*36+initialadd))
                    pygame.display.update()
                    playerlist[index]=-1
                elif(machinelist[index]!=0):
                    screen.blit(emptycell2,(cellnumber[0]*36,cellnumber[1]*36+initialadd))
                    pygame.display.update()
                    writenumber(screen,cellnumber,machinelist[index],initialadd)
                    playerlist[index]=machinelist[index]
                else:
                    listtoadd=[]
                    emptyroll(screen,index,cellnumber,machinelist,playerlist,initialadd,cellmax)
                    # screen.blit(emptycell2,(cellnumber[0]*36,cellnumber[1]*36+initialadd))
                    # pygame.display.update()
                # else:
                #     drawover(cellnumber,screen,initialadd)
            for i in range(0,cellmax*cellmax,cellmax):
                print(playerlist[i:i+cellmax])
            print("###############################")
global listtoadd
listtoadd=[]





def emptyroll(screen,index,cellnumber,machinelist,playerlist,initialadd,cellmax):

    if(index in listtoadd):
        return 0
    listtoadd.append(index)

    # print("in")
    if(machinelist[index]==-1):

        return 0
    elif(machinelist[index]!=0):

        screen.blit(emptycell2,(cellnumber[0]*36,cellnumber[1]*36+initialadd))
        pygame.display.update()
        writenumber(screen,cellnumber,machinelist[index],initialadd)
        playerlist[index]=machinelist[index]
        return 0
    else:

        screen.blit(emptycell2,(cellnumber[0]*36,cellnumber[1]*36+initialadd))
        pygame.display.update()
        playerlist[index]=0
        y=int(index/cellmax)

        if(int((index-1)/cellmax)==y and index-1>=0):
            emptyroll(screen,index-1,(cellnumber[0]-1,cellnumber[1]),machinelist,playerlist,initialadd,cellmax)
        if(int((index+1)/cellmax)==y and index+1>=0):

            emptyroll(screen,index+1,(cellnumber[0]+1,cellnumber[1]),machinelist,playerlist,initialadd,cellmax)
        if(int((index-cellmax)/cellmax)==y-1 and index-cellmax>=0):

            emptyroll(screen,index-cellmax,(cellnumber[0],cellnumber[1]-1),machinelist,playerlist,initialadd,cellmax)
        if(int((index+cellmax)/cellmax)==y+1 and index+cellmax>=0):

            emptyroll(screen,index+cellmax,(cellnumber[0],cellnumber[1]+1),machinelist,playerlist,initialadd,cellmax)

        pygame.display.update()
        return 0




def creatingmachinelist(cellmax,bombnumber):
    machinelist=[0 for i in range(cellmax*cellmax)]
    randbomb= [i for i in range(cellmax*cellmax)]
    random.seed(5)
    randbomb= random.sample(randbomb,bombnumber)
    for i in randbomb:
        machinelist[i]=-1
    for idx,i in enumerate(machinelist):
        if(i==0):
            y=int(idx/cellmax)
            alllist=[]
            toplist=[idx-i for i in range(cellmax-1,cellmax+2) if int((idx-i)/cellmax)==y-1]
            bottomlist=[idx+i for i in range(cellmax-1,cellmax+2) if int((idx+i)/cellmax)==y+1]
            middlelist=[idx+i for i in range(-1,2,2) if int((idx+i)/cellmax)==y]
            alllist.extend(toplist)
            alllist.extend(bottomlist)
            alllist.extend(middlelist)
            alllist=[i for i in alllist if (i > 0 and i<cellmax*cellmax-1)]
            number=len([i for i in alllist if(machinelist[i]==-1)])
            machinelist[idx]=number
    return machinelist
colors=[(0,0,255),(0,123,0),(255,0,0),(0,0,123),(123,0,0),(0,123,123),(0,0,0),(123,123,123)]
def writenumber():
    # color1 = (0, 0, 255)
    # blue = (0, 0, 128)
    font = pygame.font.Font("arial.ttf", 20)

    # # create a text surface object,
    # # on which text is drawn on it.
    # text = font.render(str(number), True,colors[number-1])  
    # # create a rectangular object for the
    # # text surface object
    # textRect = text.get_rect()
    # decay=18
    # textRect.center = (cellnumber[0]*36+decay+2,cellnumber[1]*36+initialadd+decay)
    # screen.blit(text, textRect)
    # pygame.display.update()
    return font
def actionforml(screen,playerlist,machinelist,cellnumber,cellmax,initialadd):
    index=cellmax*cellnumber[1]+cellnumber[0]
    reward=None
    game_over=False
    if(machinelist[index]==-1):
        screen.blit(bombimg,(cellnumber[0]*36,cellnumber[1]*36+initialadd))
        pygame.display.update()
        playerlist[index]=-1
        reward = -100
        game_over=True
    elif(machinelist[index]!=0):
        screen.blit(emptycell2,(cellnumber[0]*36,cellnumber[1]*36+initialadd))
        pygame.display.update()
        writenumber(screen,cellnumber,machinelist[index],initialadd)
        playerlist[index]=machinelist[index]
        reward=5
    else:
        listtoadd=[]
        emptyroll(screen,index,cellnumber,machinelist,playerlist,initialadd,cellmax)
        reward=5

    if(not any(v is None for v in playerlist)):
    	game_over=True
    	reward=100
    return playerlist,reward,game_over

# def reset():



def main():
    pygame.init()
    cellmax=16
    width = 36*cellmax
    height = 36*cellmax
    FPS = 30
    initialadd=100
    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height+initialadd),0,32)
    machinelist=creatingmachinelist(cellmax,40)
    for i in range(0,cellmax*cellmax,cellmax):
        print(machinelist[i:i+cellmax])
    # rect = cat.get_rect(x=300, y=100)  # Create rectangle the same size as 'cat.png'.
    game_opening(width,height,screen,initialadd)

    playerlist=[None for i in range(cellmax*cellmax)]

    playerlist=actionforml(screen,playerlist,machinelist,(0,0),cellmax,initialadd)
    while True:
        # if rect.collidepoint(pygame.mouse.get_pos()):
        #     print("The mouse cursor is hovering over the cat")


        # clicklistener(screen,initialadd,cellmax,machinelist,playerlist)
        cellX=int(input("Enter X :"))
        cellY=int(input("Enter Y :"))
        playerlist=actionforml(screen,playerlist,machinelist,(cellX,cellY),cellmax,initialadd)


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # screen.blit(cat, rect)  # Use your rect to position the cat.
        # pygame.display.flip()
        fpsClock.tick(FPS)
font =writenumber()