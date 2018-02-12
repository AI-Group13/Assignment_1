import sys
import pygame
import math
import time
import random
from nQueens import create_scene, initial_scene, heuristic, try_placement
from nQueens_HillClimb import greedy_hillClimb

# Reading from the input file to get the grid size and the if the user wants visualization of the moves or not

def read_input_file(path_to_input_file):
    try:
        with open(path_to_input_file, 'r') as f:
            lines = f.read().splitlines()
            f.close()
    except IOError as e:
        print('Could not open the input file (%s).' % e)
        return
    grid_size = int(lines[0])

    if int(lines[1])!=1 and int(lines[1])!=0:
        sys.exit("Incorrect visualization condition fed as input ")
    else:
        visual = lines[1]
        print ("Visualization:", visual )

    return grid_size, int(visual)

# The main function that reads the input file and then runs the Hill Climb on the given grid size for N-Queens obeying the condition of visualization

def main():

    t_start = time.time()
    grid_size, visual = read_input_file('input.txt')
    InitQueenLoc = initial_scene(grid_size)  # screen, N, point_list, square_size, red)

    print ("Solving Hill Climbing for grid-size ", grid_size )

    greedy_hillClimb(InitQueenLoc,grid_size, visual)

    print ("Hill Climbing Complete")

    # Measure the total time taken for the program to run

    time_taken = (time.time() - t_start)
    print ("Time taken", time_taken )
    # time.sleep(10)

if __name__ == '__main__':
    main()
