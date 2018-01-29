#!/usr/bin/env python3

import sys
import urban_planner_helpers

if __name__ == '__main__':

    # check to make sure a valid input path was given, exit otherwise
    if len(sys.argv) is 1:
        print("You must provide the path to the input text file")
        sys.exit(-1)

    pathToFile = sys.argv[1]

    (num_industrial, num_commercial, num_residential, board_map) = urban_planner_helpers.read_input_file(pathToFile)

    print(num_industrial)
    print(num_commercial)
    print(num_residential)
    print(board_map)

