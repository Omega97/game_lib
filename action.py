from copy import deepcopy

if __name__ == "__main__":
    from useful import choose, argmax
else:
    from .useful import choose, argmax


class Action:
    """
    An action is what transforms the state into a new state
    """

    def __init__(self, index):
        self.index = index  # can be tuple or int

    def __repr__(self):
        return f'Action({self.index})'

    def apply(self, state):
        """apply move, modify state"""
        state.make_move(self.index)
        state.update_plys()
        state.compute_outcome()
        return state

    def apply_on_copy(self, state):
        """apply move on copy, return copy"""
        new_state = deepcopy(state)
        return self.apply(new_state)

    def __call__(self, state):
        """make move, return evolved version of a copy of the state"""
        return self.apply_on_copy(state)


class ActionDistribution:
    """
    list of probabilities, each one associated to an action (normalization not required)
    """

    action_type = None

    def __init__(self, v: list, state):
        self.values = v     # can be numpy array or list
        self.state = state

    def __repr__(self):
        return f'ActionDistribution({self.get_values()})'

    # def __iter__(self):
    #     """iter over coo of all possible moves"""
    #     return iter(self.state)

    def get_values(self):
        return self.values

    def get_allowed_values(self):
        return [i for i in self.values if i > 0]

    def get_allowed_coo(self):
        coo = [val for n, val in enumerate(self.state) if self[n] > 0]
        assert len(coo) == len(self.get_allowed_values())
        return coo

    def iter_coo_value(self):
        """ yield (coo, value) for all possible coo """
        def f():
            i = 0
            for coo in self.state:
                yield (coo, self.values[i])
                i += 1
        return f()

    def number_of_allowed_moves(self):
        return len(self.get_allowed_values())

    def __getitem__(self, item: int):
        assert type(item) == int
        return self.values[item]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __len__(self):
        return len(self.values)

    def __mul__(self, other):
        assert type(other) == type(self)
        return ActionDistribution([self[i] * other[i] for i in range(len(self))], state=self.state)

    def choose_action(self) -> Action:
        """choose action at random"""
        self.correct_invalid()
        n = choose(self.get_allowed_values())
        return Action(self.get_allowed_coo()[n])

    def clean(self):
        """assert values >= 0 and all moves are legal"""
        legal = self.state.legal_moves()
        for i in range(len(self)):
            self[i] *= legal[i]
        return self

    def keep_best(self):
        max_ = max(self.get_allowed_values())
        for i, x in self:
            self[i] = x == max_
        return self

    def argmax(self):
        return argmax(self.get_allowed_values())

    def apply(self, fun):
        self.values = fun(self.get_values())    # todo get_allowed_values?

    def correct_invalid(self):
        for i in range(len(self)):
            if self[i] < 0:
                self[i] = 0
        if sum(self.get_values()) == 0:
            self.values = self.state.legal_moves().values

    def assert_valid(self):
        """True if every value is non-negative and at least one is positive"""
        for i in self.get_values():
            if i < 0:
                raise ValueError('An action distribution must not contain negative values!')
        if sum(self.get_values()) == 0:
            raise ValueError('An action distribution must not contain only zeros!')
