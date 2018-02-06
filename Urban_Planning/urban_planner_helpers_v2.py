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
        #board.append(list(line_list[ii]))
        board.append(line_list[ii].split(','))

    return num_industrial, num_commercial, num_residential, board


def generate_starting_boards(number_to_make, board_map):
    
    #Geenrates a board with shuffled values EXCEPT toxic and scenic sites
    list_of_starting_boards = []
    flat_board = np.array(board_map).flatten()
    shuffle_board = flat_board.copy()
#    print(shuffle_board)
    toxic_loc = np.where(flat_board == 'X' )[0]
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
        new_tox_loc = np.where(shuffle_board == 'X')[0]
        if np.intersect1d(toxic_loc,new_tox_loc).size:
            continue
        for i in range(len(new_tox_loc)):
            shuffle_board[new_tox_loc[i]],shuffle_board[toxic_loc[i]] = shuffle_board[toxic_loc[i]],shuffle_board[new_tox_loc[i]] 
        reshaped_board = np.reshape(shuffle_board.tolist(),(len(board_map),len(board_map[0])))
        list_of_starting_boards.append(reshaped_board.tolist())
        counter -= 1
        
    return list_of_starting_boards

def generate_mashed_maps(list_of_hill_climbs, elite_maps, normal_maps):
    
    new_maps_length = len(list_of_hill_climbs) - len(elite_maps)
        
    while len(normal_maps) != new_maps_length:
        normal_maps.append(random.choice(normal_maps))
    
    while len(elite_maps) != new_maps_length:
        elite_maps.append(random.choice(elite_maps))

    new_maps = []
    
    for i in range(len(elite_maps)):
        new_maps.append(proper_selection_approach(elite_maps[i],normal_maps[i]))
    
    
#    proper_selection_approach(elite_maps[1],normal_maps[1])
    return new_maps
    
def basic_selection_approach(elite_map,normal_map):
    
    flat_elite = np.array(elite_map).flatten()
    flat_normal = np.array(normal_map).flatten()
    
    flat_map_length = len(flat_elite)
    half_length = int(flat_map_length*0.5)
    new_map = []
    mashup_chooser = np.random.randint(2,size=1)

    if mashup_chooser == 1:
        for i in range(flat_map_length):
            if i<half_length:
                new_map.append(flat_elite[i])
            else:
                new_map.append(flat_normal[i])
    if mashup_chooser == 0:
        for i in range(flat_map_length):
            if i<half_length:
                new_map.append(flat_normal[i])
            else:
                new_map.append(flat_elite[i])    
    new_map = np.reshape(new_map,(len(elite_map),len(elite_map[0])))
    return new_map.tolist()

def proper_selection_approach(elite_map,normal_map):
    
    flat_elite = np.array(elite_map).flatten()
    flat_normal = np.array(normal_map).flatten()
    
#    flat_elite = np.array(['X' ,'R' ,'X' ,'I' ,'C' ,'1' ,'2' ,'R' ,'4', 'S', '5', 'I'])
#    flat_normal = np.array(['X', '5', 'X', '2' ,'I' ,'1', 'R', '4' ,'I' ,'S' ,'C' ,'R'])
    print(flat_elite)
    print('...')
    print(flat_normal)
    ct = 0
    if not intersect(flat_elite,'C',flat_normal,'R'):
        print('sth')
        if not intersect(flat_elite,'I',flat_normal,'R'):
            print('Put R of normal in elite')
            ct = 1
    if not intersect(flat_elite,'R',flat_normal,'C'):
        print('sth')
        if not intersect(flat_elite,'I',flat_normal,'C'):
            print('Put C of normal in elite')
            ct = 1
            
    if not intersect(flat_elite,'I',flat_normal,'C'):
        print('sth')
        if not intersect(flat_elite,'R',flat_normal,'C'):
            print('Put C of normal in elite')
            ct = 1
            
    if not intersect(flat_elite,'C',flat_normal,'I'):
        print('sth')
        if not intersect(flat_elite,'R',flat_normal,'I'):
            print('Put I of normal in elite')
            ct = 1
            
    if ct == 0:
        print('failed to find solution')            

def intersect(map1,K,map2,L):
    return np.intersect1d(np.where(map1 == K)[0],np.where(map2 == L)[0]).any()
    
    
    
        
        

