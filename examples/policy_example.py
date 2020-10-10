"""
Library of interesting policies

policy(state) -> GameAD


Note: make sure at least one legal move is suggested by the policy
"""
from policy import *
from examples.mancala import GameState


def random_policy():
    """random moves"""

    @Policy
    def _random_policy(state: GameState):
        board_size = len(state)
        return [1 for _ in range(board_size)]

    return _random_policy
