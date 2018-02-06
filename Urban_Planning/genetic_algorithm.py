import time
import urban_planner_helpers


def genetics(start_map, working_boards, number_zones, map_heuristics):
    score = 0
    timestamp = time.time()
    winning_map = start_map
    return score, timestamp, winning_map


def calculate_fitness(organism_map, maps_cost):
    score = 0

    residential_locations = urban_planner_helpers.find_this_landmarks(organism_map, 'R')
    commercial_locations = urban_planner_helpers.find_this_landmarks(organism_map, 'C')
    industrial_locations = urban_planner_helpers.find_this_landmarks(organism_map, 'I')

    res_cost, com_cost, ind_cost = maps_cost

    for zone in residential_locations:

        # TODO see if this check is even needed later on
        if res_cost[zone[1]][zone[0]] != 'X' and res_cost[zone[1]][zone[0]] != 'S':
            score += res_cost[zone[1]][zone[0]]

        surrounding_zone = urban_planner_helpers.find_list_of_points_manhattan_away(zone[0], zone[1], 3)
        for spot in surrounding_zone:
            x = spot[0]
            y = spot[1]
            map_val = organism_map[y][x]

            if map_val == 'R':
                score += 5
            elif map_val == 'I':
                score -= 5

    for zone in commercial_locations:

        # TODO see if this check is even needed later on
        if com_cost[zone[1]][zone[0]] != 'X' and com_cost[zone[1]][zone[0]] != 'S':
            score += com_cost[zone[1]][zone[0]]

        surrounding_zone = urban_planner_helpers.find_list_of_points_manhattan_away(zone[0], zone[1], 3)
        for spot in surrounding_zone:
            x = spot[0]
            y = spot[1]
            map_val = organism_map[y][x]

            if map_val == 'R':
                score += 5

        surrounding_zone = urban_planner_helpers.find_list_of_points_manhattan_away(zone[0], zone[1], 2)
        for spot in surrounding_zone:
            x = spot[0]
            y = spot[1]
            map_val = organism_map[y][x]

            if map_val == 'C':
                score -= 5

    for zone in industrial_locations:

        # TODO see if this check is even needed later on
        if ind_cost[zone[1]][zone[0]] != 'X' and ind_cost[zone[1]][zone[0]] != 'S':
            score += ind_cost[zone[1]][zone[0]]

        surrounding_zone = urban_planner_helpers.find_list_of_points_manhattan_away(zone[0], zone[1], 2)
        for spot in surrounding_zone:
            x = spot[0]
            y = spot[1]
            map_val = organism_map[y][x]

            if map_val == 'I':
                score += 3

    return score