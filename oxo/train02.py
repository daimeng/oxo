from game import TicTacToe
from keras.models import Sequential
from keras.layers import Dense, Input

# from player import AiPlayer
import numpy as np

X = []
y = []

# if __name__ == "__main__":
#     for i in range(10):
#         game = TicTacToe(players=[AiPlayer("model.keras"), AiPlayer("model.keras")])

#         while True:
#             cell = game.curr_player().request_move(game.board, game.left)
#             X.append(game.board)
#             y.append(cell)
#             over = game.make_move(cell)
#             if over:
#                 break

#     X = np.array(X)
#     y = np.array(y)

#     model = Sequential()
#     model.add(Input(shape=(9,)))
#     model.add(Dense(9, activation="relu"))
#     model.add(Dense(1, activation="softmax"))
#     model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
#     model.fit(X, y, epochs=100, batch_size=64)
#     model.save("model.keras")
