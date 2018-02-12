# Module: urban_planner_helpers
import random
from itertools import permutations

import numpy as np

import urban_planner_helpers


# reads the input file and returns a tuple containing relevant data
def read_input_file(path_to_input_file):
    try:
        with open(path_to_input_file, 'r') as f:

            line_list = f.read().splitlines()
            f.close()

    except IOError as e:
        print('Could not open the input file (%s).' % e)
        return

    length = len(line_list)
    num_industrial = int(line_list[0])
    num_commercial = int(line_list[1])
    num_residential = int(line_list[2])

    board = []

    for ii in range(3, length):
        # board.append(list(line_list[ii]))
        board.append(line_list[ii].split(','))

    return num_industrial, num_commercial, num_residential, board


def generate_starting_boards(number_to_make, board_map):
    board_size_y = len(board_map)
    board_size_x = len(board_map[0])
    # Geenrates a board with shuffled values EXCEPT toxic and scenic sites
    list_of_starting_boards = []
    flat_board = np.array(board_map).flatten()
#    print(flat_board)
    shuffle_board = flat_board.copy()
    #    print(shuffle_board)
    toxic_loc = np.where(flat_board == 'X')[0]
    scenic_loc = np.where(flat_board == 'S')[0]
    #    print(scenic_loc1)
    ##Solution 1
    counter = number_to_make
    # for ii in range(number_to_make):
    while (counter != 0):
        random.shuffle(shuffle_board)
        new_scenic_loc = np.where(shuffle_board == 'S')[0]
        if np.intersect1d(scenic_loc, new_scenic_loc).size:
            continue
        for i in range(len(new_scenic_loc)):
            shuffle_board[new_scenic_loc[i]], shuffle_board[scenic_loc[i]] = shuffle_board[scenic_loc[i]], \
                                                                             shuffle_board[new_scenic_loc[i]]
        new_tox_loc = np.where(shuffle_board == 'X')[0]
        if np.intersect1d(toxic_loc, new_tox_loc).size:
            continue
        for i in range(len(new_tox_loc)):
            shuffle_board[new_tox_loc[i]], shuffle_board[toxic_loc[i]] = shuffle_board[toxic_loc[i]], shuffle_board[
                new_tox_loc[i]]
        reshaped_board = np.reshape(shuffle_board.tolist(), (board_size_y, board_size_x))
        list_of_starting_boards.append(reshaped_board.tolist())
        counter -= 1
    if len(list_of_starting_boards) == 1:
        list_of_starting_boards = list_of_starting_boards[0]
    return list_of_starting_boards


def cross_over(list_of_hill_climbs, elite_maps, normal_maps):
    new_maps_length = len(list_of_hill_climbs) - len(elite_maps)
    expanded_elites, expanded_normals = list(elite_maps), list(normal_maps)
    while len(expanded_normals) != new_maps_length:
        expanded_normals.append(random.choice(expanded_normals))

    while len(expanded_elites) != new_maps_length:
        expanded_elites.append(random.choice(expanded_elites))

    new_maps = []

    for i in range(len(expanded_elites)):
        flat_elite = np.array(expanded_elites[i]).flatten()
        flat_normal = np.array(expanded_normals[i]).flatten()

        ct = 0
        L1 = ['C', 'R', 'I', 'C', 'R', 'I']
        L2 = ['R', 'C', 'C', 'I', 'I', 'R']
        L3 = ['I', 'I', 'R', 'R', 'C', 'C']

        p = list(permutations(['I', 'R', 'C']))

        while (ct == 0):

            '''
            Approach 1
            
            for i in range(len(L1)):
                if not intersect(flat_elite,L1[i],flat_normal,L2[i]):
                    if not intersect(flat_elite,L3[i],flat_normal,L2[i]):
                        flat_elite[np.where(flat_elite == L2[i])] = 0
                        flat_elite[np.where(flat_normal == L2[i])] = L2[i]
#                        print('Swapped')
                        ct = 1
            '''

            ''' Approach 2 '''
            for x in p:
                if not intersect(flat_elite, x[0], flat_normal, x[1]):
                    if not intersect(flat_elite, x[2], flat_normal, x[1]):
                        flat_elite[np.where(flat_elite == x[1])] = 0
                        flat_elite[np.where(flat_normal == x[1])] = x[1]
                        #                        print('Swapped')
                        ct = 1

            if ct == 0:
                #                print('Mutated')
                flat_normal = mutate(flat_normal)
        flat_elite = np.reshape(flat_elite.tolist(), (len(expanded_elites[i]), len(expanded_elites[i][0])))
        new_maps.append(flat_elite.tolist())

    return new_maps


def intersect(map1, K, map2, L):
    return np.intersect1d(np.where(map1 == K)[0], np.where(map2 == L)[0]).any()


def mutate(input_map):
    input_map = np.array(input_map).flatten()
    vals_to_avoid = np.concatenate((np.where(input_map == 'X')[0], np.where(input_map == 'S')[0]))
    all_vals = [i for i in range(len(input_map))]
    vals_to_move = list(set(all_vals) - set(vals_to_avoid.tolist()))
    (r1, r2) = (np.random.choice(vals_to_move), np.random.choice(vals_to_move))
    input_map[r1], input_map[r2] = input_map[r2], input_map[r1]
    return input_map


