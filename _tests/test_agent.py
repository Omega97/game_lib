from examples.agent_example import random_agent
from match import Match
from examples.mancala import GameState


def test_1():
    state = GameState()
    core = random_agent()
    print(core(state))


def test_2():
    state = GameState()
    agents = [random_agent(), random_agent()]
    match = Match(state=state, agents=agents, do_show=True)
    match.play()


if __name__ == '__main__':
    test_2()
