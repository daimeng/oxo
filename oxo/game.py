from typing import Optional, List
from player import Player, HumanPlayer, RandomPlayer, AiPlayer
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
    winner: int = 0
    print = False
    players: List[Player]
    left = 9

    def __init__(self, players):
        self.players = players
        self.board = np.array([EMPTY] * 9)
        self.current_player_id = 1

    def curr_player(self) -> Player:
        return self.players[0 if self.current_player_id == 1 else 1]

    def print_board(self):
        if self.print:
            print(self.board.reshape(3, 3))

    def check_winner(self):
        for a, b, c in CHECKS:
            if abs(self.board[a] + self.board[b] + self.board[c]) == 3:
                self.winner = self.board[a]
                return True

        return False

    def is_board_full(self):
        # return EMPTY not in self.board
        return self.left == 0

    def make_move(self, cell):
        if self.board[cell] != EMPTY:
            if self.print:
                print("Invalid move! Try again.")
            return False

        self.board[cell] = self.current_player_id
        self.left -= 1

        if self.check_winner():
            if self.print:
                print(f"Player {self.current_player_id} wins!")
            return True
        elif self.is_board_full():
            if self.print:
                print("It's a tie!")
            return True
        else:
            # next turn
            self.current_player_id = -self.current_player_id
            return False


# run game: python game.py
if __name__ == "__main__":
    # game = TicTacToe(players=[HumanPlayer(), RandomPlayer()])
    game = TicTacToe(players=[HumanPlayer(), AiPlayer("model.keras")])
    game.print = True

    while True:
        game.print_board()
        cell = game.curr_player().request_move(game.board, game.left)
        if game.make_move(cell):
            break
