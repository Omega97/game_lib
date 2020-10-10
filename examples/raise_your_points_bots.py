"""
policy must return AD (manage that)
"""
from policy import Policy
from agent import keep_best_of_policy_to_agent
from main import GameState
from match import Match
from libs.agent_lib import random_core


def human_policy():
    """the user is required to input moves"""

    @Policy
    def _human_policy(state: GameState):
        while True:
            legal = state.legal_moves()
            c = input('\n input move > ')
            if c in ('+', '2'):
                if legal[1]:
                    return state.action_distribution([0, 1])
            if c in ('-', '1'):
                if legal[0]:
                    return state.action_distribution([1, 0])

    return _human_policy


def human_core(name='human'):
    """human picks the moves from console"""
    return keep_best_of_policy_to_agent(human_policy(), name=name)


def test():
    state = GameState()
    match = Match(state, [random_core(), random_core(), random_core()], do_show=True)
    match.play()


if __name__ == '__main__':
    test()
