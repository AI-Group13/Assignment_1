# Module: urban_planner_helpers
import numpy as np
import random
from itertools import permutations
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

def cross_over(list_of_hill_climbs, elite_maps, normal_maps):
    
    new_maps_length = len(list_of_hill_climbs) - len(elite_maps)
    expanded_elites, expanded_normals = list(elite_maps),list(normal_maps)
    while len(expanded_normals) != new_maps_length:
        expanded_normals.append(random.choice(expanded_normals))
    
    while len(expanded_elites) != new_maps_length:
        expanded_elites.append(random.choice(expanded_elites))
    
    new_maps = []
    
    for i in range(len(expanded_elites)):
        flat_elite = np.array(expanded_elites[i]).flatten()
        flat_normal = np.array(expanded_normals[i]).flatten()
        
        ct = 0
        L1 = ['C','R','I','C','R','I']
        L2 = ['R','C','C','I','I','R']
        L3 = ['I','I','R','R','C','C']
        
        p = list(permutations(['I','R','C']))
        
        while(ct==0):

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
                if not intersect(flat_elite,x[0],flat_normal,x[1]):
                    if not intersect(flat_elite,x[2],flat_normal,x[1]):
                        flat_elite[np.where(flat_elite == x[1])] = 0
                        flat_elite[np.where(flat_normal == x[1])] = x[1]
#                        print('Swapped')
                        ct = 1
    
            if ct == 0:
#                print('Mutated')
                flat_normal = mutate(flat_normal)
        flat_elite = np.reshape(flat_elite.tolist(),(len(expanded_elites[i]),len(expanded_elites[i][0])))
        new_maps.append(flat_elite)

    return new_maps        


def intersect(map1,K,map2,L):
    return np.intersect1d(np.where(map1 == K)[0],np.where(map2 == L)[0]).any()


def mutate(input_map):
    input_map = np.array(input_map).flatten()
    vals_to_avoid = np.concatenate((np.where(input_map == 'X')[0],np.where(input_map == 'S')[0]))
    all_vals = [i for i in range(len(input_map))]
    vals_to_move = list(set(all_vals) - set(vals_to_avoid.tolist()))
    (r1,r2) = (np.random.choice(vals_to_move),np.random.choice(vals_to_move))
    input_map[r1],input_map[r2] = input_map[r2],input_map[r1]
    return input_map


def Add_zones(Empty_map,Res_zones,Ind_zones,Com_zones):
    Zoned_map = np.array(Empty_map).flatten()
    vals_to_avoid = np.concatenate((np.where(Zoned_map == 'X')[0],np.where(Zoned_map == 'S')[0]))
    all_vals = [i for i in range(len(Zoned_map))]
    vals_to_change = list(set(all_vals) - set(vals_to_avoid.tolist()))
    if Res_zones + Ind_zones + Com_zones <= len(vals_to_change):
        zone_list = ['R' for i in range(Res_zones)] + ['I' for i in range(Ind_zones)] + ['C' for i in range(Com_zones)]
        np.random.shuffle(vals_to_change)
        vals_to_change = vals_to_change[:len(zone_list)]
        Zoned_map[vals_to_change] = [zone_list]
        return np.reshape(Zoned_map.tolist(),(len(Empty_map),len(Empty_map[0])))
    else:
        print('Invalid number of zones')
    
def shift_zone(input_map):
    ip_map = np.array(input_map).flatten()
    shift_map = ip_map.copy()
    vals_to_avoid = np.concatenate((np.where(ip_map == 'X')[0],np.where(ip_map == 'S')[0]))
    all_vals = [i for i in range(len(ip_map))]
    vals_to_change = list(set(all_vals) - set(vals_to_avoid.tolist()))
    val_other_zones = np.concatenate((np.where(ip_map == 'C')[0],np.where(ip_map == 'R')[0],np.where(ip_map == 'I')[0])).tolist()
    val_without_zones = list(set(vals_to_change) - set(val_other_zones))
    scores = []
    zones = ['R','I','C']
    for x in range(3):
        val_zone = np.where(ip_map == zones[x])[0].tolist()
        for i in range(len(val_zone)):
            shift_map[val_zone[i]] = 0
            for j in range(len(val_without_zones)):
                shift_map[val_without_zones[j]] = zones[x]
    #            print(np.reshape(shift_map.tolist(),(len(input_map),len(input_map[0]))))
#                print(shift_map)
                ''' put score function here'''
                score = np.random.randint(-20,50,1)
                zipped = np.append(shift_map,score)
    #            print(zipped)
                scores.append(zipped)
                shift_map[val_without_zones[j]] = 0
            shift_map[val_zone[i]] = zones[x]
    return scores
        