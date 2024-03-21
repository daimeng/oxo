from abc import ABC, abstractmethod
from typing import DefaultDict
import random
from game import TicTacToe, print_board
from collections import defaultdict

# from keras import Model, saving
import numpy as np


class Player(ABC):
    @abstractmethod
    def request_move(self, game: TicTacToe) -> int:
        pass


class HumanPlayer(Player):
    def request_move(self, game: TicTacToe) -> int:
        row = int(input("Enter row (0, 1, 2): "))
        col = int(input("Enter column (0, 1, 2): "))
        return row * 3 + col


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


randy = RandomPlayer()

NEWROW = lambda: np.zeros(9)


class AiPlayer(Player):
    Q: DefaultDict[bytes, np.ndarray]
    lr: float
    discount: float
    greed: float

    def __init__(self, lr=0.1, discount=1.0, greed=0.5):
        self.Q = defaultdict(NEWROW)
        self.lr = lr
        self.discount = discount
        self.greed = greed

    def request_move(self, game: TicTacToe) -> int:
        state = game.board.tobytes()

        if random.uniform(0, 1) < self.greed:
            action = randy.request_move(game)
        else:
            action = int(np.argmax(self.Q[state]))

        return action

    def update(self, state: bytes, action: int, reward: float, nstate: bytes):
        print_board(np.frombuffer(state, dtype="int8"))
        print(
            action,
            reward,
        )
        print_board(np.frombuffer(nstate, dtype="int8"))
        print("")

        oldv = self.Q[state][action]

        # max of new state
        next_max = np.max(self.Q[nstate])

        # higher learning rate takes more from future rewards
        newv = (1 - self.lr) * oldv + self.lr * (reward + self.discount * next_max)

        # update
        self.Q[nstate][action] = newv
