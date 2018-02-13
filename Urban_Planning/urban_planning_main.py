#!/usr/bin/env python3

import sys
import time
import urban_planner_helpers
import timeit
# Test
from random import shuffle
import numpy as np

max_duration = 5  # 10 seconds
number_boards = 100


# filler functions
def hillclimb(Zoned_board, heuristics):
    ''' The number of times you repeat the cycle to check if it hit the highest score, before restarts'''
    r = len(Zoned_board)
    c = len(Zoned_board[0])
    termination_parameter = 4

    score_counter = 0
    repetition_counter = 0
    hillclimb_board = list(Zoned_board)

    while (repetition_counter != termination_parameter):
        possible_maps_scores = urban_planner_helpers.shift_zone(hillclimb_board, heuristics)
        actual_scores = [int(i[-1]) for i in possible_maps_scores]
        loc_max_score = np.where(actual_scores == np.max(actual_scores))[0]
        next_move = possible_maps_scores[loc_max_score[0]][:-1]
        if score_counter < np.max(actual_scores):
            score_counter = np.max(actual_scores)
        else:
            repetition_counter += 1
        hillclimb_board = np.reshape(next_move, (r, c))

    return score_counter


def genetics(gen_maps, heuristics):
    elite_ratio = 0.3
    normal_ratio = 0.3

    mutation_ratio = 0.1  # Can't be greater than  (1-elite_ratio)

    score_map = urban_planner_helpers.selection(gen_maps, heuristics)

    elite_maps = score_map[:int(len(gen_maps) * elite_ratio)]
    normal_maps = gen_maps[int(len(gen_maps) * elite_ratio):int(
        (len(gen_maps) * (elite_ratio + normal_ratio)))]
    Maps_to_mutate = normal_maps
    mutation_indices = np.random.choice([i for i in range(len(Maps_to_mutate))],
                                        int(len(gen_maps) * mutation_ratio)).tolist()
    for i in mutation_indices:
        Maps_to_mutate[i] = urban_planner_helpers.mutate(Maps_to_mutate[i])

    Crossover_Mutated_maps = urban_planner_helpers.cross_over(gen_maps, elite_maps, normal_maps)

    max_score = 0
    New_mapset = elite_maps + Crossover_Mutated_maps
    for i in range(len(score_map)):
        #        print(i)
        score = urban_planner_helpers.calculate_fitness(New_mapset[i], heuristics)
        if score > max_score:
            max_score = score

    return New_mapset, max_score


if __name__ == '__main__':

    timeit.timeit()
    # check to make sure a valid input path was given, exit otherwise
    if len(sys.argv) < 3:
        print("You must provide the path to the input text file, and the mode")
        sys.exit(-1)

    pathToFile = sys.argv[1]

    mode = sys.argv[2]
    print(mode)

    if mode != 'genetic' and mode != 'hill':
        print("Incorrect mode entered.\nPlease choose either \'genetic\' or \'hill\'")

    (num_industrial, num_commercial, num_residential, board_map) = urban_planner_helpers.read_input_file(pathToFile)
    board_size_x = len(board_map)
    board_size_y = len(board_map[0])

    zone_tuple = (num_industrial, num_commercial, num_residential)
    heuristics = urban_planner_helpers.generate_start_heuristics(board_map)

    Zoned_board = urban_planner_helpers.Add_zones(board_map, num_industrial, num_commercial, num_residential)
    hill_board = list(Zoned_board)
    gen_maps = urban_planner_helpers.generate_starting_boards(number_boards, Zoned_board)

    hill_score = 0
    genetic_score = 0

    counter = 0
    start_time = time.time()
    still_computing = True

    while (time.time() - start_time) < max_duration and still_computing:

        if mode == 'genetic':
            '''Genetics'''
            new_maps, current_score = genetics(gen_maps, heuristics)
            gen_maps = new_maps
            if current_score > genetic_score:
                genetic_score = current_score
            counter += 1
            print(current_score)
        elif mode == 'hill':
            ''' Hill Climbing '''
            current_score = hillclimb(hill_board, heuristics)
            if hill_score < current_score:
                hill_score = current_score
            hill_board = urban_planner_helpers.generate_starting_boards(1, Zoned_board)
            counter += 1
            print(current_score)

    if mode == 'genetic':
        print("Genetic Algorithm operated ", counter, " times")
        print("Max score for Genetic Algorithm: ", genetic_score)

    elif mode == 'hill':
        print("Hill climbing operated ", counter, " times")
        print("Max score for hill climbing: ", hill_score)
