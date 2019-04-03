from aima_python.search import (Problem, uniform_cost_search)

from state import State
from utils import (
    PIECE, BLOCK, MOVE, JUMP, EXIT,
    all_cells, moveable_cells, jumpable_cells, print_board
)


def setup_approx_distances(curr_state):
    ApproxDistances.curr_board_dict = curr_state.board_dict.copy()


    curr_pieces = [cell for cell, occupied in
                        ApproxDistances.curr_board_dict.items()
                                if occupied and occupied != BLOCK]

    for starting_point in ApproxDistances.starting_points:
        ApproxDistances.distance_dict[starting_point] = 0
        board_dict = ApproxDistances.curr_board_dict.copy()
        board_dict[starting_point] = PIECE
        for piece in curr_pieces:
            board_dict[piece] = ""
            for other_piece in set(curr_pieces) - set([piece]):
                board_dict[other_piece] = BLOCK
            uniform_cost_search(ApproxDistances(State(board_dict)))

    return ApproxDistances.distance_dict

class ApproxDistances(Problem):
    """
    Compute minimum hex distances to any exit cells for each hex with
    detouring blocks by starting from exit cells and visiting each unoccupied
    hexes
    """

    starting_points = []
    curr_board_dict = {}

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
            for next_cell in jumpable_cells(curr_cell, state):
                possible_actions += [(JUMP, curr_cell, next_cell)]
        return possible_actions

    def result(self, state, action):
        board_dict = state.board_dict.copy()
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
        return [cell for cell, occupied in state.board_dict.items()
                                                    if occupied == PIECE]
