#!/usr/bin/env python3

import sys

import genetic_algorithm
import urban_planner_helpers
import urban_planner_helpers_v2
import genetic_algorithm

max_duration = 10  # 10 seconds
number_organisms = 100

mode = 'algorithm'  # TODO choose based on Beck's preferred input method

if __name__ == '__main__':

    # check to make sure a valid input path was given, exit otherwise
    if len(sys.argv) is 1:
        print("You must provide the path to the input text file")
        sys.exit(-1)

    pathToFile = sys.argv[1]

    (num_industrial, num_commercial, num_residential, board_map) = urban_planner_helpers.read_input_file(pathToFile)
    
    zone_tuple = (num_industrial, num_commercial, num_residential)
    generated_map_heuristics = urban_planner_helpers.generate_start_heuristics(board_map)
       
    rand_zone = urban_planner_helpers_v2.Add_zones(board_map,1,2,3)
    
    fit = urban_planner_helpers_v2.calculate_fitness(rand_zone, generated_map_heuristics)
    print(fit)

    board_size_y = len(board_map)
    board_size_x = len(board_map[0])

    # empty holders for reported values
    # score = 0
    # timestamp = 0
    # winning_map = board_map
    #
    # if mode is 'genetic':
    #
    #     working_boards = urban_planner_helpers.generate_starting_boards(number_organisms, board_size_x, board_size_y)
    #
    #     score, timestamp, winning_map = genetic_algorithm.genetics(board_map, working_boards, zone_tuple,
    #                                                                generated_map_heuristics)
    #
    # elif mode is 'algorithm':
    #
    #     working_boards = urban_planner_helpers.generate_starting_boards(1, board_size_x, board_size_y)
    #
    #     # score, timestamp, winning_map = hill_climbing.hillclimb(board_map, working_boards, zone_tuple,
    #     #                                                         generated_map_heuristics)

    # print('The winning score was: %i' % score)
    # print('The score was achieved at: %f seconds' % timestamp)
    # print('The winning map is: ')
    # urban_planner_helpers.print_board(winning_map)
