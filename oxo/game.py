import numpy as np
from numba import njit, types, typeof
from numba.experimental import jitclass

EMPTY = 0

CHECKS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


@njit()
def pack(board: np.ndarray) -> int:
    s = 0
    for b in board:
        s += b + 1
        s <<= 2
    return s


@njit()
def check_winner(board) -> int:
    if abs(board[0] + board[1] + board[2]) == 3:
        return board[0]

    if abs(board[0] + board[3] + board[6]) == 3:
        return board[0]

    if abs(board[3] + board[4] + board[5]) == 3:
        return board[3]

    if abs(board[6] + board[7] + board[8]) == 3:
        return board[6]

    if abs(board[1] + board[4] + board[7]) == 3:
        return board[1]

    if abs(board[2] + board[5] + board[8]) == 3:
        return board[2]

    if abs(board[0] + board[4] + board[8]) == 3:
        return board[0]

    if abs(board[2] + board[4] + board[6]) == 3:
        return board[2]

    return 2


spec = [
    ("board", typeof(np.array([], dtype="int8"))),
    ("current_player_id", types.int8),
    ("left", types.uint8),
]


@jitclass(spec)
class TicTacToe:
    board: np.ndarray
    current_player_id: int
    left: int
    # b: bytes

    def __init__(self):
        self.board = np.zeros(9, dtype="int8")
        self.reset()

    def reset(self):
        self.left = 9
        self.board[:] = 0
        self.current_player_id = 1

    def make_move(self, cell) -> int:
        if self.board[cell] != EMPTY:
            return 3

        # set cell
        self.board[cell] = self.current_player_id
        # self.b = self.board.tobytes()
        self.left -= 1

        winner = check_winner(self.board)
        # next turn
        self.current_player_id = -self.current_player_id

        if winner != 2:
            return winner
        elif self.left == 0:
            return 0
        else:
            return 2


def print_board(board: np.ndarray):
    print("---->")
    for row in board.reshape(3, 3):
        for cell in row:
            if cell == 1:
                print(" X", end="")
            elif cell == 0:
                print(" .", end="")
            elif cell == -1:
                print(" O", end="")
        print("")
    print("<----")
