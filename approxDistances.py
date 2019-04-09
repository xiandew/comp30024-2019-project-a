from aima_python.problem import Problem
from aima_python.search import uniform_cost_search

from state import State
from utils import (
    PIECE, BLOCK, MOVE, JUMP, EXIT, EMPTY_CELL, JUMP_DELTA, generate_cells,
    all_cells, moveable_cells, jumpable_cells, avg, print_board
)

def get_approx_distances(curr_state, exit_cells):

    for cell in exit_cells:
        board_dict = dict(curr_state)
        board_dict[cell] = PIECE
        ApproxDistances.distance_dict[cell] = 0
        uniform_cost_search(ApproxDistances(State(board_dict)))

    print_board(ApproxDistances.distance_dict)

    return ApproxDistances.distance_dict

class ApproxDistances(Problem):
    """
    Compute minimum hex distances to any exit cells for each hex with
    detouring blocks by starting from exit cells and visiting each unoccupied
    hexes
    """

    # key: cell, value: approximate minimum distance to closest exit cell
    distance_dict = {}

    def __init__(self, initial):
        super().__init__(initial)

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
            for next_cell in relaxed_jumpable_cells(curr_cell, state):
                possible_actions += [(JUMP, curr_cell, next_cell)]
        return possible_actions

    def result(self, state, action):
        board_dict = dict(state)
        curr_cell, next_cell = action[1], action[2]
        [board_dict[curr_cell], board_dict[next_cell]] = (
                    [board_dict[next_cell], board_dict[curr_cell]] )
        return State(board_dict)

    def path_cost(self, c, state1, action, state2):
        cost = c + 1
        next_cell = action[2]
        if ( (not next_cell in ApproxDistances.distance_dict) or
                    ApproxDistances.distance_dict[next_cell] > cost ):
            ApproxDistances.distance_dict[next_cell] = cost
        return cost

    def get_pieces(self, state):
        """
        Return cells of pieces in current state
        """
        return [cell for cell, occupied in state.items()
                                                    if occupied == PIECE]


def relaxed_jumpable_cells(curr_cell, state):
    """
    """
    return [cell for cell in generate_cells(curr_cell, JUMP_DELTA)
                            if cell in state and state[cell] == EMPTY_CELL]
