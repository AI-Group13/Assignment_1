# Module: urban_planner_helpers
import random
import time
from itertools import permutations
import copy
import numpy as np


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
    random.seed(time.time())

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
    residential_locations = find_this_landmarks(organism_map, 'R')
    commercial_locations = find_this_landmarks(organism_map, 'C')
    industrial_locations = find_this_landmarks(organism_map, 'I')

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
        surrounding_zone = find_list_of_points_manhattan_away(zone[0], zone[1], 3)

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

        surrounding_zone = find_list_of_points_manhattan_away(zone[0], zone[1], 3)
        for spot in surrounding_zone:
            x = spot[0]
            y = spot[1]

            # so long as that spot is within the confines of the board:
            if board_size_x > x >= 0 and board_size_y > y >= 0:
                map_val = organism_map[y][x]

                if map_val == 'R':
                    score += 5

        surrounding_zone = find_list_of_points_manhattan_away(zone[0], zone[1], 2)
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

        surrounding_zone = find_list_of_points_manhattan_away(zone[0], zone[1], 2)
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


def shift_zone(input_map, heuristics):
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
                score = calculate_fitness(np.reshape(shift_map, (r, c)), heuristics)
                zipped = np.append(shift_map, score)

                scores.append(zipped)
                shift_map[val_without_zones[j]] = 0
            shift_map[val_zone[i]] = zones[x]
    return scores


def selection(ip_maps, heuristics):
    total_scores = []
    for i in ip_maps:
        score = calculate_fitness(i, heuristics)
        total_scores.append(score)

    sorted_maps = [x for _, x in sorted(zip(total_scores, ip_maps), reverse=True)]
    return sorted_maps


# Calculates the constant costs of each location on the board for each type of zone
# this does not have anything to do with interzone scores, just scores from being near toxic dumps, scenic views, and
# the cost to build on each spot
def generate_start_heuristics(input_board):
    # create a copy of each board type
    # also converts the cost from a string number to the negative integer
    residential_initial = copy_and_invert_costs(input_board)
    commercial_initial = copy.deepcopy(residential_initial)
    industrial_initial = copy.deepcopy(residential_initial)

    # go through the input board and find all the locations of Dumps and Scenic Views
    list_of_dumps = find_this_landmarks(input_board, 'X')
    list_of_looks = find_this_landmarks(input_board, 'S')

    # go through each kind of map and add the benefits and drawbacks for that type of zone to each location on the map
    residential_updated = calculate_costs(residential_initial, list_of_dumps, list_of_looks, 'R')
    commercial_updated = calculate_costs(commercial_initial, list_of_dumps, list_of_looks, 'C')
    industrial_updated = calculate_costs(industrial_initial, list_of_dumps, list_of_looks, 'I')

    # return a tuple of the threee kinds of maps
    return residential_updated, commercial_updated, industrial_updated


# This iterates over a map, using proviced locations of the dumps and scenic views, and board type, to create the static
# cost map of the entire board for that type of zone
def calculate_costs(initial_map, dumps, looks, board_type):
    # calculate the board size
    board_size_y = len(initial_map)
    board_size_x = len(initial_map[0])

    # for each of the dumps in the list of dumps provided:
    for dump in dumps:
        # find a list of spots that are 2 away from the dump, these spots are the ones that are negativaly affected
        affected_spots = find_list_of_points_manhattan_away(dump[0], dump[1], 2)

        # for each affected spot:
        for spot in affected_spots:
            # find the x and y location of that spot
            x = spot[0]
            y = spot[1]

            # so long as that spot is within the confines of the board:
            if board_size_x > x >= 0 and board_size_y > y >= 0:
                # store the value at that spot as a variable
                # remember, boards are [y][x]
                map_val = initial_map[y][x]

                # if that spot is NOT a scenic view and NOT the dump itself:
                if map_val != 'S' and map_val != 'X':
                    # If were making this map for Industrial locations:
                    if board_type == 'I':
                        # increase the penalty for building here
                        initial_map[y][x] = map_val - 10
                    # if it is a residential zone or commerical zone
                    if board_type == 'R' or board_type == 'C':
                        # also decrease the cost, just by more
                        initial_map[y][x] = map_val - 20

    # do the same thing as dumps but for scenic views. This only affects residential locations, and decreases the cost
    # to build there instead of increasing it.
    for overlook in looks:
        nice_homes = find_list_of_points_manhattan_away(overlook[0], overlook[1], 2)

        for house in nice_homes:

            x = house[0]
            y = house[1]

            if board_size_x > x >= 0 and board_size_y > y >= 0:

                # remember, boards are [y][x]
                map_val = initial_map[house[1]][house[0]]
                if map_val != 'S' and map_val != 'X':
                    if board_type == 'R':
                        initial_map[house[1]][house[0]] = map_val + 10

    # return the generated static cost map
    return initial_map


# This function takes in an input board and creates a new board of mixed strings and integers
# the integers are then made negative (invert) so that the cost is accuratly reflected mathmathically
def copy_and_invert_costs(input_board):
    # create an empty board
    out_board = generate_empty_board(len(input_board[0]), len(input_board))

    # for each row of the board
    for yy in range(len(input_board)):
        for xx in range(len(input_board[yy])):
            # for each entry, store the value as a variable (thank god for dynamic typing)
            map_val = input_board[yy][xx]
            # If the value is NOT a dump or a scenic view:
            if map_val != 'X' and map_val != 'S':
                # convert the char to an integer, and make it negative
                out_board[yy][xx] = -int(map_val)
            else:
                # otherwise just copy it over directly
                out_board[yy][xx] = map_val
    # return the out board after everything has been transferred over
    return out_board


# this function returns a list of points a certain manhattan distance away
# this function does not do anything with those locations, and doesn't care if they're outside the map boundaries
# those are handled by the function making use of these locations
def find_list_of_points_manhattan_away(start_x, start_y, distance):
    # list of points to store and return later
    list_of_points = []

    # honestly, this code is black magic I found on the internet. It works, and doesn't return any duplicates
    # my original part returned so many duplicates
    for i in range(1, distance + 1):

        list_of_points.append((start_x, start_y + i))
        list_of_points.append((start_x, start_y - i))
        list_of_points.append((start_x + i, start_y))
        list_of_points.append((start_x - i, start_y))

        for j in range(1, i):
            list_of_points.append((start_x + j, start_y + i - j))
            list_of_points.append((start_x - j, start_y + i - j))
            list_of_points.append((start_x + j, start_y - i + j))
            list_of_points.append((start_x - j, start_y - i + j))

    return list_of_points


# iterate over the map and find all the locations of the given landmark
def find_this_landmarks(board, landmark):
    list_of_points = []

    for yy, row in enumerate(board):
        for xx, spot in enumerate(row):
            if spot == landmark:
                list_of_points.append((xx, yy))

    return list_of_points


# Makes an empty board of None with the correct x and y size
def generate_empty_board(x, y):
    return [[None] * x for _ in range(y)]
