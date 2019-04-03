from aima_python.search import Problem

from hexDistances import (
    getHexDistances, moveable_cells, jumpable_cells
)
from state import State

import math

# String constants to avoid typos
MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"

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
    def __init__(self, initial, goal, piece_colour, blocks):
        Problem.__init__(self, initial, goal)

        # the colour of our pieces
        self.piece_colour = piece_colour

        # Setup the exit cells for given colour with blocked cells removed
        self.exit_cells = (set(EXIT_CELLS[piece_colour]) -
                           set([tuple(block) for block in blocks]))

        self.hexDistances = getHexDistances(goal, self.exit_cells)

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
        new_state = dict(state)

        # update the new state by the action
        operator = action[0]
        # Exit action will result one piece disappear and leave the exit cell
        # empty
        if operator == EXIT:
            curr_cell = action[1]
            new_state[curr_cell] = ""
        # Move or jump action will exchange the states of two cells
        if operator == MOVE or operator == JUMP:
            curr_cell, next_cell = action[1], action[2]
            [new_state[curr_cell], new_state[next_cell]] = (
                [new_state[next_cell], new_state[curr_cell]])
        return State(new_state)

    def path_cost(self, c, state1, action, state2):
        return c + PATH_COSTS[action[0]]

    def h(self, node):
        target_cells = self.exit_cells
        piece_cells = self.get_pieces(node.state)
        # If there are no pieces, which means the node will reach the goal,
        # return the smallest heuristic of 0 in this case.
        if not piece_cells:
            return 0
        # Otherwise, the heuristic is the sum of [the average distance of each
        # piece to the exit cells + 1]. Plus 1 means that when each piece
        # reaches one of the exit cells, it still needs 1 step to exit the
        # board.
        # return sum(1 + avg([hex_distance(cell, target)
        #                 for target in target_cells]) for cell in piece_cells)

        rs = [(avg([hex_distance(cell, target) for target in target_cells]), cell) for cell in piece_cells]

        return sum(1 + self.hexDistances[cell] for r, cell in rs)


def avg(lst):
    return sum(lst) / len(lst)

# -----------------------------------------------------------------------------

def hex_distance(a, b):
    """
    Acknowledgement: This function was copied and reproduced from a JS version
    on redblobgames website, which can be found from
    <https://www.redblobgames.com/grids/cellagons/#distances-axial>

    Calculate the hex distance for axial coordinates system.
    """
    return (abs(a[0] - b[0])
          + abs(a[0] + a[1] - b[0] - b[1])
          + abs(a[1] - b[1])) / 2


def euclidean_distance(x, y):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
