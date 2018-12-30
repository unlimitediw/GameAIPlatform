"""
N-Puzzle
0   3	8
4	1	7
2	6	5

A* method N-puzzle solution

A* value = heuristic value + path value
principle: Fine the state with minimize A* value and explore it to generate the new states.
           When one of new state's heuristic value == 0, return its path value which is the answer

heuristic = Manhattan distance + Linear conflict

The Manhattan distance = abs(X_pos - X_correct_pos) + abs(Y_pos - Y_correct_pos).
Linear conflict = 2 * (total times of linear conflict exist.

effect: can solve most 8-puzzle, 15-puzzle problems and some easy 24-puzzle problems.

(P.S.------------------------------------------------------------------------------------
This part is about the optimize heuristic but not been implemented in this project yet.
The reason not implemented yet is that the construction of database is time consuming and time is not enough for me.
Apart from Manhattan distance + Linear conflict we can do one more thing to the heuristic function
which is heuristic = max(actual_path__A, actual_path_B)
It's name is pattern database which can solve most complicated 15-puzzle in 10s(after construction of database)

Main idea:
A A A A
A A A A
B B B B
B B B B
Take this board as an example A set should be [1, 2, 3, 4, 5, 6, 7, 8], B set should be [9, 10, 11, 12, 13, 14, 15, 0]
The initialized board may be in this order below:
5  3  7  12                     5  3  7  *       *  *  *  12
1  6  11 15     -------> we is  1  6  *  *  and  *  *  11 15
13 8  0  4                      *  8  *  4       13 *  0  *
9  2  10 14                     *  2  *  *       9  *  10 14
We can calculate both A's and B's actual cost to reorder into correct position and save this value with key into
database

Like A[5370160008040200] = A_actual_value, B[99999912999911151399009909991014] = B_actual_value

The construction of database since for each case we have 16!/8!(which is 518918400) key value so we can separate the
board into three part which will get database in 16!/11!(524160) level.

We can design the board separated in different level or pattern
for example:
2 parts:
A A A B
A A A B
A A A B
B B B B
3 parts:
A A A A
B A B B
B B B C
C C C C

The different design will generate different effect which need us to try and test

With this database(constructed by A*(p+heuristic = Manhattan distance + Linear conflict))
The new heuristic = max(A,B,C...)(the total part you separated, general speaking, less part separate less time to solve
problem but more time to construct data base)
End)

"""

import copy


class NPuzzle:
    def rearrange_n_puzzle(self, board):

        # I use a dictionary 'dic' here to collect all the sub_situations
        # with key value of the A* value(heuristic + path)
        dic = {}

        # Initialization
        blank_pos = [0, 0]
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    blank_pos = [i, j]

        ini_board = Board()
        ini_board.blank_pos = blank_pos
        ini_board.board = board
        ini_board.recalculate_heuristic_new()
        ini_board.total_cost = ini_board.heuristic + ini_board.path_cost
        dic[ini_board.total_cost] = [ini_board]
        # explore all elements in the dic in the order of its key value
        while dic:
            b = dic[min(dic.keys())][0]
            for i in range(len(b.direction_memo)):
                if b.direction_memo[i] == 0:
                    # each move is a new state so we create a new board class
                    # copy the old one and change base on it
                    new_b = Board()
                    if self.make_move(i, b, new_b):
                        new_b.recalculate_heuristic_new()
                        if new_b.heuristic == 0:
                            print("Finished", new_b.path_cost)
                            exit()
                        new_b.total_cost = new_b.heuristic + new_b.path_cost
                        if new_b.total_cost not in dic:
                            dic[new_b.total_cost] = [new_b]
                        else:
                            # one key map to a list and the elements in the list have the same A* value
                            dic[new_b.total_cost].append(new_b)
            if len(dic[b.total_cost]) == 1:
                dic.pop(b.total_cost)
            else:
                del (dic[b.total_cost][0])

    def make_move(self, direction, b, new_b):
        new_b.path_cost = b.path_cost + 1           # each move will add 1 to the path_cost
        new_b.board = copy.deepcopy(b.board)
        new_b.blank_pos = b.blank_pos[:]
        if direction == 0 and b.blank_pos[0] > 0:
            # do the swap operation
            new_b.board[b.blank_pos[0]][b.blank_pos[1]] = b.board[b.blank_pos[0] - 1][
                b.blank_pos[1]]
            new_b.board[b.blank_pos[0] - 1][b.blank_pos[1]] = 0
            new_b.blank_pos[0] -= 1
            new_b.direction_memo = [0, 1, 0, 0]     # the previous direction should be omit
            return True
        elif direction == 1 and b.blank_pos[0] < len(b.board) - 1:
            new_b.board[b.blank_pos[0]][b.blank_pos[1]] = b.board[b.blank_pos[0] + 1][
                b.blank_pos[1]]
            new_b.board[b.blank_pos[0] + 1][b.blank_pos[1]] = 0
            new_b.blank_pos[0] += 1
            new_b.direction_memo = [1, 0, 0, 0]
            return True
        elif direction == 2 and b.blank_pos[1] > 0:
            new_b.board[b.blank_pos[0]][b.blank_pos[1]] = b.board[b.blank_pos[0]][
                b.blank_pos[1] - 1]
            new_b.board[b.blank_pos[0]][b.blank_pos[1] - 1] = 0
            new_b.blank_pos[1] -= 1
            new_b.direction_memo = [0, 0, 0, 1]
            return True
        elif direction == 3 and b.blank_pos[1] < len(b.board[0]) - 1:
            new_b.board[b.blank_pos[0]][b.blank_pos[1]] = b.board[b.blank_pos[0]][
                b.blank_pos[1] + 1]
            new_b.board[b.blank_pos[0]][b.blank_pos[1] + 1] = 0
            new_b.blank_pos[1] += 1
            new_b.direction_memo = [0, 0, 1, 0]
            return True
        return False


