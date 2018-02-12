#
# Sample code showing implementation and Visualization of Breadth-First Search and Depth-First Search in a tree with uniform branching factor

import pygame
import math
import time
import random


#---------------Visualization section starts------------------------#


# Setting up pygame variables
def initialize_pygame(config_space_x, config_space_y):
    pygame.init()
    window_size = [int(config_space_x), int(config_space_y)]
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Modified N-Queens Problem')
    white = 255, 255, 255
    red = 255,0,0
    black = 20, 20, 40
    pink = 249,231, 228
    blue = 0,255,255
    screen.fill(pink)
    return screen, white, red, black, pink, blue

# ---------------------------------------------------------------
# Creating the pygame configuration for initial setup
def create_scene(N):

    p = -1
    screen, white, red, black, pink , blue = initialize_pygame(1000, 1000)
    square_size = 800/N
    point_list = [(100 + (800/N)*i, 100 + (800/N)*j) for i in range(0,N) for j in range(0,N)] # Numbering squares column wise
    # print (point_list)
    # print (len(point_list))

    for t in range(0,N):
        for q in range(0,N):
            p+=1
            if t%2 == q%2:
                color = white
            else:
                color = black
            pygame.draw.rect(screen, color, (point_list[p][0], point_list[p][1], square_size, square_size ))      #Checkerboard colouring of squares
    return screen, white, red, black, pink, N, point_list, square_size

# ---------------------------------------------------------------
# Creating the initial scene with randomly distributed Queens
def initial_scene( N, screen=0, point_list=0, square_size=0, red=0, loc_visualize = 0):

    InitQueenLoc = [random.randint(0,N-1)+i*N  for i in range(0,N)]         #Randomly generating a cconfiguration for the setup to start in
    # print (InitQueenLoc)

    if loc_visualize!=0:
        locs = [element[0] + element[1]*N for element in loc_visualize]
        for loc in locs:
            pygame.draw.circle(screen, red, (point_list[loc][0]+square_size/2, point_list[loc][1] +square_size/2), int(square_size*0.3)) #Visualizing the initial config
        pygame.display.update()
        time.sleep(0.1)

    return InitQueenLoc

#---------------Visualization section ends ------------------------#




#---------------Calculation section starts-------------------------#


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
            if checkPoint[0]==candidates[0] or checkPoint[1]==candidates[1] or (checkPoint[0]-checkPoint[1])==(candidates[0]-candidates[1]) or \
                (checkPoint[0]+checkPoint[1])==(candidates[0]+candidates[1]):
                attacks +=1
                # print (checkPoint)
                # print (candidates)
                # print ("---------------")
    # print ("Total attacks", (attacks-len(currentScene))/2)
    if attacks != len(currentScene):
        heu = 10 + (attacks-len(currentScene))/2
    else:
        heu = 0

    return currentScene, heu              # Returning the current positions of queens and number of queens attacking one-another


# ---------------------------------------------------------------
# Calculating heurstics for the current scene at different individual position of the Queens
def try_placement(currentScene, N):

    # print (currentScene)
    new = currentScene
    scene_status = []
    cost = 0
    for trialPos in currentScene:                                   # Trying all setups for each of the 6 queens

        # tempCurrentScene = currentScene
        # print (tempCurrentScene)

        tp = trialPos

        for i in range(0, N):

            # print ("*******************************************")
            # print ("trial pos", trialPos)

            pos = (i, tp[1])
            # print ("position to check", pos)
            new[new.index(tp)] = pos
            # print ("newSceen", new)

            tp = pos

            heuristicScene = [element[0] + element[1]*N for element in new]       # Queen positions in terms of consectuviely numbered squares
            sc, heuristicvalue = heuristic(heuristicScene,N)  # Heuristic value for the new configuration obtained after shifting the queen to the new location
            if trialPos[0] - pos[0] !=0:
                cost = 10 + (trialPos[0] - pos[0]) ** 2
            #
            # print ("Cost of movement", cost)
            # print ("Heuristic Scene in grid format", new)
            # print ("Heuristic Scene", heuristicScene)
            # print ("Heuristic Value", heuristicvalue)
            # print ("-----------------------")

            # print ("tuple is", tuple((new, heuristicvalue, cost)))  #, cost, heuristicvalue)))
            scene_status.append(tuple((tuple(new), heuristicvalue, cost)))
            # print (" *********************************************** ")


        new[new.index(pos)] = trialPos
    # print ("Final Scene equal to intial scene", new)

    return currentScene, scene_status                           # currentScene is the initially fed scene, scene_status has heuristic values and cost with the particular
                                                                # placement scene

# for element in scene_status:
#     print element


#---------------Calculation section end-------------------------#
