# String constants to avoid typos
COLOUR = "colour"
PIECES = "pieces"
BLOCKS = "blocks"
MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"

# The minimum and maximum coordinates on the q and r axes
MIN_COORDINATE = -3
MAX_COORDINATE = 3

# Delta values which give the corresponding cells by adding them to the current
# cell
MOVE_DELTA = [(0, 1), (1, 0), (-1, 1), (0, -1), (-1, 0), (1, -1)]
JUMP_DELTA = [(delta_q * 2, delta_r * 2) for delta_q, delta_r in MOVE_DELTA]


def all_cells():
    """
    generate the coordinates of all cells on the board.
    """
    ran = range(MIN_COORDINATE, MAX_COORDINATE + 1)
    return [(q, r) for q in ran for r in ran if -q-r in ran]


ALL_CELLS = all_cells()


def generate_cells(cell, delta_pairs):
    """
    generate a list of cells by adding delta values
    """
    return [(cell[0] + delta_q, cell[1] + delta_r)
                            for delta_q, delta_r in delta_pairs]


def moveable_cells(curr_cell, occupied):
    """
    moveable_cells are cells next to the current_cell with nothing occupied
    """
    neighbours = generate_cells(curr_cell, MOVE_DELTA)
    return [cell for cell in neighbours
                    if cell in ALL_CELLS and cell not in occupied]

def jumpable_cells(curr_cell, occupied):
    """
    jumpable_cells are cells that are one cell apart from the current cell
    and cells in the middle must be occupied by either a block or a piece
    """
    generated_cells = generate_cells(curr_cell, JUMP_DELTA)
    jumpable = []
    for cell in generated_cells:
        if cell in ALL_CELLS and cell not in occupied:
            middle_cell = tuple(map(lambda x, y: (x + y) // 2, curr_cell, cell))
            if middle_cell in ALL_CELLS and middle_cell in occupied:
                jumpable.append(cell)
    return jumpable


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

    ran = range(-3, 3 + 1)
    # prepare the provided board contents as strings, formatted to size.
    cells = []
    for qr in [(q, r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)
