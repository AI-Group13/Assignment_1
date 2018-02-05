#!/usr/bin/env python3

import sys
import time
import urban_planner_helpers_v2
import timeit
#Test
from random import shuffle

max_duration = 10 # 10 seconds
number_boards = 100


# filler functions
def hillclimb():
    return


def genetics():
    return


if __name__ == '__main__':
    
    timeit.timeit()
    # check to make sure a valid input path was given, exit otherwise
    if len(sys.argv) is 1:
        print("You must provide the path to the input text file")
        sys.exit(-1)

    pathToFile = sys.argv[1]
    print(sys.argv[1])
    
    (num_industrial, num_commercial, num_residential, board_map) = urban_planner_helpers_v2.read_input_file(pathToFile)
    board_size_x = len(board_map)
    board_size_y = len(board_map[0])

    list_of_hill_climbs = urban_planner_helpers_v2.generate_starting_boards(number_boards, board_map)

    start_time = time.time()

    still_computing = True

#    while (time.time() - start_time) < max_duration and still_computing:
#        for board in list_of_hill_climbs:
#            hillclimb()

        # do genetic engineering
#        genetics()
        
