from aima_python.search import (Problem, uniform_cost_search)
from state import State

# String constants to avoid typos
PIECE = "piece"
MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"

# Delta values which give the corresponding cells by adding them to the current
# cell
MOVE_DELTA = [(0, 1), (1, 0), (-1, 1), (0, -1), (-1, 0), (1, -1)]
JUMP_DELTA = [(0, -2), (2, -2), (2, 0), (0, 2), (-2, 2), (-2, 0)]

def getHexDistances(board, exit_cells):
    HexDistances.board = board

    for exit_cell in exit_cells:
        uniform_cost_search(HexDistances(exit_cell))

    # print_board(HexDistances.dict, "", True)
    return HexDistances.dict


class HexDistances(Problem):
    """
    Compute minimum hex distances to any exit cells for each hex with
    detouring blocks by starting from exit cells and visiting each unoccupied
    hexes
    """

    # key: hex, value: distance
    dict = {}

    def __init__(self, piece):
        super().__init__(self.setup_initial_state(piece))
        HexDistances.dict[piece] = 1

    def setup_initial_state(self, piece):
        initial_state = HexDistances.board.copy()
        initial_state[piece] = PIECE
        return State(initial_state)

    def actions(self, state):
        """
        Possible actions include move, jump
        """
        possible_actions = []
        for curr_cell in self.get_pieces(state):
            # Move actions
            for next_cell in moveable_cells(curr_cell, state):
                possible_actions += [(MOVE, curr_cell, next_cell)]
            # Jump actions
            for next_cell in jumpable_cells(curr_cell, state):
                possible_actions += [(JUMP, curr_cell, next_cell)]
        return possible_actions

    def result(self, state, action):
        new_state = dict(state)
        curr_cell, next_cell = action[1], action[2]
        [new_state[curr_cell], new_state[next_cell]] = (
            [new_state[next_cell], new_state[curr_cell]])
        return State(new_state)

    def path_cost(self, c, state1, action, state2):
        next_cell = action[2]
        cost = c + 1
        if (not next_cell in HexDistances.dict) or HexDistances.dict[next_cell] > cost:
            HexDistances.dict[next_cell] = cost
        return cost

    def get_pieces(self, state):
        """
        Return cells of pieces in current state
        """
        return [cell for cell, occupied in state.items() if occupied == PIECE]


def generate_cells(cell, delta_pairs):
    """
    generate a list of six cells by adding delta values
    """
    return [(cell[0] + delta_q, cell[1] + delta_r)
            for delta_q, delta_r in delta_pairs]


def moveable_cells(current_cell, state):
    """
    moveable_cells are cells next to the current_cell with nothing occupied
    """
    neighbours = generate_cells(current_cell, MOVE_DELTA)
    return [cell for cell in neighbours if cell in state and state[cell] == ""]

def jumpable_cells(current_cell, state):
    """
    jumpable_cells are cells that are one cell apart from the current cell
    and cells in the middle must be occupied by either blocks or pieces
    """
    generated_cells = generate_cells(current_cell, JUMP_DELTA)
    jumpable = []
    for cell in generated_cells:
        if cell in state and state[cell] == "":
            jumpover = tuple(map(lambda x, y: (x + y) // 2, current_cell,
                                 cell))
            if jumpover in state and state[jumpover] != "":
                jumpable.append(cell)
    return jumpable


MIN_COORDINATE = -3
MAX_COORDINATE = 3

def all_cells():
    """
    generate the coordinates of all cells on the board.
    """
    ran = range(MIN_COORDINATE, MAX_COORDINATE + 1)
    return [(q, r) for q in ran for r in ran if -q-r in ran]

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
