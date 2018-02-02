# Module: urban_planner_helpers


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
        board.append(list(line_list[ii]))

    return num_industrial, num_commercial, num_residential, board


def generate_empty_board(x, y):
    board = []

    for row in range(y):
        row_temp = []
        for col in range(x):
            row_temp.append(' ')
        board.append(row_temp)
        row_temp.clear()


def generate_starting_boards(number_to_make, x, y):
    list_of_starting_boards = []

    for ii in range(number_to_make):
        list_of_starting_boards.append(generate_empty_board(x, y))

    return list_of_starting_boards


# prints the board without the list markers and as separate lines for each row
def print_board(board):
    for row in board:
        print(''.join(row))
