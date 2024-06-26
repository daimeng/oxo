import numpy as np
import random
from numba import njit, types
from numba.typed import List
from numba.experimental import jitclass
from .player import Player, random_move
from .game import TicTacToe, pack


nnspec = [
    ("W1", types.Array(types.float64, 2, "C")),
    ("b1", types.Array(types.float64, 2, "C")),
    ("W2", types.Array(types.float64, 2, "C")),
    ("b2", types.Array(types.float64, 2, "C")),
    ("loss", types.ListType(types.float64)),
]


@jitclass(nnspec)
class NnPlayer(Player):
    W1: np.ndarray
    b1: np.ndarray
    W2: np.ndarray
    b2: np.ndarray

    lr: float
    discount: float
    epsilon: float
    loss: list[float]

    def __init__(self, lr=0.00001, discount=1.0, epsilon=0.5):
        # input x hidden

        self.W1 = np.random.rand(9, 360) - 0.5
        self.b1 = np.random.rand(1, 360) - 0.5
        self.W2 = np.random.rand(360, 9) - 0.5
        self.b2 = np.random.rand(1, 9) - 0.5

        self.lr = lr
        self.discount = discount
        self.epsilon = epsilon
        self.loss = List.empty_list(types.float64)

    def request_move(self, game: TicTacToe) -> int:
        X = game.board.reshape(1, 9).astype(np.float64)

        if random.uniform(0, 1) < self.epsilon:
            action = random_move(game)
        else:
            p, _, _, _ = self.forward(X)
            action = int(np.argmax(p[0]))

        return action

    def forward(
        self, X: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        # 1x36 = 1x9 * 9x36
        Z1 = X.dot(self.W1) + self.b1
        A1 = np.maximum(0, Z1)  # ReLU

        # 1x9 = 1x36 * 36x9
        Z2 = A1.dot(self.W2) + self.b2

        # # 1x9, softmax
        # Z2x = np.exp(Z2)
        # A2 = Z2x / np.sum(Z2x)

        # sigmoid
        # A2 = 1 / (1 + np.exp(-Z2))
        A2 = Z2
        return A2, Z2, A1, Z1

    def update(self, state: np.ndarray, action: int, reward: float):
        X = state.reshape(1, 9).astype(np.float64)
        # forward prop
        qvalues, Z2, A1, Z1 = self.forward(X)

        # TD target, -1 for illegal moves
        target = np.where(state == 0, qvalues, -1)
        target[0, action] = reward

        error = qvalues - target
        loss = qvalues[0, action] - reward
        self.loss.append(loss**2)

        # sig_deriv_q = qvalues * (1 - qvalues)
        dZ2 = error  # * sig_deriv_q

        # 36x9 = 36x1 * 1x9
        dW2 = A1.T.dot(dZ2)
        db2 = dZ2

        # 1x36 = 1x9 * 9x36
        ReLU_deriv = Z1 > 0
        dZ1 = dZ2.dot(self.W2.T) * ReLU_deriv

        # 9x36 = 9x1 * 1x36
        dW1 = X.T.dot(dZ1)
        db1 = dZ1

        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
