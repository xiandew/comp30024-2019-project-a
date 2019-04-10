from aima_python.problem import Problem
from aima_python.search import uniform_cost_search
from utils import (
    JUMP_DELTA, ALL_CELLS, moveable_cells, generate_cells, print_board
)

# ______________________________________________________________________________

def get_approx_path_costs(exit_cells, blocks):

    ApproxPathCosts.blocks = blocks

    for cell in exit_cells:
        ApproxPathCosts.path_costs[cell] = 0
        uniform_cost_search(ApproxPathCosts(cell))

    print_board(ApproxPathCosts.path_costs)

    return ApproxPathCosts.path_costs

# ______________________________________________________________________________

class ApproxPathCosts(Problem):
    """
    Compute minimum path costs to one of the exit cells for each hex by
    implementing dijkstra search from exit cells one by one.
    These path costs are said to be approximate since jumping actions are
    relaxed for optimality.
    A jumping action is allowed as long as the jumping cell is not blocked
    regardless whether there is an occupied hex as a pivot or not.
    Note that these path costs do not count the exit actions.
    """

    blocks = []

    # key: cell, value: approximate minimum distance to closest exit cell
    path_costs = {}

    def __init__(self, piece):
        super().__init__(piece)

    def actions(self, piece):
        """
        Possible actions include move and relaxed jump actions
        """
        return [(piece, next_cell) for next_cell in
                    ( moveable_cells(piece, ApproxPathCosts.blocks) +
                        relaxed_jumpable_cells(piece, ApproxPathCosts.blocks) )]

    def result(self, piece, action):
        return action[1]

    def path_cost(self, c, state1, action, state2):
        new_cost = c + 1
        next_cell = action[1]
        if ( next_cell not in ApproxPathCosts.path_costs or
                    new_cost < ApproxPathCosts.path_costs[next_cell] ):
            ApproxPathCosts.path_costs[next_cell] = new_cost
        return new_cost

# ______________________________________________________________________________

def relaxed_jumpable_cells(curr_cell, blocks):
    """
    Return all cells that are in the jumping range of current cell and not
    blocked
    """
    return [cell for cell in generate_cells(curr_cell, JUMP_DELTA)
                                if cell in ALL_CELLS and cell not in blocks]
