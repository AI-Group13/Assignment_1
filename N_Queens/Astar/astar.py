from nQueens import create_scene, initial_scene, heuristic, try_placement
import pygame
from queue import PriorityQueue
import numpy as np


def astar(attacks, allPos, currentScene, N):
    
    cumilative_Cost = 0
    Q = PriorityQueue()
    
    while(attacks > 0):
        
        #creates a heuristic map for one particular move or in other words branches one node
        heuristicMap = try_placement(allPos, currentScene, N)                   
        
        #adds the cost of the parent path to the current path and appends it to the priority queue
        hm = []
        for row in heuristicMap:
            hm.append((row[0] + cumilative_Cost, row[1] + cumilative_Cost , row[2]))
        
        for row in hm:
            Q.put((row))

        cumilative_Cost = 0
        
        #pops out the first or the move with the least (cost + heuristics)
        cScene = Q.get()
        
        #print(cScene)
        #add to a temporary variable to later add to the child branch
        cumilative_Cost+=cScene[1]
        
        #print(cScene[1])
        #converting tuple to list to be used by our function
        cScenes = list(cScene[2])
        
        #changing the current node to the best node from the queue
        currentScene = cScenes

        for checkPoint in currentScene:
            for candidates in currentScene:
                if checkPoint[0]==candidates[0] or checkPoint[1]==candidates[1] or (checkPoint[0]-checkPoint[1])==(candidates[0]-candidates[1]) or (checkPoint[0]+checkPoint[1])==(candidates[0]+candidates[1]):
                    attacks +=1
        attacks = (attacks-len(currentScene))/2  
        
    print("The solution is: " + str(currentScene))
    print("The total cost for the above solution is: " + str(cScene[1]))
    return currentScene


    



