


import pygame
import math
import time
import random
import numpy as np

# ------------------------------------------------------------------------
# Setting up pygame variables



#--------------------------------------------------------------------------
# Creating the pygame configuration for intial setup
def create_scene(N):
    window_size = 500
    square_size = int(window_size/N)
    window_size = square_size * N
    point_list = [((square_size)*i,(square_size)*j) for i in range(0,N) for j in range(0,N)] # Numbering squares column wise
    allPos = [(i,j) for i in range(0,N) for j in range(0,N)]        # Numbering squares with column-row notation
    
    return N, point_list, square_size, allPos, window_size



# ---------------------------------------------------------------
# Creating the initial scene with randomly distributed Queens
def initial_scene(N):
    
    InitQueenLoc = [random.randint(0,N-1)+i*N  for i in range(N)]         #Randomly generating a cconfiguration for the setup to start in
    
    # for loc in InitQueenLoc:
    #     pygame.draw.circle(screen, red, (point_list[loc][0]+square_size/2, point_list[loc][1] +square_size/2), int(square_size*0.3)) #Visualizing the initial config
    #     pygame.display.update()
    #     time.sleep(0.1)
    return InitQueenLoc

def draw_graph(currentScene, N, point_list, square_size, window_size):
    pygame.init()
    screen = pygame.display.set_mode((window_size,window_size))
    pygame.display.set_caption('Modified N-Queens Problem')
    red = 32, 174, 170
    black_tile = 0, 0, 0
    screen.fill((255,255,255))
    count = 0
    for i in range(0, window_size, square_size):
        if count%2==0 or count==0:
            n=0
        else:
            n=square_size
        for j in range(n,window_size, 2*square_size):
            screen.fill(black_tile, (i, j, square_size, square_size))
        count+=1   
    newQueenLoc = [i[0] + i[1]*N for i in currentScene]
    for loc in newQueenLoc:
        pygame.draw.circle(screen, red, (int(point_list[loc][0]+square_size/2), \
        int(point_list[loc][1] + square_size/2)), int(square_size*0.3))              #Visualizing the initial config
        pygame.display.update()
    time.sleep(8)


# ---------------------------------------------------------------
# Calculating the heuristic
def heuristic(currentPos, N):
    currentScene = []
    attacks = 0
    counter = -1
    for a in range(0,N):
        for b in range(0,N):
            counter += 1                                            # Converting the consecutive numbering of squares to (row, column) numbering for calculating
            if counter in currentPos:                               # the number of queens attacking one another
                currentScene.append((b,a))
    for checkPoint in currentScene:
        for candidates in currentScene:
            if checkPoint[0]==candidates[0] or checkPoint[1]==candidates[1] or \
            (checkPoint[0]-checkPoint[1])==(candidates[0]-candidates[1]) or \
            (checkPoint[0]+checkPoint[1])==(candidates[0]+candidates[1]):
                attacks +=1
    return currentScene, (attacks-len(currentScene))/2              # Returning the current positions of queens and number of queens attacking one-another




#----------------------------------------------------------------------------------
#
def try_placement(allPos, currentScene, N):

    new = currentScene
    scene_status = []
    heuristicMap = []
    costMap = []
    for trialPos in currentScene:                                   # Trying all setups for each of the 6 queens
        tp = trialPos

        for i in range(0, N):
            #print("some")
            pos = (i, tp[1])
            
            new[new.index(tp)] = pos
            
            tp = pos

            heuristicScene = [element[0] + element[1]*N for element in new]       # Queen positions in terms of consectuviely numbered squares
           
            scene, attacks = heuristic(heuristicScene,N)  # Heuristic value for the new configuration obtained after shifting the queen to the new location
           
            if attacks >= 1:
                heuristicvalue = 10 + attacks

            else:
                heuristicvalue = 0
            
            cost = 10 + ((trialPos[0] - pos[0]) ** 2)
           
            scene_status.append(tuple((tuple(new), heuristicvalue, cost)))
            
            if cost > 10:
                heuristicMap.append(((cost+heuristicvalue), cost, tuple(new)))
                #costMap.append((cost, tuple(new)))
    
        
        new[new.index(pos)] = trialPos
    #print(heuristicMap)
    return heuristicMap