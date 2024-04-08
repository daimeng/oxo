import sys
from numba import njit
import numpy as np
from .game import TicTacToe, print_board, pack
from .player import AiPlayer, Player, RandomPlayer, HumanPlayer


@njit()
def train(game: TicTacToe, players: list[Player]):
    wins0 = 0
    wins1 = 0
    xp0: list[tuple[int, int, float]] = [(-1, 0, 0.0)]
    xp1: list[tuple[int, int, float]] = [(-1, 0, 0.0)]

    for _ in range(1000):
        # if isinstance(players[0], AiPlayer):
        #     players[0].epsilon -= 0.0002
        # if isinstance(players[1], AiPlayer):
        #     players[1].epsilon *= 0.0001

        for _ in range(1000):
            xp0.clear()
            xp1.clear()
            game.reset()
            done = False

            while not done:
                pnum = int(game.current_player_id != 1)
                player = players[pnum]

                state = pack(game.board)

                # get next experience
                action = player.request_move(game)
                reward = 0.0
                lreward = 0.0
                match game.make_move(action):
                    case 3:
                        reward = -10.0
                    case 2:
                        reward = 0.0
                    case 0:
                        reward = 0.9
                        lreward = 0.9
                        done = True
                    case x:
                        reward = 1.0
                        lreward = -1.0
                        if x == 1:
                            wins0 += 1
                        elif x == -1:
                            wins1 += 1
                        done = True

                xp = xp0 if pnum == 0 else xp1
                xp.append((state, action, reward))

                if done:
                    # assign negative reward to loser's last move
                    pnum = int(game.current_player_id != 1)
                    xp = xp0 if pnum == 0 else xp1
                    lastxp = xp[-1]
                    xp[-1] = (lastxp[0], lastxp[1], lreward)

            # do weight updates
            for pnum in range(2):
                player = players[pnum]
                nstate = pack(game.board)
                xp = xp0 if pnum == 0 else xp1
                xplen = len(xp)

                for i in range(xplen - 1, -1, -1):
                    state, action, reward = xp[i]

                    if isinstance(player, AiPlayer):
                        player.update(state, action, reward, nstate)
                    nstate = state

    return wins0, wins1


def main(opts):
    game = TicTacToe()
    players: list[Player] = [AiPlayer(epsilon=0.5), AiPlayer(epsilon=0.5)]

    w0, w1 = train(game, players)
    print(w0, w1)

    if "play" in opts or "play2" in opts:
        if "play" in opts:
            if isinstance(players[0], AiPlayer):
                players[0].epsilon = 0
            players: list[Player] = [players[0], HumanPlayer()]
        else:
            if isinstance(players[1], AiPlayer):
                players[1].epsilon = 0
            players: list[Player] = [HumanPlayer(), players[1]]

        for _ in range(1000):
            game.reset()

            while True:
                print_board(game.board)
                player = players[int(game.current_player_id != 1)]  # 1 -> 0, -1 -> 1
                cell = player.request_move(game)
                if game.make_move(cell) < 2:
                    break

    elif "test" in opts:
        if isinstance(players[0], AiPlayer):
            players[0].epsilon = 0
        players2: list[Player] = [players[0], RandomPlayer()]
        wins0 = 0
        wins1 = 0
        for _ in range(10000):
            # os.system("clear")
            game.reset()

            while True:
                pnum = int(game.current_player_id != 1)
                player = players2[pnum]
                action = player.request_move(game)
                res = game.make_move(action)
                # os.system("clear")
                # print(f"Player {pnum} plays {action}!")
                # print(game.board.reshape(3, 3))
                if res < 2:
                    if res == 1:
                        wins0 += 1
                    if res == -1:
                        wins1 += 1
                    break

        print(wins0, wins1)

        if isinstance(players[1], AiPlayer):
            players[1].epsilon = 0
        players2: list[Player] = [RandomPlayer(), players[1]]
        wins0 = 0
        wins1 = 0
        for _ in range(10000):
            # os.system("clear")
            game.reset()

            while True:
                pnum = int(game.current_player_id != 1)
                player = players2[pnum]
                action = player.request_move(game)
                res = game.make_move(action)
                # os.system("clear")
                # print(f"Player {pnum} plays {action}!")
                # print(game.board.reshape(3, 3))
                if res < 2:
                    if res == 1:
                        wins0 += 1
                    if res == -1:
                        wins1 += 1
                    break

        print(wins0, wins1)


if __name__ == "__main__":
    main(sys.argv[1:])
