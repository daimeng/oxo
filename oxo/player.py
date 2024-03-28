from typing import DefaultDict
from numba import njit, types
from numba.experimental import jitclass
from numba.typed import Dict
import random
from .game import TicTacToe, print_board, pack
from collections import defaultdict

# from keras import Model, saving
import numpy as np


class Player:
    def __init__(self):
        pass

    def request_move(self, game: TicTacToe) -> int:
        return 0


@jitclass()
class HumanPlayer(Player):
    def request_move(self, game: TicTacToe) -> int:
        row, col = input("Enter coords (as 1-3, 1-3): ").split(",")
        row = int(row.strip()) - 1
        col = int(col.strip()) - 1
        return row * 3 + col


@jitclass()
class RandomPlayer(Player):
    def request_move(self, game: TicTacToe) -> int:
        r = random.randint(0, game.left)
        rr = r
        for i, cell in enumerate(game.board):
            if cell == 0:
                rr -= 1
            if rr <= 0:
                return i
        raise Exception(
            f"Something went wrong: r={r}, rr={rr}, left={game.left}\n{game.board.reshape(3, 3)}"
        )


@njit()
def newrow():
    return np.zeros(9, dtype="int64")


aispec = [("Q", types.DictType(types.int64, types.int64[:]))]


@njit()
def random_move(game: TicTacToe):
    r = random.randint(0, game.left)
    rr = r
    for i, cell in enumerate(game.board):
        if cell == 0:
            rr -= 1
        if rr <= 0:
            return i
    raise Exception(
        f"Something went wrong: r={r}, rr={rr}, left={game.left}\n{game.board.reshape(3, 3)}"
    )


@jitclass(aispec)
class AiPlayer(Player):
    Q: dict[int, np.ndarray]
    lr: float
    discount: float
    greed: float

    def __init__(self, lr=0.1, discount=1.0, greed=0.5):
        self.Q = Dict.empty(key_type=types.int64, value_type=types.int64[:])
        self.lr = lr
        self.discount = discount
        self.greed = greed

    def request_move(self, game: TicTacToe) -> int:
        state = pack(game.board)

        if random.uniform(0, 1) < self.greed:
            action = random_move(game)
        elif state in self.Q:
            action = int(np.argmax(self.Q[state]))
        else:
            action = random_move(game)

        return action

    def update(self, state: int, action: int, reward: float, nstate: int):
        # print_board(np.frombuffer(state, dtype="int8"))
        # print(
        #     action,
        #     reward,
        # )
        # print_board(np.frombuffer(nstate, dtype="int8"))
        # print("")

        if state not in self.Q:
            self.Q[state] = newrow()

        if nstate not in self.Q:
            self.Q[nstate] = newrow()

        oldv = self.Q[state][action]

        # max of new state
        next_max = np.max(self.Q[nstate])

        # higher learning rate takes more from future rewards
        self.Q[state][action] = (1 - self.lr) * oldv + self.lr * (
            reward + self.discount * next_max
        )
