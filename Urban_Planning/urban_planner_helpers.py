# Module: urban_planner_helpers

import copy


# reads the input file and returns a tuple containing relevant data
def read_input_file(path_to_input_file):
    try:
        # open the file, save the object as a nice accessible letter
        with open(path_to_input_file, 'r') as f:

            # split all the lines up
            line_list = f.read().splitlines()

            # close it
            f.close()

    # If we couldn't open it.
    except IOError as e:
        print('ERROR: %s.' % e)
        return

    # find how long it is
    length = len(line_list)

    # we know the order of the numbers so read them out and store
    num_industrial = int(line_list[0])
    num_commercial = int(line_list[1])
    num_residential = int(line_list[2])

    # make an empty board
    board = []

    # add each line list (comma separated) to the board
    for ii in range(3, length):
        board.append(line_list[ii].split(','))

    # return the number of each zone and that initial board
    return num_industrial, num_commercial, num_residential, board


# Makes an empty board of None with the correct x and y size
def generate_empty_board(x, y):
    return [[None] * x for _ in range(y)]


# generate a number of starting boards
def generate_starting_boards(number_to_make, x, y):
    # empty list of boards
    list_of_starting_boards = []

    # for the number needed, make the board and add it to the list
    for ii in range(number_to_make):
        list_of_starting_boards.append(generate_empty_board(x, y))

    # return the list of boards
    return list_of_starting_boards


# prints the board without the list markers and as separate lines for each row
def print_board(board):
    # empty list of the string version of the rows
    str_board = []

    # for each row
    for yy in range(len(board)):
        # list of chars
        row_str = []
        # for each board entry:
        for xx in range(len(board[0])):
            # convert to a string and print
            row_str.append(str(board[yy][xx]))
        # add that row to the list of rows
        str_board.append(row_str)

    # combine each row into one long string and print it
    for row in str_board:
        print(''.join(row))


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
