"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Acknowledgement: Search algorithms are referenced from AIMA provided code.
Source files can be found from <https://github.com/aimacode/aima-python>

Authors:
    Mingyu Su, 912464
    Xiande Wen, 905003
"""

import sys
import json
import time

from aima_python.search import astar_search
from chexersProblem import ChexersProblem

# ______________________________________________________________________________

# String constants to avoid typos
MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # Search for the goal node
    goal_node = astar_search(ChexersProblem(data))

    print_actions(goal_node)

    print("# {} moves".format(len(goal_node.solution())))


def print_actions(goal_node):
    """
    Print the actions taken to reach the goal node in the specified format
    """

    for action in goal_node.solution():
        operator = action[0]
        if operator == EXIT:
            curr_cell = action[1]
            print("{} from {}.".format(operator, curr_cell))
        if operator == MOVE or operator == JUMP:
            curr_cell, next_cell = action[1], action[2]
            print("{} from {} to {}.".format(operator, curr_cell, next_cell))

# ______________________________________________________________________________


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("# --- %s seconds ---" % (time.time() - start_time))
