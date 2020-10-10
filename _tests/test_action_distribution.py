from state import ActionDistribution
from main import GameState


def test_1():
    ad = ActionDistribution([1, 2, 3])
    print(ad)
    print(ad.choose())


def test_2():
    state = GameState()
    ad = state.legal_moves()
    print(ad)
    print(ad.choose())




if __name__ == '__main__':
    test_2()
