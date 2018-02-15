import sys
import pygame
import math
import time
import random
from nQueens import create_scene, initial_scene, heuristic, try_placement
from astar import astar
from nQueens import initial_scene, heuristic, try_placement, draw_graph



#-----------------------------------------------------------------------------------------------------
#reads a text file for the inputs :         1. Number of Queen          2. The algorithm to be applied
# def read_input_file(path_to_input_file):
#     try:
#         with open(path_to_input_file, 'r') as f:
#             lines = f.read().splitlines()
#             f.close()
#     except IOError as e:
#         print('Could not open the input file (%s).' % e)
#         return
#     grid_size = int(lines[0])

#     if int(lines[1])!=1 and int(lines[1])!=2:
#         sys.exit("Incorrect algorithm type as input ")
#     else:
#         algo_used = lines[1]
#         print ("algo_used is ", algo_used )

#     return grid_size, int(algo_used)




#-------------------------------------------------------------------------------------------------------
def main():
    t_start = time.time()

    grid_size,  = input('Enter the size of the chess board: ')
    grid_size = int(grid_size)
    # print(grid_size)

    #grid_size = 6
    #creates and displays a chess board
    N, point_list, square_size, allPos, window_size = create_scene(grid_size)

    #gives the queens random location in each column and displays on the chess board
    InitQueenLoc = initial_scene(N)

    #returns the current position of all the queens in a numbered fashion (1, 2, 3, 4, 5, ......) and returns the pair of queens attacking each other
    currentScene, attacks = heuristic(InitQueenLoc, N)
    print("The initial queen position is: " + str(currentScene))
    
    currentScene = astar(attacks, allPos, currentScene, N)

    time_taken = (time.time() - t_start)
    print('The time taken to reach the above solution is: ' + str(time_taken) + " seconds")

    draw_graph(currentScene, N, point_list, square_size, window_size)
    

if __name__ == '__main__':

    main()
    # pygame.display.update()
    # time.sleep(10)
