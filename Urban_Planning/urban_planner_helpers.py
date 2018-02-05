# Module: urban_planner_helpers

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

    for ii in range (3, length):
        board.append(line_list[ii].split(','))

    return num_industrial, num_commercial, num_residential, board


def generate_empty_board(x, y):
    board = []

    row = []

    for entry in range(x):
        row.append('0')

    for rows in range(y):
        board.append(row)

    return board


def generate_starting_boards(number_to_make, x, y):
    list_of_starting_boards = []

    for ii in range(number_to_make):
        list_of_starting_boards.append(generate_empty_board(x, y))

    return list_of_starting_boards


# prints the board without the list markers and as separate lines for each row
def print_board(board):
    for row in board:
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
