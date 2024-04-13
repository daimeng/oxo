import sys
from numba import njit
import numpy as np
from .game import TicTacToe, print_board, pack
from .player import AiPlayer, Player, RandomPlayer, HumanPlayer
from .nnplayer import NnPlayer


@njit()
def train(game: TicTacToe, players: list[NnPlayer]):
    wins0 = 0
    wins1 = 0
    xp0: list[tuple[np.ndarray, int, float]] = [(np.zeros(9, dtype="int8"), 0, 0.0)]
    xp1: list[tuple[np.ndarray, int, float]] = [(np.zeros(9, dtype="int8"), 0, 0.0)]

    for _ in range(1000):
        for _ in range(1000):
            xp0.clear()
            xp1.clear()
            game.reset()
            done = False

            while not done:
                pnum = int(game.current_player_id != 1)
                player = players[pnum]

                state = game.board.copy()

                # get next experience
                action = player.request_move(game)
                reward = 0.0
                lreward = 0.0
                match game.make_move(action):
                    case 3:
                        reward = -1.0
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

                # which xp list to pull from
                xp = xp0 if pnum == 0 else xp1
                xplen = len(xp)

                qv = 0

                for i in range(xplen - 1, -1, -1):
                    state, action, reward = xp[i]

                    if isinstance(player, AiPlayer):
                        # ignore reward for now
                        player.update(state, action, reward + qv)

                    # compute next q values
                    X = state.reshape(1, 9).astype(np.float64)
                    qvalues, _, _, _ = player.forward(X)
                    qv = np.max(qvalues)

    return wins0, wins1


def main(opts):
    game = TicTacToe()
    trainPlayers: list[NnPlayer] = [NnPlayer(epsilon=0.5), NnPlayer(epsilon=0.5)]

    w0, w1 = train(game, trainPlayers)
    print(w0, w1)

    if "play" in opts or "play2" in opts:
        if "play" in opts:
            if isinstance(trainPlayers[0], AiPlayer):
                trainPlayers[0].epsilon = 0
            players: list[Player] = [trainPlayers[0], HumanPlayer()]
        else:
            if isinstance(trainPlayers[1], AiPlayer):
                trainPlayers[1].epsilon = 0
            players: list[Player] = [HumanPlayer(), trainPlayers[1]]

        for _ in range(1000):
            game.reset()

            while True:
                print_board(game.board)
                player = players[int(game.current_player_id != 1)]  # 1 -> 0, -1 -> 1
                cell = player.request_move(game)
                if game.make_move(cell) < 2:
                    break

    elif "test" in opts:
        if isinstance(trainPlayers[0], NnPlayer):
            trainPlayers[0].epsilon = 0
        players2: list[Player] = [trainPlayers[0], RandomPlayer()]
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

        if isinstance(trainPlayers[1], NnPlayer):
            trainPlayers[1].epsilon = 0
        players2: list[Player] = [RandomPlayer(), trainPlayers[1]]
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
