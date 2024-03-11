from game import TicTacToe
from keras.models import Sequential
from keras.layers import Dense, Input
from player import AiPlayer, RandomPlayer
import numpy as np

X = []
w = []
y = []

if __name__ == "__main__":
    game = TicTacToe()
    for i in range(1000):
        game.reset()
        players = [AiPlayer(), AiPlayer()]

        while True:
            player = players[int(game.current_player_id != 1)]
            cell = player.request_move(game)
            X.append(game.board)
            y.append(cell)
            if game.make_move(cell) != 2:
                break

    X = np.asarray(X)
    w = np.asarray(w)
    y = np.asarray(y)

    model = Sequential()
    model.add(Input(shape=(9,)))
    model.add(Dense(256, activation="relu"))
    model.add(Dense(1, activation="softmax"))
    model.compile(
        loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
    )
    model.fit([X, w], y, epochs=100, batch_size=64)
    model.save("model.keras")
