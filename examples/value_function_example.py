"""
A value function takes in a state and returns the expected value of the outcome of the game

Note: the ValueFunction class already takes care of the case when the game is over
"""
if __name__ == "__main__":
    from value_funciton import ValueFunction
else:
    from ..value_funciton import ValueFunction


def trivial_value_function():
    """return:
    - the result of the game in case of game-over
    - 0 otw
    """

    @ValueFunction
    def f(_):
        return 0

    return f
