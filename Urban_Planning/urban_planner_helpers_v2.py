# Module: urban_planner_helpers
import numpy as np
import random
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


def generate_starting_boards(number_to_make, board_map):
    
    #Geenrates a board with shuffled values EXCEPT toxic and scenic sites
    list_of_starting_boards = []
    flat_board = np.array(board_map).flatten()
    print(flat_board)
    shuffle_board = flat_board.copy()
#    print(shuffle_board)
    toxic_loc = np.where(flat_board == 'x' )[0]
    scenic_loc = np.where(flat_board == 'S')[0]
#    print(scenic_loc1)
    
##Solution 1
    counter = number_to_make
    #for ii in range(number_to_make):
    while (counter != 0):
        random.shuffle(shuffle_board)
        new_scenic_loc = np.where(shuffle_board == 'S')[0]
        if np.intersect1d(scenic_loc,new_scenic_loc).size:
            continue
        for i in range(len(new_scenic_loc)):
            shuffle_board[new_scenic_loc[i]],shuffle_board[scenic_loc[i]] = shuffle_board[scenic_loc[i]],shuffle_board[new_scenic_loc[i]]
        new_tox_loc = np.where(shuffle_board == 'x')[0]
        if np.intersect1d(toxic_loc,new_tox_loc).size:
            continue
        for i in range(len(new_tox_loc)):
            shuffle_board[new_tox_loc[i]],shuffle_board[toxic_loc[i]] = shuffle_board[toxic_loc[i]],shuffle_board[new_tox_loc[i]] 
        print(shuffle_board)
        reshaped_board = np.reshape(shuffle_board.tolist(),(len(board_map),len(board_map[0])))
        list_of_starting_boards.append(reshaped_board.tolist())
        counter -= 1
        
    return list_of_starting_boards

