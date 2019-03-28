from aima_python.search import Problem
from state import State

# String constants to avoid typos
BLOCKS = "blocks"
MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"

# Delta values which give the corresponding cells by adding them to the current
# cell
MOVE_DELTA = [(0, 1), (1, 0), (-1, 1), (0, -1), (-1, 0), (1, -1)]
JUMP_DELTA = [(0, -2), (2, -2), (2, 0), (0, 2), (-2, 2), (-2, 0)]

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
    ChexersProblem class for the project. Inherits from Problem and abstract
    methods were implemented by formulating the chexers.
    """
    def __init__(self, initial, goal, piece_colour):
        Problem.__init__(self, initial, goal)

        # the colour of our pieces
        self.piece_colour = piece_colour

        # Setup the exit cells for given colour with blocked cells removed
        self.exit_cells = (set(EXIT_CELLS[self.piece_colour]) -
                            set([cell for cell, occupied in self.goal.items()
                                            if occupied == BLOCKS]))

    def is_exitable(self, piece):
        if piece in self.exit_cells:
            return True
        return False

    def actions(self, state):
        """
        Possible actions include move, jump and exit.
        """
        possible_actions = []
        for where_from in self.get_pieces(state):
            possible_actions += (
                [(MOVE, where_from, where_to)
                    for where_to in moveable_cells(where_from, state)]
              + [(JUMP, where_from, where_to)
                    for where_to in jumpable_cells(where_from, state)]
              + ([(EXIT, where_from)]
                    if self.is_exitable(where_from) else [])
            )
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
            where_from = action[1]
            new_state[where_from] = ""
        # Move or jump action will exchange the states of two cells
        if operator == MOVE or operator == JUMP:
            where_from, where_to = action[1], action[2]
            [new_state[where_from], new_state[where_to]] = (
                [new_state[where_to], new_state[where_from]])
        return State(new_state)

    def goal_test(self, state):
        return Problem.goal_test(self, state)

    def path_cost(self, c, state1, action, state2):
        return c + PATH_COSTS[action[0]]

    def h(self, node):
        target_cells = self.exit_cells
        piece_cells = self.get_pieces(node.state)
        # If there are no pieces, which means the node will reach the goal,
        # return the smallest heuristic of 0 in this case.
        if not piece_cells:
            return 0
        # Otherwise, the heuristic is the sum of [the minimum distance of each
        # piece to the exit cells + 1]. Plus 1 means that when each piece
        # reaches one of the exit cells, it still needs 1 step to exit the
        # board.
        return sum(min([1 + hex_distance(cell, target)
                for target in target_cells]) for cell in piece_cells)


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
