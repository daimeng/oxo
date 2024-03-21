import numpy as np

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

    def check_winner(self) -> int:
        for a, b, c in CHECKS:
            if abs(self.board[a] + self.board[b] + self.board[c]) == 3:
                return self.board[a]

        return 2

    def make_move(self, cell) -> int:
        if self.board[cell] != EMPTY:
            return 3

        # set cell
        self.board[cell] = self.current_player_id
        # self.b = self.board.tobytes()
        self.left -= 1

        winner = self.check_winner()
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
