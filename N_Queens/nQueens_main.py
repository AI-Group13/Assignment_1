
import sys
import pygame
import math
import time
import random
from nQueens import initialize_pygame, create_scene, initial_scene, heuristic, try_placement

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

    return grid_size, algo_used


def main():

    grid_size, algo_used = read_input_file('/media/akshay/OS/Imported/WorcesterPolytechnicInstitute/Sem II/Artificial Intelligence/searchAlgos/input.txt')

    screen, white, red, black, pink, N, point_list, square_size, allPos = create_scene(grid_size)

    InitQueenLoc = initial_scene(screen, N, point_list, square_size, red)

    currentScene, attacks = heuristic(InitQueenLoc, N)

    try_placement(allPos, currentScene, N)

    pygame.display.update()

if __name__ == '__main__':

    main()
    pygame.display.update()
    time.sleep(10)