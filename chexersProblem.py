from aima_python.problem import Problem
from approxPathCosts import get_approx_path_costs
from utils import (
    COLOUR, PIECES, BLOCKS, MOVE, JUMP, EXIT, ALL_CELLS,
    moveable_cells, jumpable_cells, print_board
)

# ______________________________________________________________________________
# The exit cells for pieces of each colour
EXIT_CELLS = {
    "red": [(3, -3), (3, -2), (3, -1), (3, 0)],
    "blue": [(0, -3), (-1, -2), (-2, -1), (-3, 0)],
    "green": [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
}

# ______________________________________________________________________________

class ChexersProblem(Problem):
    """
    ChexersProblem class for the project. Inherits from Problem.
    Methods were implemented by formulating the chexers problem.
    """
    def __init__(self, data):
        # the colour of the pieces
        self.blocks = [tuple(block) for block in data[BLOCKS]]

        # Setup the exit cells for given colour with blocked cells removed
        self.exit_cells = set(EXIT_CELLS[data[COLOUR]]) - set(self.blocks)

        # Our state is a tuple containing the current cells of the pieces
        # Setup the initial state.
        initial_state = tuple(sorted([tuple(cell) for cell in data[PIECES]]))
        # print_initial_state(data)

        # Setup the goal state. The goal state is to move all pieces
        # off the board.
        goal_state = tuple()

        self.distance_dict = get_approx_path_costs(self.exit_cells, self.blocks)

        super().__init__(initial_state, goal_state)

    def actions(self, state):
        """
        Possible actions include move, jump and exit.
        """
        occupied = list(state) + self.blocks
        possible_actions = []

        for curr_cell in state:

            # Move actions
            for next_cell in moveable_cells(curr_cell, occupied):
                possible_actions += [(MOVE, curr_cell, next_cell)]

            # Jump actions
            for next_cell in jumpable_cells(curr_cell, occupied):
                possible_actions += [(JUMP, curr_cell, next_cell)]

            # Exit actions
            if curr_cell in self.exit_cells:
                possible_actions += [(EXIT, curr_cell)]

        return possible_actions

    def result(self, state, action):
        pieces = list(state)

        # update the new state by the action
        operator = action[0]

        # Exit action will result one piece disappear and leave the exit cell
        # empty
        if operator == EXIT:
            curr_cell = action[1]
            pieces.remove(curr_cell)

        # Move or jump action will exchange the states of two cells
        if operator == MOVE or operator == JUMP:
            curr_cell, next_cell = action[1], action[2]
            pieces.remove(curr_cell)
            pieces.append(next_cell)

        return tuple(sorted(pieces))

    def h(self, node):
        piece_cells = node.state
        # If there are no pieces, which means the node will reach the goal,
        # return the smallest heuristic of 0 in this case.
        if not piece_cells:
            return 0

        # Otherwise, the heuristic is the sum of [approximate path cost of
        # each piece + 1]. Plus 1 represents the exit action since the
        # approximate path costs did not count the exit action.
        return sum([1 + self.distance_dict[cell] for cell in piece_cells])


def print_initial_state(data):

    board_dict = dict(zip(ALL_CELLS, [""] * len(ALL_CELLS)))
    for cell in data[PIECES]:
        board_dict[tuple(cell)] = data[COLOUR]
    for cell in data[BLOCKS]:
        board_dict[tuple(cell)] = "BLOCK"

    print_board(board_dict, "", True)
