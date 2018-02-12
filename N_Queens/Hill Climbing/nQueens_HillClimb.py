# Importing the helper functions

from nQueens import heuristic, try_placement
import random
from nQueens import initial_scene, create_scene
import time

def greedy_hillClimb(locations, N, visual):

    # Giving out an error with no solution availability for N<=3

    if N<=3:
        print ("No solution")
        # print (locations)
        return 0

    # Printing out the randomly generated start state for the problem
    start_state = [(locations[index]%N, index) for index in range(0,len(locations))]
    # print ("Start State", locations)
    print ("Start State", start_state)

    loc, attacks = heuristic(locations, N)
    current_minheuristic = 0

    # print ("Inital random scene", loc)
    moves, restarts, totalCost, numNodes = 0, 0, 0, 0

    while (True):

        # Trying to place the queens and extract the minimum heuristic configuration for the current board
        scene, scene_status = try_placement(loc, N)

        # print ("--------------------------------------")
        # print ("Initial Scene at this iteration", scene)
        # print ("Scene before update", loc)


        newscene_status = list(scene_status)

        # Sorting the scene based on heuristic values to get a scene the next move
        newscene_status.sort(key=lambda x: x[1])

        # Can print the values of the current scene - Positions  of the queens

        # for element in newscene_status:
        #     print (element)
        #     print (element[1])

        # Comparing the lowest heuristic of the current scene with minimum heuristic encountered so far
        previous_heuristic = current_minheuristic

        # Moving to a new scene
        move_to_scene = newscene_status[0]

        # Cost  of current move being added to the total path cost
        totalCost += move_to_scene[2]

        current_minheuristic = move_to_scene[1]

        # Terminating the process when the queens are finally placed in a manner that they face no attacks and the heuristic is 0
        if current_minheuristic==0:
            print ("Task achieved")
            print ("Final scene with queen placement", move_to_scene[0])
            print ("Final Heuristic value", move_to_scene[1])
            break

        # Making a random restart in case of a local maxima

        if current_minheuristic >= previous_heuristic:
            loc = [(random.randint(0,N-1), i)   for i in range(0,N)]
            # print ("New random setup", loc)
            restarts+=1
            totalCost=0
            moves = 0
        else:
            loc = list(move_to_scene[0])
            # print ("Updated Scene", move_to_scene)

        numNodes+=  N**2 - N
        moves+=1

        # Visualize each individual move
        # NOTE - The time delay would be reflected in the total run time

        # if visual==1:
        #     screen, white, red, black, pink, N, point_list, square_size = create_scene(N)
        #     _ = initial_scene(N, screen, point_list, square_size, red, move_to_scene[0])
        #     time.sleep(0.1)

        newscene_status = []

    branchingFactor = numNodes/moves
    print ("Total number of nodes expanded across all restarts", numNodes)
    print ("Effective branching factor", branchingFactor)
    print ("Total cost of movement", totalCost)
    print ("Total number of restarts", restarts)
    print ("Total number of moves taken", moves)


    # Visualize the final status of the queens placed at the positions that give an effective heuristic  of 0

    # NOTE -  The time delay will be reflected in the total time taken for the process

    if visual==1:
        screen, white, red, black, pink, N, point_list, square_size = create_scene(N)
        _ = initial_scene(N, screen, point_list, square_size, red, move_to_scene[0])                                         # screen, N, point_list, square_size, red)




