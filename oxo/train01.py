import os
from game import TicTacToe
from player import AiPlayer, HumanPlayer, Player


if __name__ == "__main__":
    game = TicTacToe()
    players: list[AiPlayer] = [AiPlayer(), AiPlayer()]

    for _ in range(1000):
        game.reset()
        # players[0].greed *= 0.99
        # players[1].greed *= 0.99

        done = False

        state0 = None
        state1 = None
        state2 = game.board.tobytes()

        while not done:
            player = players[int(game.current_player_id != 1)]
            action = player.request_move(game)

            state0 = state1
            state1 = state2

            reward = 0.0
            match game.make_move(action):
                case 3:
                    reward = -10.0
                case 2:
                    reward = 0.0
                case 0:
                    reward = 0.0
                    done = True
                case x:
                    reward = 1
                    done = True

            state2 = game.board.tobytes()
            if state0 and state2:
                player.update(state0, action, reward, state2)

            if done:
                # final update for losing player
                player = players[int(game.current_player_id != 1)]
                player.update(state1, action, -reward, state2)

    players[0].greed = 0
    players2: list[Player] = [players[0], HumanPlayer()]
    while True:
        os.system("clear")
        game.reset()

        while True:
            pnum = int(game.current_player_id != 1)
            player = players2[pnum]
            action = player.request_move(game)
            res = game.make_move(action)
            os.system("clear")
            print(f"Player {pnum} plays {action}!")
            print(game.board.reshape(3, 3))
            if res < 2:
                break
