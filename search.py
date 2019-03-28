"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Acknowledgement: Search algorithms are referenced from AIMA provided code.
Source files can be found from <https://github.com/aimacode/aima-python>

Authors:
"""

import sys
import json
import math
import time

from chexersProblem import ChexersProblem
from state import State

from aima_python.search import astar_search

# -----------------------------------------------------------------------------

# String constants to avoid typos
COLOUR = "colour"
PIECES = "pieces"
BLOCKS = "blocks"
MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"

# The minimum and maximum coordinates on the q and r axes
MIN_COORDINATE = -3
MAX_COORDINATE = 3

# Total number of cells on the board
TOTAL_CELLS = 37

# -----------------------------------------------------------------------------


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # setup the initial state
    initial_state = setup_initial_state(data)

    # setup the goal state
    goal_state = setup_goal_state(initial_state)

    # Search for the goal node
    goal_node = astar_search(ChexersProblem(initial_state, goal_state,
                                            data[COLOUR]))

    print_actions(goal_node)

# -----------------------------------------------------------------------------


def setup_initial_state(data):
    """
    Initial state: a board_dict with pieces and blocks as specified.
    We use the following to indicate that state of a cell.
    - "": cell is not occupied;
    - "pieces": cell is occupied by a piece;
    - "blocks": cell is blocked.
    """
    initial_state = dict(zip(all_cells(), [""] * TOTAL_CELLS))
    for cell in data[PIECES]:
        initial_state[tuple(cell)] = data[COLOUR]
    for cell in data[BLOCKS]:
        initial_state[tuple(cell)] = BLOCKS
    return State(initial_state)


def all_cells():
    """
    generate the coordinates of all cells on the board.
    """
    ran = range(MIN_COORDINATE, MAX_COORDINATE + 1)
    return [(q, r) for q in ran for r in ran if -q-r in ran]


def setup_goal_state(initial_state):
    """
    Goal state: a board_dict with blocks but no pieces
    """
    goal_state = dict(initial_state)
    for cell, occupied in goal_state.items():
        if occupied != BLOCKS:
            goal_state[cell] = ""
    return State(goal_state)


def print_actions(goal_node):
    """
    Print the actions taken to reach the goal node in the specified format
    """

    for path in goal_node.path():
        action = path.action
        if not action:
            continue
        operator = action[0]
        if operator == EXIT:
            where_from = action[1]
            print("{} from {}.".format(operator, where_from))
        if operator == MOVE or operator == JUMP:
            where_from, where_to = action[1], action[2]
            print("{} from {} to {}.".format(operator, where_from, where_to))


# -----------------------------------------------------------------------------


def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a cellagonal board's contents.

    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as cellagonal coordinates (using
    the axial coordinate system outlined in the project specification) and the
    values are formatted as strings and placed in the drawing at the corres-
    ponding location (only the first 5 characters of each string are used, to
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates
    inside each cell, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}|
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}|
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}|
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}|
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}|
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}|
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} |
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    cells = []
    for qr in all_cells():
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("# --- %s seconds ---" % (time.time() - start_time))
