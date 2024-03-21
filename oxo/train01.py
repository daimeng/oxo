import os
from game import TicTacToe, print_board
from player import AiPlayer, Player, RandomPlayer, HumanPlayer
from typing import Any, Optional


if __name__ == "__main__":
    game = TicTacToe()
    players: list[Player] = [AiPlayer(), AiPlayer()]
    xp: list[Optional[tuple[bytes, int, float]]] = [None, None]
    wins0 = 0
    wins1 = 0

    for _ in range(100000):
        game.reset()
        # players[0].greed *= 0.99
        # players[1].greed *= 0.99

        done = False

        while not done:
            pnum = int(game.current_player_id != 1)
            player = players[pnum]

            state = game.board.tobytes()

            # update experience before replacing
            lastxp = xp[pnum]
            if lastxp is not None and isinstance(player, AiPlayer):
                s, a, r = lastxp
                player.update(s, a, r, state)

            # get next experience
            action = player.request_move(game)
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
                    if x == 1:
                        wins0 += 1
                    elif x == -1:
                        wins1 += 1
                    done = True

            xp[pnum] = (state, action, reward)

            # if final state
            if done:
                if isinstance(player, AiPlayer):
                    player.update(state, action, reward, game.board.tobytes())

                # final update for losing player
                pnum = int(game.current_player_id != 1)
                player = players[pnum]
                lastxp = xp[pnum]

                if lastxp is not None and isinstance(player, AiPlayer):
                    s, a, r = lastxp
                    player.update(s, a, -r, state)

    print(wins0, wins1)

    if isinstance(players[0], AiPlayer):
        players[0].greed = 0
    players: list[Player] = [players[0], HumanPlayer()]

    for _ in range(1000):
        game.reset()

        while True:
            print_board(game.board)
            player = players[int(game.current_player_id != 1)]  # 1 -> 0, -1 -> 1
            cell = player.request_move(game)
            if game.make_move(cell) < 2:
                break

    # if isinstance(players[0], AiPlayer):
    #     players[0].greed = 0
    # players2: list[Player] = [RandomPlayer(), RandomPlayer()]
    # wins0 = 0
    # wins1 = 0
    # for _ in range(1000):
    #     # os.system("clear")
    #     game.reset()

    #     while True:
    #         pnum = int(game.current_player_id != 1)
    #         player = players2[pnum]
    #         action = player.request_move(game)
    #         res = game.make_move(action)
    #         # os.system("clear")
    #         # print(f"Player {pnum} plays {action}!")
    #         # print(game.board.reshape(3, 3))
    #         if res < 2:
    #             if res == 1:
    #                 wins0 += 1
    #             if res == -1:
    #                 wins1 += 1
    #             break

    # print(wins0, wins1)
