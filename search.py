"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Acknowledgements: Algorithms were used directly from AIMA codes. Necessary
modification has been made for this project.

Authors:
"""

import sys
import json
import math

from collections import defaultdict as dd
from aima_python.search import (
    Problem, astar_search
)

TOTAL_HEXES = 37

# avoid typos
COLOUR = "colour"
PIECES = "pieces"
BLOCKS = "blocks"
MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"

MOVE_DELTA = [(0, 1), (1, 0), (-1, 1), (0, -1), (-1, 0), (1, -1)]
JUMP_DELTA = [(0, -2), (2, -2), (2, 0), (0, 2), (-2, 2), (-2, 0)]
EXIT_HEXES = {
    "red": [(3, -3), (3, -2), (3, -1), (3, 0)],
    "blue": [(0, -3), (-1, -2), (-2, -1), (-3, 0)],
    "green":[(-3, 3), (-2, 3), (-1, 3), (0, 3)]
}

def main():
    # initial state: a `board_dict` with pieces and blocks specified in the json file
    # actions: move, jump, exit
    # goal test: all pieces need to be in the exit hexes and exit

    # setup all 37 hexes
    hexes = [(0, 0)]
    for (x, y) in hexes:
        if len(set(hexes)) == TOTAL_HEXES:
            break
        hexes += [(x + delta_x, y + delta_y)
                    for delta_x, delta_y in MOVE_DELTA]

    # setup the initial state
    initial_state = dict(zip(set(hexes), [""] * TOTAL_HEXES))
    with open(sys.argv[1]) as file:
        data = json.load(file)

        exit_hexes = EXIT_HEXES[data[COLOUR]]
        for k in data:
            if k == COLOUR:
                continue
            for hex in data[k]:
                initial_state[tuple(hex)] = k

    # setup the goal state
    goal_state = initial_state.copy()
    for hex, occupied in goal_state.items():
        if occupied != BLOCKS:
            goal_state[hex] = ""
        elif hex in exit_hexes:
            exit_hexes.remove(hex)

    node = astar_search(ChexersProblem(initial_state, goal_state, exit_hexes))
    actions = []
    while node.state != initial_state:
        actions = [node.action] + actions
        node = node.parent

    for action in actions:
        operator = action[0]
        if operator == EXIT:
            where_from = action[1]
            print("{} from {}.".format(operator, where_from))
        if operator == MOVE or operator == JUMP:
            where_from, where_to = action[1], action[2]
            print("{} from {} to {}.".format(operator, where_from, where_to))


class ChexersProblem(Problem):
    def __init__(self, initial, goal, exit_hexes):
        self.exit_hexes = exit_hexes
        Problem.__init__(self, initial, goal)

    def pieces(self, state):
        return [hex for hex, occupied in state.items() if occupied == PIECES]

    """generate a list of six hexes by adding delta values"""
    def generate_hexes(self, hex, delta_pairs):
        return [
            (hex[0] + delta_x, hex[1] + delta_y)
            for delta_x, delta_y in delta_pairs
        ]

    def moveable_hexes(self, current_hex, state):
        neighbours = self.generate_hexes(current_hex, MOVE_DELTA)
        return [hex for hex in neighbours if hex in state and state[hex] == ""]

    def jumpable_hexes(self, current_hex, state):
        generated_hexes = self.generate_hexes(current_hex, JUMP_DELTA)
        jumpable = []
        for hex in generated_hexes:
            if hex in state:
                jumpover = tuple(map(lambda x, y: (x + y) // 2, current_hex, hex))
                if jumpover in state and state[jumpover] != "":
                    jumpable.append(hex)
        return jumpable

    def is_exitable(self, piece):
        if piece in self.exit_hexes:
            return True
        return False

    def actions(self, state):
        possible_actions = []
        for where_from in self.pieces(state):
            possible_actions += (
                [(MOVE, where_from, where_to) for where_to in self.moveable_hexes(where_from, state)] +
                [(JUMP, where_from, where_to) for where_to in self.jumpable_hexes(where_from, state)] +
                ([(EXIT, where_from)] if self.is_exitable(where_from) else [])
            )
        return possible_actions;

    def result(self, state, action):
        new_state = state.copy()
        operator = action[0]

        if operator == EXIT:
            where_from = action[1]
            new_state[where_from] = ""
        if operator == MOVE or operator == JUMP:
            where_from, where_to = action[1], action[2]
            [new_state[where_from], new_state[where_to]] = (
                [new_state[where_to], new_state[where_from]]
            )
        return new_state;

    def goal_test(self, state):
        return Problem.goal_test(self, state)

    def h(self, node):
        target_hexes = self.exit_hexes
        current_hexes = self.pieces(node.state)
        return sum(min([euclidean_distance(hex, target)
                for target in target_hexes]) for hex in current_hexes)

def euclidean_distance(x, y):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))

def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.

    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using
    the axial coordinate system outlined in the project specification) and the
    values are formatted as strings and placed in the drawing at the corres-
    ponding location (only the first 5 characters of each string are used, to
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates
    inside each hex, set this to `True` -- default `False`.
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
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
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
    main()
