if __name__ == "__main__":
    from state import State
    from action import Action
    from agent import Agent
else:
    from ..state import State
    from ..action import Action
    from ..agent import Agent


def random_agent(name='random'):  # elo: 0
    """agent that makes random moves"""

    class RandomCore(Agent):
        def move_out(self, state: State) -> Action:
            return state.legal_moves().choose_action()

    return RandomCore(name)
