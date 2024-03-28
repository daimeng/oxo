from .game import TicTacToe
from .player import Player, HumanPlayer, RandomPlayer

# run game: python play.py
if __name__ == "__main__":
    game = TicTacToe()

    players: list[Player] = [HumanPlayer(), RandomPlayer()]

    while True:
        print(game.board.reshape(3, 3))
        player = players[int(game.current_player_id != 1)]  # 1 -> 0, -1 -> 1
        cell = player.request_move(game)
        if game.make_move(cell) < 2:
            break
