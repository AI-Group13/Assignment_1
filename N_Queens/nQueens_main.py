
import sys
import pygame
import math
import time
import random
from nQueens import initial_scene, heuristic, try_placement

from nQueens_HillClimb import greedy_hillClimb


# screen, white, red, black, pink, blue = initialize_pygame(1000, 1000)

def read_input_file(path_to_input_file):
    try:
        with open(path_to_input_file, 'r') as f:
            lines = f.read().splitlines()
            f.close()
    except IOError as e:
        print('Could not open the input file (%s).' % e)
        return
    grid_size = int(lines[0])

    if int(lines[1])!=1 and int(lines[1])!=2:
        sys.exit("Incorrect algorithm type as input ")
    else:
        algo_used = lines[1]
        print ("algo_used is ", algo_used )

    return grid_size, int(algo_used)


def main():

    t_start = time.time()
    grid_size, algo_used = read_input_file('/media/akshay/OS/Imported/WorcesterPolytechnicInstitute/Sem II/Artificial Intelligence/searchAlgos/input.txt')

    if algo_used==1:
        # a_star()
        print ("A star algo will be used")

    elif algo_used==2:
        InitQueenLoc = initial_scene(grid_size)  # screen, N, point_list, square_size, red)
        greedy_hillClimb(InitQueenLoc,grid_size)
    print ("Complete")
    time_taken = (time.time() - t_start)
    print ("Time taken", time_taken )

if __name__ == '__main__':

    main()
    # pygame.display.update()
    # time.sleep(10)