# this looks over a given map and uses the pregenerated cost maps to determine a score
def calculate_fitness(organism_map, maps_cost):
    # starting variable to add to to my hearts content
    score = 0

    board_size_y = len(organism_map)
    board_size_x = len(organism_map[0])

    # find the location of all the different zones
    residential_locations = urban_planner_helpers.find_this_landmarks(organism_map, 'R')
    commercial_locations = urban_planner_helpers.find_this_landmarks(organism_map, 'C')
    industrial_locations = urban_planner_helpers.find_this_landmarks(organism_map, 'I')

    # unpack the tuple of cost maps
    res_cost, com_cost, ind_cost = maps_cost
    # for each residential zone:
    for zone in residential_locations:

        # check in my cost maps to make sure I didn't get a dump or view in my landmarks.
        #  Shouldn't but I like being explicit
        # TODO see if this check is even needed later on
        if res_cost[zone[1]][zone[0]] != 'X' and res_cost[zone[1]][zone[0]] != 'S':
            # This is checking in the cost map, so the only valid entries besides X and S are negative Ints
            score += res_cost[zone[1]][zone[0]]

        # Find all the spots around me that can have benefits or drawbacks (3 for Residential locations)
        surrounding_zone = urban_planner_helpers.find_list_of_points_manhattan_away(zone[0], zone[1], 3)

        # for each of the surrounding spots:
        for spot in surrounding_zone:

            # take out the locations
            x = spot[0]
            y = spot[1]

            # so long as that spot is within the confines of the board:
            if board_size_x > x >= 0 and board_size_y > y >= 0:

                # store the value as a temp
                map_val = organism_map[y][x]

                # depending on what it finds, increment or decrement the score by 5
                if map_val == 'R':
                    score += 5
                elif map_val == 'I':
                    score -= 5

    # repeat for commercial and industrial
    for zone in commercial_locations:

        # TODO see if this check is even needed later on
        if com_cost[zone[1]][zone[0]] != 'X' and com_cost[zone[1]][zone[0]] != 'S':
            score += com_cost[zone[1]][zone[0]]

        surrounding_zone = urban_planner_helpers.find_list_of_points_manhattan_away(zone[0], zone[1], 3)
        for spot in surrounding_zone:
            x = spot[0]
            y = spot[1]

            # so long as that spot is within the confines of the board:
            if board_size_x > x >= 0 and board_size_y > y >= 0:
                map_val = organism_map[y][x]

                if map_val == 'R':
                    score += 5

        surrounding_zone = urban_planner_helpers.find_list_of_points_manhattan_away(zone[0], zone[1], 2)
        for spot in surrounding_zone:

            x = spot[0]
            y = spot[1]

            # so long as that spot is within the confines of the board:
            if board_size_x > x >= 0 and board_size_y > y >= 0:
                map_val = organism_map[y][x]

                if map_val == 'C':
                    score -= 5

    for zone in industrial_locations:

        # TODO see if this check is even needed later on
        if ind_cost[zone[1]][zone[0]] != 'X' and ind_cost[zone[1]][zone[0]] != 'S':
            score += ind_cost[zone[1]][zone[0]]

        surrounding_zone = urban_planner_helpers.find_list_of_points_manhattan_away(zone[0], zone[1], 2)
        for spot in surrounding_zone:

            x = spot[0]
            y = spot[1]
            # so long as that spot is within the confines of the board:
            if board_size_x > x >= 0 and board_size_y > y >= 0:

                map_val = organism_map[y][x]

                if map_val == 'I':
                    score += 3

    # after all that scoring, gimme the value
    return score


def Add_zones(Empty_map, Res_zones, Ind_zones, Com_zones):
    Zoned_map = np.array(Empty_map).flatten()
    vals_to_avoid = np.concatenate((np.where(Zoned_map == 'X')[0], np.where(Zoned_map == 'S')[0]))
    all_vals = [i for i in range(len(Zoned_map))]
    vals_to_change = list(set(all_vals) - set(vals_to_avoid.tolist()))
    if Res_zones + Ind_zones + Com_zones <= len(vals_to_change):
        zone_list = ['R' for i in range(Res_zones)] + ['I' for i in range(Ind_zones)] + ['C' for i in range(Com_zones)]
        np.random.shuffle(vals_to_change)
        vals_to_change = vals_to_change[:len(zone_list)]
        Zoned_map[vals_to_change] = [zone_list]
        Zoned_map = np.reshape(Zoned_map.tolist(), (len(Empty_map), len(Empty_map[0])))
        return Zoned_map
    else:
        print('Invalid number of zones')


def shift_zone(input_map,heuristics):

    r = len(input_map)
    c = len(input_map[0])
    ip_map = np.array(input_map).flatten()
    shift_map = ip_map.copy()
    vals_to_avoid = np.concatenate((np.where(ip_map == 'X')[0], np.where(ip_map == 'S')[0]))
    all_vals = [i for i in range(len(ip_map))]
    vals_to_change = list(set(all_vals) - set(vals_to_avoid.tolist()))
    val_other_zones = np.concatenate(
        (np.where(ip_map == 'C')[0], np.where(ip_map == 'R')[0], np.where(ip_map == 'I')[0])).tolist()
    val_without_zones = list(set(vals_to_change) - set(val_other_zones))
    scores = []
    zones = ['R', 'I', 'C']
    for x in range(3):
        val_zone = np.where(ip_map == zones[x])[0].tolist()
        for i in range(len(val_zone)):
            shift_map[val_zone[i]] = 0
            for j in range(len(val_without_zones)):
                shift_map[val_without_zones[j]] = zones[x]

                ''' put score function here'''
                score = calculate_fitness(np.reshape(shift_map,(r,c)),heuristics)
                zipped = np.append(shift_map, score)

                scores.append(zipped)
                shift_map[val_without_zones[j]] = 0
            shift_map[val_zone[i]] = zones[x]
    return scores

def selection(ip_maps,heuristics):
    total_scores = []
    for i in ip_maps:
        score = calculate_fitness(i,heuristics)
        total_scores.append(score)

    sorted_maps = [x for _,x in sorted(zip(total_scores,ip_maps),reverse=True)]
    return sorted_maps

        
        