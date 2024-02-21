from abc import ABC, abstractmethod
from typing import Tuple, Any
from keras import Model, saving
import numpy as np


class Player(ABC):
    @abstractmethod
    def request_move(self, board: np.ndarray, left: int) -> int:
        pass


class HumanPlayer(Player):
    def request_move(self, board: np.ndarray, left: int) -> int:
        row = int(input("Enter row (0, 1, 2): "))
        col = int(input("Enter column (0, 1, 2): "))
        return row * 3 + col


class RandomPlayer(Player):
    def request_move(self, board: np.ndarray, left: int) -> int:
        r = 1 + np.random.randint(0, left + 1)
        for i, cell in enumerate(board):
            if cell == 0:
                r -= 1
            if r == 0:
                return i
        return 0


class AiPlayer(Player):
    model: Any

    def __init__(self, filepath: str):
        self.model = saving.load_model(filepath)

    def request_move(self, board: np.ndarray, left: int) -> int:
        r = self.model.predict(np.expand_dims(board, axis=0))
        r = int(r[0][0])
        if board[r] == 0:
            return r

        print("Invalid move, selecting randomly")
        r = 1 + np.random.randint(0, left + 1)
        for i, cell in enumerate(board):
            if cell == 0:
                r -= 1
            if r == 0:
                return i
        return 0
