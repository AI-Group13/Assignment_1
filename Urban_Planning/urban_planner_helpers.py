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

    for x in range(0, x):

        y_vector = []

        for y in range(0, y):
            y_vector.append(' ')

        board.append(y_vector)

    return board


def generate_starting_boards(number_to_make, x, y):
    list_of_starting_boards = []

    for ii in range(number_to_make):
        list_of_starting_boards.append(generate_empty_board(x, y))

    return list_of_starting_boards

