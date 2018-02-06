# Module: urban_planner_helpers

import copy

global doSRand
doSRand = True


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

    num_industrial = line_list[0]
    num_commercial = line_list[1]
    num_residential = line_list[2]

    board = []

    for ii in range(3, length):
        board.append(line_list[ii].split(','))

    return num_industrial, num_commercial, num_residential, board


def generate_empty_board(x, y):
    return [[None] * x for _ in range(y)]


def generate_starting_boards(number_to_make, x, y):
    list_of_starting_boards = []

    for ii in range(number_to_make):
        list_of_starting_boards.append(generate_empty_board(x, y))

    return list_of_starting_boards


# prints the board without the list markers and as separate lines for each row
def print_board(board):
    str_board = []

    for yy in range(len(board)):
        row_str = []
        for xx in range(len(board[0])):
            row_str.append(str(board[yy][xx]))
        str_board.append(row_str)

    for row in str_board:
        print(''.join(row))


# def random_place(empty_board, zone_tuple, board_size_x, board_size_y):
#     global doSRand
#
#     print('board is sized %ix%i' % (board_size_x, board_size_y))
#
#     num_industrial, num_commercial, num_residential = zone_tuple
#
#     if doSRand:
#         random.seed()
#         doSRand = False
#
#     ii = 0
#     while ii < int(num_industrial):
#         rand_x = random.randrange(board_size_x)
#         rand_y = random.randrange(board_size_y)
#
#         print('rand is at %ix%i' % rand_x, rand_y)
#
#         if empty_board[rand_y][rand_x] is '0':
#             empty_board[rand_y][rand_x] = 'I'
#             ii += 1
#
#     # cc = 0
#     # while cc < int(num_commercial):
#     #     rand_x = random.randrange(board_size_x)
#     #     rand_y = random.randrange(board_size_y)
#     #
#     #     if empty_board[rand_y][rand_x] is '0':
#     #         empty_board[rand_y][rand_x] = 'C'
#     #         cc += 1
#     #
#     # rr = 0
#     # while rr < int(num_commercial):
#     #     rand_x = random.randrange(board_size_x)
#     #     rand_y = random.randrange(board_size_y)
#     #
#     #     if empty_board[rand_y][rand_x] is '0':
#     #         empty_board[rand_y][rand_x] = 'R'
#     #         rr += 1
#
#     return empty_board
#
#


def generate_start_heuristics(input_board):
    residential_initial = copy_and_invert_costs(input_board)
    commercial_initial = copy.deepcopy(residential_initial)
    industrial_initial = copy.deepcopy(residential_initial)

    list_of_dumps = find_this_landmarks(input_board, 'X')
    list_of_looks = find_this_landmarks(input_board, 'S')

    residential_updated = calculate_costs(residential_initial, list_of_dumps, list_of_looks, 'R')
    commercial_updated = calculate_costs(commercial_initial, list_of_dumps, list_of_looks, 'C')
    industrial_updated = calculate_costs(industrial_initial, list_of_dumps, list_of_looks, 'I')

    print(residential_updated)
    print(commercial_updated)
    print(industrial_updated)

    return residential_updated, commercial_updated, industrial_updated


def calculate_costs(initial_map, dumps, looks, board_type):
    board_size_y = len(initial_map)
    board_size_x = len(initial_map[0])

    for dump in dumps:
        affected_spots = find_list_of_points_manhattan_away(dump[0], dump[1], 2)

        for spot in affected_spots:

            x = spot[0]
            y = spot[1]

            if board_size_x > x >= 0 and board_size_y > y >= 0:
                # remember, boards are [y][x]
                map_val = initial_map[y][x]
                if map_val != 'S' and map_val != 'X':
                    if board_type == 'I':
                        initial_map[y][x] = map_val - 10
                    if board_type == 'R' or board_type == 'C':
                        initial_map[y][x] = map_val - 20

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

    return initial_map


def copy_and_invert_costs(input_board):
    out_board = generate_empty_board(len(input_board[0]), len(input_board))

    for yy in range(len(input_board)):
        for xx in range(len(input_board[yy])):
            map_val = input_board[yy][xx]
            if map_val != 'X' and map_val != 'S':
                out_board[yy][xx] = -int(map_val)
            else:
                out_board[yy][xx] = map_val

    return out_board


def find_list_of_points_manhattan_away(start_x, start_y, distance):
    list_of_points = []

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


def find_this_landmarks(board, landmark):
    list_of_points = []

    for yy, row in enumerate(board):
        for xx, spot in enumerate(row):
            if spot == landmark:
                list_of_points.append((xx, yy))

    return list_of_points
