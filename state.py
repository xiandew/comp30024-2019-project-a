class State:
    """
    It is used to store a state of the board which is defined by all cells on
    the board and their corresponding states (whether the cell is empty,
    blocked or occupied by a piece).
    """

    def __init__(self, board_dict, distance_dict = None):
        self.board_dict = board_dict
        self.distance_dict = distance_dict

    def __eq__(self, other):
        if other:
            return self.board_dict == other.board_dict
        return False

    def __str__(self):
        return str(self.board_dict)

    def __lt__(self, other):
        return str(self) < str(other)

    def __hash__(self):
        return hash(str(self))
