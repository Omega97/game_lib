"""
An Agent takes in input a State and returns an action
"""
if __name__ == "__main__":
    from state import State
    from action import Action
    from policy import Policy, value_fun_to_policy
    from useful import keep_best
    from value_funciton import ValueFunction
else:
    from .state import State
    from .action import Action
    from .policy import Policy, value_fun_to_policy
    from .useful import keep_best
    from .value_funciton import ValueFunction


class Agent:

    def __init__(self, name=None, value_function=None):
        self.name = name
        self.value_fun = value_function
        self.value_fun = None
        self.policy = None
        self.fast_policy = None
        self.tree_search = None

    def __call__(self, state: State) -> Action:
        """pick move"""
        return self.move_out(state)

    def __repr__(self):
        return f'Agent {self.name}' if self.name else 'Agent'

    def evaluate_plain_state(self, plain_state: list):
        if self.value_fun:
            return self.value_fun(plain_state)

    def move_out(self, state: State) -> Action:
        """ choose the move to play
        IMPORTANT: just choose the move don't modify any tree or anything
        """
        raise NotImplementedError

    def move_in(self, move: Action):
        """ update the tree (or whaterver structure you use) given that 'move' was played """
        pass

    def enter(self):
        """set-up: load stuff before the game begins"""
        pass

    def exit(self):
        """tear-down: things you might want to do after the game ends"""
        pass


# ----------------------------------------------------------------
#                           CONVERTERS
# ----------------------------------------------------------------


def policy_to_agent(policy: Policy, name='policy core'):
    """use the policy to decide the move"""

    class Search(Agent):
        def move_out(self, state: State) -> Action:
            return policy(state).choose_action()

    return Search(name)


def value_function_agent(value_fun: ValueFunction, k_reg=.99, name='value core'):
    """transform value function into an agent by using regularization"""
    return policy_to_agent(policy=value_fun_to_policy(value_fun, k_reg=k_reg), name=name)


def keep_best_of_policy_to_agent(policy: Policy, name='argmax agent'):
    """transform value function into an agent by using argmax"""
    return policy_to_agent(policy=policy.apply(keep_best), name=name)
