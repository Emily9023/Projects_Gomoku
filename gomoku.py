"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 26, 2020
"""

def is_empty(board):
    '''returns True iff there are no stones on the board board'''

    board_height = len(board)
    board_width = len(board[0])
    empty_board = True

    for i in range(board_height):
        for j in range(board_width):
            empty_board = board[i][j] == " "
            if not empty_board:
                return empty_board

    return empty_board


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    '''analyses the sequence of length length that ends at location (y end, x end). The function
    returns "OPEN" if the sequence is open, "SEMIOPEN" if the sequence if semi-open, and
    "CLOSED" if the sequence is closed. Assume that the sequence is complete (i.e., you are not
    just given a subsequence) and valid, and contains stones of only one colour.'''

    board_size = len(board) - 1
    y_beginning = y_end - d_y * (length - 1)
    x_beginning = x_end - d_x * (length - 1)

    col = board[y_end][x_end]

    beginning_open = False
    ending_open = False

    if (y_beginning - d_y) >= 0 and (x_beginning - d_x) >= 0 and (x_beginning - d_x) <= board_size and (y_beginning - d_y) <= board_size:
        if board[y_beginning - d_y][x_beginning - d_x] == " ":
            beginning_open = True

    if (y_end + d_y) <= board_size and (x_end + d_x) <= board_size and (x_end + d_x) >= 0 and  (y_end + d_y) >= 0:
        if board[y_end + d_y][x_end + d_x] == " ":
            ending_open = True

    if beginning_open and ending_open:
        return "OPEN"
    elif not beginning_open and not ending_open:
        return "CLOSED"
    else:
        return "SEMIOPEN"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    '''This function analyses the row (let’s call it R) of squares that starts at the location (y start,x start) and goes in the
    direction (d y,d x). Note that this use of the word row is different from “a row in a table”. Here the word row means a sequence of
    squares, which are adjacent either horizontally, or vertically, or diagonally. The function returns a tuple whose first element is
    the number of open sequences of colour col of length length in the row R, and whose second element is the number of
    semi-open sequences of colour col of length length in the row R. Assume that (y start,x start) is located on the edge of the board.
    Only complete sequences count. For example, column 1 in Fig. 1 is considered to contain one open row of length 3, and no other
    rows. Assume length is an integer greater or equal to 2.'''

    board_size = len(board) - 1

    open_seq_count = 0
    semi_open_seq_count = 0

    row_array = []

    y = y_start
    x = x_start

    counter = 0

    while x <= board_size and y <= board_size and x >= 0 and y >= 0:
        append_list = [y, x, board[y][x]]
        row_array.append(append_list)
        y += d_y
        x += d_x

    for i in range(len(row_array)):

        if row_array[i][2] == col:
            counter += 1

            if counter == length and i == len(row_array) - 1: #last case
                if is_bounded(board, row_array[i][0], row_array[i][1], length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1

        else:
            if counter == length:
                if is_bounded(board, row_array[i-1][0], row_array[i-1][1], length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                elif is_bounded(board, row_array[i-1][0], row_array[i-1][1], length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1

            counter = 0

    return open_seq_count, semi_open_seq_count



def detect_rows(board, col, length):

    '''This function analyses the board board. The function returns a tuple, whose first element is the
    number of open sequences of colour col of length lengthon the entire board, and whose second
    element is the number of semi-open sequences of colour col of length length on the entire board.
    Only complete sequences count. For example, Fig. 1 is considered to contain one open row of length
    3, and no other rows. Assume length is an integer greater or equal to 2. '''

    open_seq_count = 0
    semi_open_seq_count = 0

    board_size = len(board) - 1

    for i in range(board_size + 1):

        open, semi_open = detect_row(board, col, 0, i, length, 1, 0) #top edge
        open_seq_count += open
        semi_open_seq_count += semi_open

        open, semi_open = detect_row(board, col, i, 0, length, 0, 1) #left edge
        open_seq_count += open
        semi_open_seq_count += semi_open

        open, semi_open = detect_row(board, col, 0, i, length, 1, 1) #top edge
        open_seq_count += open
        semi_open_seq_count += semi_open

        open, semi_open = detect_row(board, col, 0, i, length, 1, -1) #top edge
        open_seq_count += open
        semi_open_seq_count += semi_open

    for j in range(1, board_size+1):
        open, semi_open = detect_row(board, col, j, board_size, length, 1, -1) #right edge
        open_seq_count += open
        semi_open_seq_count += semi_open

        open, semi_open = detect_row(board, col, j, 0, length, 1, 1) #left edge
        open_seq_count += open
        semi_open_seq_count += semi_open

    return open_seq_count, semi_open_seq_count

def search_max(board):
    empty_spaces = []
    max_score = -10000000000000
    temp_board = board
    temp_scores = []

    for i in range(len(board)):
        for j in range(len(board)):

            if board[i][j] == " ":
                to_append = [i,j]
                empty_spaces.append(to_append)

    for i in range(len(empty_spaces)):

        temp_board[empty_spaces[i][0]][empty_spaces[i][1]] = "b"


        '''if is_win(temp_board) == "Black won":

            temp_board[empty_spaces[i][0]][empty_spaces[i][1]] = " "

            return empty_spaces[i][0], empty_spaces[i][1]'''

        max_score = max(max_score, score(temp_board))

        temp_scores.append(score(temp_board))

        temp_board[empty_spaces[i][0]][empty_spaces[i][1]] = " "


    position = empty_spaces[temp_scores.index(max_score)]

    move_y = position[0]
    move_x = position[1]

    return move_y, move_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    '''This function determines the current status of the game, and returns one of
["White won", "Black won", "Draw", "Continue playing"], depending on the current status
on the board. The only situation where "Draw" is returned is when board is full.
'''

    board_height = len(board)
    board_width = len(board[0])

    for i in range (board_height):
        for j in range(board_width-4):

            #check if row has 5 in row
            if board[i][j] == board [i][j + 1] == board [i][j + 2] == board [i][j + 3] == board [i][j + 4] == "b":

                if j+4 == board_width - 1 and j == 0:
                    return "Black won"
                elif j+4 == board_width - 1 and board[i][j-1] != "b": #edge case
                    return "Black won"
                elif j == 0 and board[i][j+5] != "b": #first case
                    return "Black won"
                elif j+4 == board_width - 1 and board[i][j-1] == "b":
                    #return "Continue playing"
                    pass
                elif j == 0 and board[i][j+5] == "b":
                    pass
                elif board[i][j+5] != "b" and board[i][j-1] != "b":
                    return "Black won"

            if board[i][j] == board [i][j + 1] == board [i][j + 2] == board [i][j + 3] == board [i][j + 4] == "w":
                if j+4 == board_width - 1 and j == 0:
                    return "White won"
                elif j+4 == board_width - 1 and board[i][j-1] != "w": #edge case
                    return "White won"
                elif j == 0 and board[i][j+5] != "w": #first case
                    return "White won"
                elif j+4 == board_width - 1 and board[i][j-1] == "w":

                    pass
                elif j == 0 and board[i][j+5] == "w":
                    pass
                elif board[i][j+5] != "w" and board[i][j-1] != "w":
                    return "White won"

            #check if columns has 5 in row
            if board[j][i] == board [j + 1][i] == board [j + 2][i] == board [j + 3][i] == board [j + 4][i] == "b":


                if j+4 == board_width - 1 and j == 0:
                    return "Black won"
                elif j+4 == board_width - 1 and board[j-1][i] != "b": #edge case
                    return "Black won"
                elif j == 0 and board[j+5][i] != "b": #first case
                    return "Black won"
                elif j+4 == board_width - 1 and board[j-1][i] == "b":
                    #return "Continue playing"
                    pass
                elif j == 0 and board[j+5][i] == "b":
                    pass
                elif board[j+5][i] != "b" and board[j-1][i] != "b":
                    return "Black won"

            if board[j][i] == board [j + 1][i] == board [j + 2][i] == board [j + 3][i] == board [j + 4][i] == "w":
                if j+4 == board_width - 1 and j == 0:
                    return "White won"
                elif j+4 == board_width - 1 and board[j-1][i] != "w": #edge case
                    return "White won"
                elif j == 0 and board[j+5][i] != "w": #first case
                    return "White won"
                elif j+4 == board_width - 1 and board[j-1][i] == "w":
                    #return "Continue playing"
                    pass
                elif j == 0 and board[j+5][i] == "w":
                    pass
                elif board[j+5][i] != "w" and board[j-1][i] != "w":
                    return "White won"


    #check \ diagonal
    for i in range (board_height-4):
        for j in range(board_width-4):
            if board[i][j] == board [i + 1][j + 1] == board [i + 2][j + 2] == board [i + 3][j + 3] == board [i + 4][j + 4] == "b":
                if (i==0 and j+4==board_width-1) or (j==0 and i+4==board_height - 1):
                    return "Black won"
                elif (j+4 == board_width - 1 or i+4 == board_height - 1) and board[i-1][j-1] != "b": #edge case
                    return "Black won"
                elif (j==0 or i==0)  and board[i+5][j+5] != "b":
                    return "Black won"
                elif (j+4 == board_width - 1 or i+4 == board_height - 1) and board[i-1][j-1] == "b":
                    pass
                elif (j==0 or i==0)  and board[i+5][j+5] == "b":
                    pass
                elif board[i+5][j+5] == "b":
                    pass
                elif board[i-1][j-1] != "b" and board[i+5][j+5] != "b":
                    return "Black won"

            if board[i][j] == board [i + 1][j + 1] == board [i + 2][j + 2] == board [i + 3][j + 3] == board [i + 4][j + 4] == "w":
                if (i==0 and j+4==board_width-1) or (j==0 and i+4==board_height - 1):
                    return "White won"
                elif (j+4 == board_width - 1 or i+4 == board_height - 1) and board[i-1][j-1] != "w": #edge case
                    return "White won"
                elif (j==0 or i==0)  and board[i+5][j+5] != "w":
                    return "White won"
                elif (j+4 == board_width - 1 or i+4 == board_height - 1) and board[i-1][j-1] == "w":
                    pass
                elif (j==0 or i==0)  and board[i+5][j+5] == "w":
                    pass
                elif board[i+5][j+5] == "w":
                    pass
                elif board[i-1][j-1] != "w" and board[i+5][j+5] != "w":
                    return "White won"


    #check / diagonal
    for i in range (board_height-4):
        for j in range(4, board_width):
            if board[i][j] == board [i + 1][j - 1] == board [i + 2][j - 2] == board [i + 3][j - 3] == board [i + 4][j - 4] == "b":
                if (i==0 and j-4==0) or (j==board_width-1 and i+4==board_height-1):
                    return "Black won"
                elif (i+4==board_height - 1 or j-4==0) and board[i-1][j+1] != "b": #edge case
                    return "Black won"
                elif (i==0 or j==board_width-1) and board[i+5][j-5] != "b":
                    return "Black won"
                elif (i+4==board_height - 1 or j-4==0) and board[i-1][j+1] == "b":
                    pass
                elif (i==0 or j==board_width -1) and board[i+5][j-5] == "b":
                    pass
                elif board[i-1][j+1] != "b" and board[i+5][j-5] != "b":
                    return "Black won"

            if board[i][j] == board [i + 1][j - 1] == board [i + 2][j - 2] == board [i + 3][j - 3] == board [i + 4][j - 4] == "w":
                if (i==0 and j-4==0) or (j==board_width-1 and i+4==board_height-1):
                    return "White won"
                elif (i+4==board_height - 1 or j-4==0) and board[i-1][j+1] != "w": #edge case
                    return "White won"
                elif (i==0 or j==board_width -1) and board[i+5][j-5] != "w":
                    return "White won"
                elif (i+4==board_height - 1 or j-4==0) and board[i-1][j+1] == "w":
                    pass
                elif (i==0 or j==board_width -1) and board[i+5][j-5] == "w":
                    pass
                elif board[i-1][j+1] != "w" and board[i+5][j-5] != "w":
                    return "White won"


    #check if board is full
    for i in range(board_height):
        for j in range(board_width):
            if board[i][j] == " ":
                return "Continue playing"

    #returns draw if the board is full and no 5 in a row
    return "Draw"

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res


        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0





'''if __name__ == "__main__":

    #play_gomoku(8)

    board = [[" ", "w", " ", " ", " ", " ", " ", " " ],
            [" ", "w", "w", "w", "w", " ", " ", " " ],
            [" ", " ", " ", " ", " ", " ", " ", "w" ],
            [" ", " ", " ", " ", " ", " ", " ", "b" ],
            [" ", "w", " ", " ", " ", " ", " ", "b" ],
            [" ", "w", " ", " ", " ", " ", " ", "b" ],
            [" ", " ", " ", " ", " ", " ", " ", "b" ],
            [" ", " ", "b", "b", "b", "b", "b", "b" ]]

    print(is_win(board))'''