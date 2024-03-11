from typing import Optional, List
from player import Player, HumanPlayer, RandomPlayer
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
    left = 9

    def __init__(self):
        self.board = np.zeros(9, dtype="int8")
        self.reset()

    def reset(self):
        self.board[:] = 0
        self.current_player_id = 1

    def check_winner(self) -> int:
        for a, b, c in CHECKS:
            if abs(self.board[a] + self.board[b] + self.board[c]) == 3:
                return self.board[a]

        return 2

    def make_move(self, cell) -> int:
        if self.board[cell] != EMPTY:
            return 2

        # set cell
        self.board[cell] = self.current_player_id
        self.left -= 1

        winner = self.check_winner()
        if winner != 2:
            return winner
        elif self.left == 0:
            return 0
        else:
            # next turn
            self.current_player_id = -self.current_player_id
            return 2


# run game: python game.py
if __name__ == "__main__":
    game = TicTacToe()

    players: list[Player] = [HumanPlayer(), RandomPlayer()]

    while True:
        print(game.board.reshape(3, 3))
        player = players[int(game.current_player_id != 1)]  # 1 -> 0, -1 -> 1
        cell = player.request_move(game)
        if game.make_move(cell) != 2:
            break
