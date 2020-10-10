if __name__ == "__main__":
    from useful import type_check
else:
    from .useful import type_check


class ValueFunction:

    def __init__(self, fun):
        """Used to truncate roll-outs, saves computational power
        When called, takes as input a state and returns the expectation value
        of the outcome for each player from the point of view of the current player

        :param fun: makes the evaluation of the expected outcome of the game, plain state -> float
        """
        self.fun = fun

    @type_check(list)
    def __call__(self, state) -> list:
        """ evaluate state with value function if not game over, else return outcome
        uses original order of the players

        :param state: state
        :return: list of expectation values (one per player)
        """
        if state.is_game_over():
            v = state.get_outcome()  # objective
            return [v[(i + state.player) % len(v)] for i in range(len(v))]  # subjective
        else:
            return self.fun(state.plain_state())    # subjective
