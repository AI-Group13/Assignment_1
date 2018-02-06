from nQueens import heuristic, try_placement
import random
from nQueens import initial_scene, create_scene
import time

def greedy_hillClimb(locations, N):

    if N<=3:
        print ("No solution")
        # print (locations)
        return 0

    loc, attacks = heuristic(locations, N)
    current_minheuristic = 0

    # print ("Inital random scene", loc)

    p, r = 0, 0

    while (True):

        scene, scene_status = try_placement(loc, N)

        # print ("--------------------------------------")
        # print ("Initial Scene at this iteration", scene)
        # print ("Scene before update", loc)

        newscene_status = list(scene_status)
        newscene_status.sort(key=lambda x: x[1])

        # for element in newscene_status:
        #     print (element)
        #     print (element[1])

        previous_heuristic = current_minheuristic
        move_to_scene = newscene_status[0]
        current_minheuristic = move_to_scene[1]

        if current_minheuristic==0:
            print ("Task achieved")
            print (move_to_scene)
            break

        if current_minheuristic >= previous_heuristic:
            loc = [(random.randint(0,N-1), i)   for i in range(0,N)]
            # print ("New random setup", loc)
            r+=1
        else:
            loc = list(move_to_scene[0])
            # print ("Updated Scene", move_to_scene)

        # print ("----------")
        # print (move_to_scene)
        # print (currentScene)
        # print ("-------------")
        # print (scene_status)
        # print ("-------------")
        # print (scene)

        p+=1

        # screen, white, red, black, pink, N, point_list, square_size = create_scene(N)
        # _ = initial_scene(N, screen, point_list, square_size, red, move_to_scene[0])

    print ("Total number of restarts", r)
    print ("Total number of moves taken", p)

    screen, white, red, black, pink, N, point_list, square_size = create_scene(N)
    _ = initial_scene(N, screen, point_list, square_size, red, move_to_scene[0])                                         # screen, N, point_list, square_size, red)
    # time.sleep(50)


