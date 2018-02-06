#!/usr/bin/env python3

import sys
import time
import urban_planner_helpers_v2
import timeit
#Test
from random import shuffle
import numpy as np

max_duration = 10 # 10 seconds
number_boards = 10


# filler functions
def hillclimb():

    return


def genetics(list_of_hill_climbs):
    
    elite_ratio = 0.3
    normal_ratio = 0.3
    
    #Plceholder score-map
    score_map = np.random.randint(100, size=100)
    
    #Placeholder Elite seelction
    elite_maps = list_of_hill_climbs[:int(len(list_of_hill_climbs)*elite_ratio)]
    normal_maps = list_of_hill_climbs[int(len(list_of_hill_climbs)*elite_ratio):int((len(list_of_hill_climbs)*(elite_ratio+normal_ratio)))]
    new_maps = urban_planner_helpers_v2.generate_mashed_maps(list_of_hill_climbs,elite_maps,normal_maps)
    print(new_maps)
    #Temporary score map
    
    
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
    
    ## placeholder-code for selection
    
    still_computing = True
    
    genetics(list_of_hill_climbs)

#    while (time.time() - start_time) < max_duration and still_computing:
#        for board in list_of_hill_climbs:
#            hillclimb()

        # do genetic engineering
#        genetics()
        
