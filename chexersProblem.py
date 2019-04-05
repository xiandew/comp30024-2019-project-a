from aima_python.search import Problem

from approxDistances import (ApproxDistances, get_approx_distances)
from state import State
from utils import (
    COLOUR, PIECES, BLOCKS, BLOCK, MOVE, JUMP, EXIT,
    all_cells, moveable_cells, jumpable_cells, hex_distance, avg, middle_piece, print_board
)

import math

# Total number of cells on the board
TOTAL_CELLS = 37

# The exit cells for pieces of each colour
EXIT_CELLS = {
    "red": [(3, -3), (3, -2), (3, -1), (3, 0)],
    "blue": [(0, -3), (-1, -2), (-2, -1), (-3, 0)],
    "green": [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
}

# Path costs of three actions, which will set the algorithm's preference of
# each action
PATH_COSTS = {
    MOVE: 2,
    JUMP: 1,
    EXIT: 0
}

class ChexersProblem(Problem):
    """
    ChexersProblem class for the project. Inherits from Problem.
    Methods were implemented by formulating the chexers problem.
    """
    def __init__(self, data):
        # the colour of the pieces
        self.piece_colour = data[COLOUR]

        # Setup the exit cells for given colour with blocked cells removed
        self.exit_cells = (set(EXIT_CELLS[self.piece_colour]) -
                                set([tuple(block) for block in data[BLOCKS]]))

        # setup the initial state
        initial_state = setup_initial_state(data)

        # setup the goal state
        goal_state = setup_goal_state(initial_state)

        super().__init__(initial_state, goal_state)

    def is_exitable(self, piece):
        if piece in self.exit_cells:
            return True
        return False

    def actions(self, state):
        """
        Possible actions include move, jump and exit.
        """
        possible_actions = []
        for curr_cell in self.get_pieces(state):
            # Move actions
            for next_cell in moveable_cells(curr_cell, state):
                possible_actions += [(MOVE, curr_cell, next_cell)]
            # Jump actions
            for next_cell in jumpable_cells(curr_cell, state):
                possible_actions += [(JUMP, curr_cell, next_cell)]
            # Exit actions
            if self.is_exitable(curr_cell):
                possible_actions += [(EXIT, curr_cell)]
        return possible_actions

    def get_pieces(self, state):
        """
        Return cells of pieces in current state
        """
        return [cell for cell, occupied in state.board_dict.items()
                                    if occupied == self.piece_colour]

    def result(self, state, action):
        board_dict = state.board_dict.copy()

        # update the new state by the action
        operator = action[0]

        # Exit action will result one piece disappear and leave the exit cell
        # empty
        if operator == EXIT:
            curr_cell = action[1]
            board_dict[curr_cell] = ""
        # Move or jump action will exchange the states of two cells
        if operator == MOVE or operator == JUMP:
            curr_cell, next_cell = action[1], action[2]
            [board_dict[curr_cell], board_dict[next_cell]] = (
                        [board_dict[next_cell], board_dict[curr_cell]])

        # print_board(board_dict)
        return State(board_dict)

    # def path_cost(self, c, state1, action, state2):
    #     return c + PATH_COSTS[action[0]]

    def h(self, node):
        piece_cells = self.get_pieces(node.state)
        # If there are no pieces, which means the node will reach the goal,
        # return the smallest heuristic of 0 in this case.
        if not piece_cells:
            return 0

        # Otherwise, the heuristic is the sum of [... + 1]. Plus 1 means that when each piece
        # reaches one of the exit cells, it still needs 1 step to exit the
        # board.

        # distances = get_approx_distances(node.state, self.exit_cells)
        # return sum([1 + avg(d) for d in distances])

        return sum(1 + avg([hex_distance(cell, target)
                        for target in self.exit_cells]) for cell in piece_cells)


def setup_initial_state(data):
    """
    Initial state:
    """
    board_dict = dict(zip(all_cells(), [""] * TOTAL_CELLS))
    for cell in data[PIECES]:
        board_dict[tuple(cell)] = data[COLOUR]
    for cell in data[BLOCKS]:
        board_dict[tuple(cell)] = BLOCK

    print_board(board_dict, "", True)

    return State(board_dict)


def setup_goal_state(initial_state):
    """
    Goal state:
    """
    board_dict = initial_state.board_dict.copy()
    for cell, occupied in board_dict.items():
        if occupied != BLOCK:
            board_dict[cell] = ""
    return State(board_dict)

# -----------------------------------------------------------------------------


def get_nblocks(a, b, board_dict):
    d = hex_distance(a, b)
    if not d:
        return 0
    nblocks = 0
    for i in range(0, int(d)+1):
        if board_dict[cube_to_axial(cube_round(cube_lerp(a, b, 1.0/d * i)))] == BLOCK:
            nblocks += 1
    return nblocks

def lerp(a, b, t): # for floats
    return a + (b - a) * t

def cube_lerp(a, b, t): # for hexes
    ax, ay, az = axial_to_cube(a)
    bx, by, bz = axial_to_cube(b)
    return (lerp(ax, bx, t),
            lerp(ay, by, t),
            lerp(az, bz, t))

def cube_to_axial(cube):
    return (cube[0], cube[2])

def axial_to_cube(hex):
    x, z = hex
    return (x, -x-z, z)

def cube_round(cube):
    x, y, z = cube
    rx = round(x)
    ry = round(y)
    rz = round(z)

    x_diff = abs(rx - x)
    y_diff = abs(ry - y)
    z_diff = abs(rz - z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry-rz
    elif y_diff > z_diff:
        ry = -rx-rz
    else:
        rz = -rx-ry

    return (rx, ry, rz)
