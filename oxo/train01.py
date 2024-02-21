from game import TicTacToe
from keras.models import Sequential
from keras.layers import Dense, Input
from player import RandomPlayer
import numpy as np

X = []
w = []
y = []

if __name__ == "__main__":
    for i in range(1000):
        game = TicTacToe(players=[RandomPlayer(), RandomPlayer()])

        while True:
            cell = game.curr_player().request_move(game.board, game.left)
            X.append(game.board)
            w.append(game.winner)
            y.append(cell)
            over = game.make_move(cell)
            if over:
                break

    X = np.asarray(X)
    w = np.asarray(w)
    y = np.asarray(y)

    model = Sequential()
    model.add(Input(shape=(9,)))
    model.add(Dense(9, activation="relu"))
    model.add(Dense(1, activation="softmax"))
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.fit(X, [w, y], epochs=100, batch_size=64)
    model.save("model.keras")
