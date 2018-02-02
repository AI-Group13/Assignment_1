import time
import urban_planner_helpers

def hillclimb(start_map, working_boards, number_zones, map_heuristics):

    score = 0
    timestamp = time.time()
    winning_map = start_map
    return score, timestamp, winning_map
