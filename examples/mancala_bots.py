"""
setup:
- reset all variables
- load NN

tear-down:
- delete tree
- save game
- trail NN

"""
from examples.mancala import GameState
from examples.agent_example import *
from match import Match
from agent import Agent
from policy import value_fun_to_policy
from value_funciton import ValueFunction
from useful import type_check, step


def neural_net_bot(k_reg=.99, name='nn bot'):

    class NNBot(Agent):
        def __init__(self):
            super().__init__(name)
            self.value_fun = None
            self.policy = None

        def enter(self):
            """load NN"""

            @type_check(list)
            def vf(v):
                assert type(v) == list
                out = round(step(k=1/10)(v[-1]), 5)
                return [out, 1-out]     # todo check

            self.value_fun = ValueFunction(vf)
            self.policy = value_fun_to_policy(self.value_fun, k_reg=k_reg)

        @type_check(Action)
        def move_out(self, state: GameState) -> Action:
            """return best move of best sub-state"""
            return self.policy(state).choose_action()

        def move_in(self, move: Action):
            ...

        @type_check(list)
        def evaluate_plain_state(self, state: GameState):
            return self.value_fun(state)

        def exit(self):
            """training"""
            ...

    return NNBot()


# -----------------------------------


def test_0():
    state = GameState()
    core = neural_net_bot()
    core.enter()
    print(core(state))


def test_1():
    state = GameState()
    match = Match(state, [random_agent(), random_agent()], do_show=True, trunc_percentage=1 / 20)
    match.play()


def test_2():
    state = GameState()
    match = Match(state, [neural_net_bot(), random_agent()], do_show=True, trunc_percentage=1 / 20)
    match.play()
    # for i in match.record:
    #     print(i)


def test_3():
    state = GameState([1, 5, 2, 0, 0,
                       1, 0, 0, 0, 0], handicap=-3)
    match = Match(state, [neural_net_bot(), random_agent()], do_show=True, trunc_percentage=1 / 20)
    match.play()
    # for i in match.record:
    #     print(i)


def test():
    state = GameState()
    match = Match(state, [neural_net_bot(), random_agent()], do_show=True, trunc_percentage=1 / 20)
    match.play()

    for player in (0, 1):
        print('\n')
        for i in match.get_data(player):
            print(i)

    match.plot()


if __name__ == '__main__':
    # from random import seed
    # seed(3)

    test_1()
