"""
Match between multiple agents
"""
import logging
import os
import pickle
from matplotlib import pyplot as plt
from numpy import array

if __name__ == '__main__':
    from state import State
    from useful import now_string, shift, loop_range
else:
    from .state import State
    from .useful import now_string, shift, loop_range


class Match:
    def __init__(self, state: State, agents: list, do_show=False,
                 do_record=True, trunc_percentage=0, max_depth=None):

        # game-related
        self.state = state
        self.agents = agents
        self.game = type(state)
        self.depth = 0
        self.record = []
        self._last_move = None
        self.values = None

        # settings
        self.do_show = do_show
        self.do_record = do_record
        self.resign_threshold = trunc_percentage
        self.max_depth = max_depth

        assert len(self.agents) == type(state).number_of_players

    def set_outcome(self, outcome):
        self.state.outcome = outcome

    def get_outcome(self):
        return self.state.outcome

    def get_plys(self):
        return self.state.plys

    def get_player(self):
        return self.state.player

    def player_picks_move(self):
        """
        pick the current player
        git the move it wants to play
        """
        self.state.legal_moves().assert_valid()
        agent = self.agents[self.get_player()]
        self._last_move = agent(self.state)
        # logging.info(f"player {self.get_player()}'s move: {self._last_move}")
        self.depth += 1

    def compute_cross_value_matrix(self):
        """"""
        n_players = len(self.agents)
        self.values = [self.agents[i].evaluate_plain_state(self.state) for i in range(n_players)]

    def update_record(self):
        """add data to record"""
        assert self.values is not None
        if self.do_record:
            self.record += [{'board': self.state.plain_state(),
                             'player': self.get_player(),
                             'move': self._last_move,
                             'ply': self.get_plys(),
                             'values': self.values,
                             }]
            self.values = None

    def distribute_move(self):
        """tell to every agent what move has been played"""
        for c in self.agents:
            c.move_in(self._last_move)

    def update_state(self):
        """apply last move on current state, then set outcome in case the game is over"""
        self.state = self._last_move(self.state)
        if self.state.is_game_over():
            self.set_outcome(self.state.compute_outcome())

    def trunc_by_low_expected_outcome(self):
        """trunc if expected outcome extremely low
        If all players but one have expected outcome below resign_threshold then:
        - the game is over
        - that one player wins
        - the outcome is set to average expectation values over all players
        """
        assert self.values is not None

        if self.resign_threshold is not None:
            player = self.get_player()
            if self.values[player] is not None:
                value = self.values[player][0]
                if value is not None:
                    # logging.info(f" {player}'s value = {value:.3f}")
                    if value < self.resign_threshold:
                        self.state.still_playing[player] = False
                    if sum(self.state.still_playing) == 1:
                        self.set_outcome(self.state.compute_outcome_after_resignation())
                        # logging.info(f'GAME TRUNCATED, resignation: '
                        #              f'{value:.3f} < {self.resign_threshold:.3f} outcome = {self.get_outcome()}')
                        if self.do_show:
                            print(f'\n Win by resignation ({value*100:.1f}%) \n')

    def trunc_by_exceeding_length(self):
        """trunc game by exceeding length, draw"""
        if self.max_depth is not None:
            if self.depth + 1 >= self.max_depth:
                self.set_outcome(self.state.compute_outcome_forced_draw())
                if self.do_show:
                    print('\n Draw by exceeding length \n')
                # logging.info(f'GAME TRUNCATED, exceeding length: '
                #              f'outcome = {self.get_outcome()}')

    def get_data(self, player_id):
        """
        get data from record
        - ply: move id
        - board: plain state from current player's perspective, list
        - value: expectation values of all players from # todo
        """
        return [{'ply': d['ply'],
                 'board': d['board'],
                 'value': d['values'][player_id],
                 }
                for d in self.record if d['player'] == player_id]

    def plot(self, ylim=None):
        """plot expectation values during match for all players"""
        if self.do_record:
            for player in range(len(self.agents)):
                data = self.get_data(player)

                if data[0]['value'] is not None:
                    x = [i['ply'] for i in data]
                    y = [i['value'][player] for i in data]
                    plt.plot(x, y)
                else:
                    plt.plot([], [])

            plt.title('Winrate')
            plt.legend([i.name for i in self.agents])
            plt.ylim(ylim if ylim is not None else [0, 1])
            plt.show()

    def run_core_enter(self):
        """run .enter() method for all cores"""
        for core in self.agents:
            core.enter()

    def run_core_exit(self):
        """run .exit() method for all cores"""
        for core in self.agents:
            core.exit()

    def show(self):
        """print game state"""
        if self.do_show:
            self.compute_cross_value_matrix()
            if self.values is not None:
                try:
                    print(f'\n exp = {self.values[self.get_player()][0]:.2f}')
                except TypeError:
                    pass
            print(self.state.show())
            self.values = None

    def main_game_sequence(self):
        ...

    def main_sequence(self):
        """this methods get called in order"""
        methods = [self.show,
                   self.trunc_by_exceeding_length,
                   self.compute_cross_value_matrix,   # move is chosen and distributed to players
                   self.trunc_by_low_expected_outcome,
                   self.player_picks_move,
                   self.update_record,
                   self.distribute_move,
                   self.update_state  # only now, state is updated
                   ]
        for n in loop_range(len(methods)):
            yield methods[n]

    def main_game_loop(self):
        """
        play a game until:
        - the end
        - length exceeds limit
        - all players but one resigned  # todo ?
        """
        for method in self.main_sequence():
            method()
            if self.get_outcome() is not None:
                break

        self.compute_cross_value_matrix()   # todo ?
        self.update_record()

    def play(self):
        """
        context manager-like method to play the game
        - prepare everything
        - actual game
        - close everything
        """
        self.run_core_enter()
        self.main_game_loop()
        self.show()     # todo move elsewhere
        self.run_core_exit()
        # logging.debug(self.state)
        # logging.info(f'outcome = {self.get_outcome()}')
        return self.get_outcome()

    def get_game_data_for_player(self, player):
        """generator of dicts of board, player, values
        note: values are subjective, i.e. the order depends on who is playing"""
        for d in self.record:
            values = d['values'][player]
            if values is not None:
                yield {'board': d['board'],
                       'player': d['player'],
                       'ply': d['ply'],
                       'values': values,
                       }

    def get_modified_data_for_player(self, player, k):    # todo check multiplayer
        """add outcome influence and next-state-infuence"""
        old = None
        new = None
        for d in self.get_game_data_for_player(player):
            old, new = new, d
            if old is not None:
                yield improve_data(old, new, outcome=self.get_outcome(), n_turns=self.get_plys(), k=k)
        yield improve_data(new, new, outcome=self.get_outcome(), n_turns=self.get_plys(), k=k)

    def save_data_for_player(self, path, k=10, player=0):
        """ save data of the game for traning
        board plain-state, value

        :param player: 0, 1, ...
        :param path: .pkl
        :param k: at k steos before the end the difference between the values and outcome is cut in half
        """

        new_data = list(self.get_modified_data_for_player(player, k))

        try:
            with open(path, 'rb') as file:
                old_data = pickle.load(file)
        except FileNotFoundError:
            old_data = []
        except EOFError:
            old_data = []

        with open(path, 'wb') as file:
            pickle.dump(old_data + new_data, file)

    def save_data_for_all_players(self, path, k):
        """ save data of the game for traning
        board plain-state, value

        :param path: .pkl
        :param k: at k steos before the end the difference between the values and outcome is cut in half
        """
        data = []

        for i in range(type(self.state).number_of_players):
            data += list(self.get_modified_data_for_player(i, k))

        with open(path, 'wb') as file:
            pickle.dump(data, file)


