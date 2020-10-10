from examples.mancala import *


def test_1():
    state = GameState(board=[0, 0, 0, 0, 1, 2, 1, 0,
                             0, 0, 0, 0, 1, 2, 1, 0])
    print(state)

    for i in [6, 5, 6, 4, 6, 5, 6, 4, 5, 5, 6]:
        state = Action(i)(state)
        if state.do_switch():
            print(state.show(switch_side=False, side=1-state.player))
        print(state.show())

    print(state.legal_moves())
    print(state.is_game_over())
    print(state.get_outcome())



def test_2():
    state = GameState()
    print(state)

    for i in [4, 6, 6]:
        state = Action(i)(state)
        if state.do_switch():
            print(state.show(switch_side=False, side=1-state.player))
        print(state.show())


def test_3():
    state = GameState(board=[0, 0, 0, 0, 1, 2, 1, 0,
                             0, 0, 0, 0, 1, 2, 1, 0])
    print(state.legal_moves())
    for i in state:
        print(i)
    for i in state.legal_moves():
        print(i)


if __name__ == '__main__':
    test_1()
