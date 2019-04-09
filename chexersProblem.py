from aima_python.problem import Problem

from approxDistances import get_approx_distances
from state import State
from utils import (
    COLOUR, PIECES, BLOCKS, BLOCK, MOVE, JUMP, EXIT, EMPTY_CELL,
    all_cells, moveable_cells, jumpable_cells, hex_distance, print_board
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

        self.distance_dict = get_approx_distances(goal_state, self.exit_cells)

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
        return [cell for cell, occupied in state.items()
                                    if occupied == self.piece_colour]

    def result(self, state, action):
        board_dict = dict(state)

        # update the new state by the action
        operator = action[0]

        # Exit action will result one piece disappear and leave the exit cell
        # empty
        if operator == EXIT:
            curr_cell = action[1]
            board_dict[curr_cell] = EMPTY_CELL
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

        return sum([1 + self.distance_dict[cell] for cell in piece_cells])


def setup_initial_state(data):
    """
    Initial state:
    """
    board_dict = dict(zip(all_cells(), [EMPTY_CELL] * TOTAL_CELLS))
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
    board_dict = dict(initial_state)
    for cell, occupied in board_dict.items():
        if occupied != BLOCK:
            board_dict[cell] = EMPTY_CELL
    return State(board_dict)