# ------------------------------------------------------------------


def improve_data(old_dct, new_dct, outcome, n_turns, k):
    """modifies data taking into account next move and final result"""

    n_to_end = n_turns - old_dct['ply']
    current_player = old_dct['player']
    next_player = new_dct['player']

    next_val = array(shift(new_dct['values'], n=current_player - next_player))
    outcome_val = array(shift(outcome, n=current_player))

    backup = old_dct['values'][0]
    old_dct['values'] = list(next_val + (outcome_val - next_val) * 2 ** (-n_to_end / k))

    return {'x': old_dct['board'],
            'y': old_dct['values'][0],
            'backup': backup}


def training_data_from_match(state, agent, data_path='data.pkl', k_signal=10,
                             resignation_score=None, max_game_length=None):
    """
    generate a game
    save a data batch in file
    data: plain_state, value

    :param agent: function(plain_state: list) -> value: float
    :param data_path: .pkl
    :param k_signal: propagate outcome backwards
    :param resignation_score: agent resigns if expectation value is too low
    :param max_game_length: truncate too long games
    :return:
    """
    agents = [agent, agent]
    match = Match(state, agents,
                   do_show=False,
                   trunc_percentage=resignation_score,
                   max_depth=max_game_length)
    match.play()
    match.save_data_for_player(data_path, k_signal)
