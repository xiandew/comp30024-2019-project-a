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


from aima_python.search import (
    Problem, astar_search
)

# -------------------------------------------------------------------------------

# String constants to avoid typos
COLOUR = "colour"
PIECES = "pieces"
BLOCKS = "blocks"
MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"

# Delta values which give the corresponding cells by adding them to the current cell
MOVE_DELTA = [(0, 1), (1, 0), (-1, 1), (0, -1), (-1, 0), (1, -1)]
JUMP_DELTA = [(0, -2), (2, -2), (2, 0), (0, 2), (-2, 2), (-2, 0)]

# The exit cells for pieces of each colour
EXIT_CELLS = {
    "red": [(3, -3), (3, -2), (3, -1), (3, 0)],
    "blue": [(0, -3), (-1, -2), (-2, -1), (-3, 0)],
    "green":[(-3, 3), (-2, 3), (-1, 3), (0, 3)]
}

# Total number of cells on the board
TOTAL_CELLS = 37

# -------------------------------------------------------------------------------


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # setup the initial state
    initial_state = setup_initial_state(data)

    # setup the goal state
    goal_state = setup_goal_state(initial_state)

    # setup the exit cells for given colour with blocked cells removed
    exit_cells = set(EXIT_CELLS[piece_colour]) - set([tuple(cell) for cell in data[BLOCKS]])

    # Search for the goal node
    goal_node = astar_search(ChexersProblem(initial_state, goal_state, exit_cells))

    print_actions(goal_node, initial_state)

# -------------------------------------------------------------------------------


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
        initial_state[tuple(cell)] = PIECES
    for cell in data[BLOCKS]:
        initial_state[tuple(cell)] = BLOCKS
    return State(initial_state)


def all_cells():
    """
    generate the coordinates of all cells on the board.
    """
    cells = [(0, 0)]
    for (q, r) in cells:
        cells += [(q + delta_q, r + delta_r) for delta_q, delta_r in MOVE_DELTA]
        if len(set(cells)) == TOTAL_CELLS:
            break
    return set(cells)


def setup_goal_state(initial_state):
    """
    Goal state: a board_dict with blocks but no pieces
    """
    goal_state = dict(initial_state)
    for cell, occupied in goal_state.items():
        if occupied != BLOCKS:
            goal_state[cell] = ""
    return State(goal_state)


def print_actions(goal_node, initial_state):
    """
    Retrieve the actions taken to reach the goal node and print them
    in the specified format
    """
    actions = []
    node = goal_node
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

# -------------------------------------------------------------------------------


class State(dict):
    """
    State class inherits from built-in dict. Make it immutable, hashable and
    comparable for compatible with the referenced search algorithms from AIMA.

    It is used to store a state of the board which is defined by all cells on
    the board and their corresponding states (whether the cell is empty, blocked
    or occupied by a piece).

    Acknowledgement: This code is referenced from official python developer's
    guide <https://www.python.org/dev/peps/pep-0351/#sample-implementations>
    """

    def _immutable(self, *args, **kws):
        raise TypeError('state is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear       = _immutable
    update      = _immutable
    setdefault  = _immutable
    pop         = _immutable
    popitem     = _immutable

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return str(self) < str(other)

# -------------------------------------------------------------------------------


class ChexersProblem(Problem):
    """
    ChexersProblem class for the project. Inherits from Problem and abstract
    methods were implemented by formulating the chexers.
    """
    def __init__(self, initial, goal, exit_cells):
        self.exit_cells = exit_cells
        Problem.__init__(self, initial, goal)

    def moveable_cells(self, current_cell, state):
        """
        moveable_cells are cells next to the current_cell with nothing occupied
        """
        neighbours = generate_cells(current_cell, MOVE_DELTA)
        return [cell for cell in neighbours if cell in state and state[cell] == ""]

    def jumpable_cells(self, current_cell, state):
        generated_cells = generate_cells(current_cell, JUMP_DELTA)
        jumpable = []
        for cell in generated_cells:
            if cell in state and state[cell] == "":
                jumpover = tuple(map(lambda x, y: (x + y) // 2, current_cell, cell))
                if jumpover in state and state[jumpover] != "":
                    jumpable.append(cell)
        return jumpable

    def is_exitable(self, piece):
        if piece in self.exit_cells:
            return True
        return False

    def actions(self, state):
        """
        Possible actions include move, jump and exit.
        """
        possible_actions = []
        for where_from in get_pieces(state):
            possible_actions += (
                [(MOVE, where_from, where_to)
                    for where_to in self.moveable_cells(where_from, state)]
              + [(JUMP, where_from, where_to)
                    for where_to in self.jumpable_cells(where_from, state)]
              + ([(EXIT, where_from)]
                    if self.is_exitable(where_from) else [])
            )
        return possible_actions;

    def result(self, state, action):
        new_state = dict(state)

        # update the new state by the action
        operator = action[0]
        if operator == EXIT:
            where_from = action[1]
            new_state[where_from] = ""
        if operator == MOVE or operator == JUMP:
            where_from, where_to = action[1], action[2]
            [new_state[where_from], new_state[where_to]] = (
                [new_state[where_to], new_state[where_from]]
            )
        return State(new_state);

    def goal_test(self, state):
        return Problem.goal_test(self, state)

    def h(self, node):
        target_cells = self.exit_cells
        piece_cells = get_pieces(node.state)
        # If the node will reach the goal, return the smallest heuristic of 0
        if piece_cells == []:
            return 0
        # Plus 1 to ensure the optimal state is always the state with no pieces
        return 1 + sum(min([hex_distance(cell, target)
                for target in target_cells]) for cell in piece_cells)


def get_pieces(state):
    return [cell for cell, occupied in state.items() if occupied == PIECES]


def generate_cells(cell, delta_pairs):
    """
    generate a list of six cells by adding delta values
    """
    return [(cell[0] + delta_q, cell[1] + delta_r)
                for delta_q, delta_r in delta_pairs]

# -------------------------------------------------------------------------------


def hex_distance(a, b):
    """
    Acknowledgement: This function was copied and reproduced from a JS version
    on redblobgames website, which can be found from
    <https://www.redblobgames.com/grids/cellagons/#distances-axial>

    Calculate the cell distance for axial coordinates system.
    """
    return (abs(a[0] - b[0])
          + abs(a[0] + a[1] - b[0] - b[1])
          + abs(a[1] - b[1])) / 2


def euclidean_distance(x, y):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))

# -------------------------------------------------------------------------------


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
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q, r) for q in ran for r in ran if -q-r in ran]:
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
