from libs.policy_lib import *
from main import GameState


def test_1():
    states = [GameState(),
              GameState([0, 0, 0, 0, 0, 2, 1, 0,
                         0, 0, 0, 2, 2, 0, 0, 0]),
              GameState([0, 0, 0, 0, 0, 2, 1, 0,
                         0, 0, 0, 2, 2, 0, 0, 0], player=1),
              ]

    policy = random_policy()

    for state in states:
        print(state)
        ad = policy(state)

        print(ad)
        print(ad.choose())


if __name__ == '__main__':
    test_1()
