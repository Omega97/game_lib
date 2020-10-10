"""
    Policy

policy(state) -> GameAD


- must return a list describing probabilities for every move


Notes:
- the NN returns always an output of the same size
- it MUST be a non-normalized distribution (all values >= 0)
- all illegal moves are set to 0 (with clean_policy())


state; legal moves = [1, 4, 5]
policy -> [.1, .2, .3, .4, .5, .6]
clean -> [.1, 0., 0., .4, .5]

"""
import logging

if __name__ == "__main__":
    from state import State
    from action import Action, ActionDistribution
    from useful import regularizer
    from value_funciton import ValueFunction
else:
    from .state import State
    from .action import Action, ActionDistribution
    from .useful import regularizer
    from .value_funciton import ValueFunction


class Policy:
    """
    policy(GameState) -> ActionDistribution
    """
    def __init__(self, policy_fun):
        self.policy_fun = policy_fun     # state: GameState -> action distribution: ActionDistribution
        self.modifiers = []     # list -> list

    def __iter__(self):
        return iter(self.modifiers)

    def __call__(self, state: State) -> ActionDistribution:     # todo clean before?
        # compute initial output
        ad = self.policy_fun(state)

        # apply modifiers
        for f in self:
            ad.apply(f)

        return ad.clean()

    def apply(self, fun):
        """fun transforms the output of the initial function"""
        self.modifiers.append(fun)
        return self


# ---------------------------------------------


def value_fun_to_policy(value_fun: ValueFunction, k_reg=.99):
    """transform value function to policy by using regularization"""

    def get_score(state, index):
        """
        After player "p" choses a move, the new player is "q", while n is the number of players.
        The value of the position from the player q's point of view is:
        value_fun(updated_state)[(p - q) % n]

        :param state: current state
        :param index: coo of the move
        :return:
        """
        updated_state = state.get_updated(Action(index))

        n = type(state).number_of_players
        p = state.player
        q = updated_state.player

        i = (p - q) % n

        return value_fun(updated_state)[i]

    def policy_fun(state: State):   # modify moves instead of creating values
        """
        get all moves
        get the updated states and evaluate them
        return action distribution
        """
        moves = state.legal_moves()

        scores = [get_score(state, index) if value > 0 else 0.
                  for index, value in moves.iter_coo_value()]

        # logging.debug(state)
        # logging.debug([value for index, value in moves.iter_coo_value()])
        # logging.debug([round(i, 4) for i in scores])

        ad = state.action_distribution(scores)

        try:
            ad.assert_valid()
        except Exception as e:
            # logging.warn(e)
            pass

        ad.correct_invalid()

        return ad

    policy = Policy(policy_fun)
    policy.apply(regularizer(k_reg))

    return policy
