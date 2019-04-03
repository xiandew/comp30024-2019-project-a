import re
import time
import json
import sys

SPEED = 1.5  # number of seconds per frame
DEBUG = False  # for a larger board drawing that includes the coordinates inside each hex

def print_board(board_dict, message="", **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.

    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using 
    the axial coordinate system outlined in the project specification) and the 
    values are formatted as strings and placed in the drawing at the corres- 
    ponding location (only the first 5 characters of each string are used, to 
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the 
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates 
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not DEBUG:
        # Use the normal board template (smaller, not showing coordinates)
        # 16
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
        # 23
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

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q, r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            val = board_dict[qr]
            cell = val[0] + str(val[1]).center(5) + val[2]
        else:
            cell = "     "  # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


seq = []
while True:
    try:
        l = input()
        if l and l[0] == "#":
            continue
        else:
            rt = re.findall(r"\((\+?-?\d+), ?(\+?-?\d+)\)", l)
            src = tuple(map(int, rt[0]))
            if "EXIT" in l:
                dest = None
            else:
                dest = tuple(map(int, rt[1]))
            seq.append((src, dest, l))
    except EOFError:
        break

RESET = "\x1b[0m"
BLOCK = "\x1b[7m"
COLOR = {
    "red": ("\x1b[31m", "\x1b[1m\x1b[7m\x1b[31;1m"),
    "green": ("\x1b[32m", "\x1b[1m\x1b[7m\x1b[32;1m"),
    "blue": ("\x1b[34m", "\x1b[1m\x1b[7m\x1b[34;1m")
}


def move_up(n): return f"\x1b[{n}A"


height = 23 if DEBUG else 16

d = {}

with open(sys.argv[1]) as file:
    data = json.load(file)

board = dict()
color = COLOR[data['colour']]

for i in data['pieces']:
    board[tuple(i)] = (color[0], "(" + data['colour'][0] + ")", RESET)
for i in data['blocks']:
    board[tuple(i)] = (BLOCK, "", RESET)

print_board(board, "Starting")

for idx, i in enumerate(seq):
    time.sleep(SPEED)
    sys.stdout.write(move_up(height))
    sys.stdout.flush()
    src, des, cmd = i
    if des:
        board[des] = (color[1], board[src][1], RESET)
    board[src] = ("", board[src][1][1], "")
    print_board(board, "{}/{}: {:<50}".format(idx + 1, len(seq), cmd))
    if des:
        board[des] = (color[0], board[des][1], RESET)
    board[src] = ("", "", "")

time.sleep(SPEED)
sys.stdout.write(move_up(height))
sys.stdout.flush()
print_board(board, "Final board".ljust(50))
for i in board.values():
    if any(j in i[1] for j in ('r', 'g', 'b')):
        print("# " + COLOR["red"][1] + "This sequence is not complete." + RESET)
        exit()
print("# " + COLOR["green"][1] + "This sequence is complete." + RESET)