class Board(object):
    # 0-up 1-down 2-left 3-right
    direction_memo = [0, 0, 0, 0]   # history direction memo
    blank_pos = (0, 0)              # blank_pos memo
    board = [[]]
    heuristic = 0
    path_cost = 0
    total_cost = 0

    # heuristic calculation:
    # calculate manhattan distance
    # calculate linear conflict at the same time
    def recalculate_heuristic_new(self):
        heuristic = 0
        l = len(self.board)
        row_memo = [0 for i in range(l)]
        col_memo = [0 for i in range(l)]
        for i in range(l):
            for j in range(l):
                ac_row = (self.board[i][j] - 1) // l
                ac_col = (self.board[i][j] - 1) % l
                if ac_row == i and ac_col != j:
                    if row_memo[i] != 0 and self.board[i][j] < row_memo[i] and self.board[i][j] != 0:
                        # calculate linear conflict
                        heuristic += 2
                    row_memo[i] = self.board[i][j]
                elif ac_col == j and ac_row != i:
                    if col_memo[j] != 0 and self.board[i][j] < col_memo[j] and self.board[i][j] != 0:
                        heuristic += 2
                    col_memo[j] = self.board[i][j]
                # Manhattan distance
                if self.board[i][j] != 0:
                    # calculate manhattan distance
                    heuristic += abs(ac_row - i) + abs(ac_col - j)
        self.heuristic = heuristic

    # with pattern database


# Data initialization:
# just put your n-puzzle.txt in the same dictionary of N_Puzzle_basic.py
datafile = 'n-puzzle.txt'
board = []
with open(datafile) as f:
    for line in f:
        sub_list = []
        sub_list.extend([int(i) for i in line.split()])
        board.append(sub_list)

# There are some test cases for 8, 15 and 24-puzzle
# board = [[15, 2, 1, 12], [8, 5,  11], [4, 9, 10, 7], [3, 14, 13, 0]]
# board = [[12,6,9,4], [2,7,13,15], [1,8,3,5], [11,10,0,14]]
# board = [[3,6,4,8],[1,0,5,2],[14,10,15,12],[9,13,7,11]]
# board = [[4,3,2,1],[5,6,7,8],[9,10,11,12],[0,13,14,15]]
# board = [[0,3,8],[4,1,7],[2,6,5]]
# board = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,24,23,0,22]]
# board = [[4,0,12,7,5],[2,1,20,10,8],[24,11,16,19,3],[17,23,22,15,14],[6,21,18,9,13]]

# Run
a = NPuzzle()
a.rearrange_n_puzzle(board)
