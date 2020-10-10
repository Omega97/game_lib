"""
A State represents the actual information of a board position
"""
from copy import deepcopy

if __name__ == "__main__":
    from action import ActionDistribution
else:
    from .action import ActionDistribution


class State:

    number_of_players = None

    def __init__(self, board=None, player=None, plys=0):
        """
        :param board: all info that you need to describe a board state, except the following
        :param player: current player
        :param plys: number of moves made
        """
        if type(self).number_of_players is None:
            raise ValueError('Please specify the number_of_players')
        self.board = board
        self.player = player
        self.plys = plys
        self.outcome = None
        self.still_playing = [True for _ in range(type(self).number_of_players)]
        if self.board is None:
            self.set_initial_state()

    def __iter__(self):
        """iterate over all indices of possible moves, yield tuples"""
        raise NotImplementedError

    def __getitem__(self, item):
        return self.board[item]

    def __setitem__(self, key, value):
        self.board[key] = value

    def update_plys(self):
        self.plys += 1

    def get_updated(self, action):
        return action(deepcopy(self))

    def get_outcome(self):
        """return outcome if game is over, else None"""
        if self.outcome is not None:
            return self.outcome
        else:
            if self.is_game_over():
                self.outcome = self.compute_outcome()
                return self.outcome

    def action_distribution(self, values):
        return ActionDistribution(values, state=self)

    def count_legal_moves(self):
        return self.legal_moves().number_of_allowed_moves()

    def resign(self, player_id):
        """player 'player_id' is no more willing to play
        if all players but one resign then that player is winner"""
        self.still_playing[player_id] = False
        if sum(self.still_playing) == 1:
            self.compute_outcome_after_resignation()

    def __hash__(self):
        """hash of state, overwrite if necessary"""
        s = str(self.board) + ' '
        s += str(self.player) + ' '
        s += str(self.plys) + ' '
        return hash(s)

    def show(self, *kw) -> str:
        """return string that represents state
        possibly use variables to tweak the representation"""
        raise NotImplementedError

    def __repr__(self):
        return self.show()

    def set_initial_state(self):
        """set .board to initial conditions """
        raise NotImplementedError

    def plain_state(self) -> list:
        """
        :returns list that describes state of the board from perspective of the current player
        white_stones , black_stones , score"""
        raise NotImplementedError

    def legal_moves(self) -> ActionDistribution:
        """return ActionDistribution of legal moves"""
        raise NotImplementedError

    def switch_player(self):
        """here .player is updated after ply ends"""
        self.player = (self.player + 1) % self.number_of_players

    def make_move(self, move_id):
        """modify the board info according to the move that has been chosen
        suggestion: assert move is legal
        note: remember to .switch_player()"""
        raise NotImplementedError

    def is_game_over(self) -> bool:
        """return True if game is over, else False"""
        raise NotImplementedError

    def compute_outcome(self) -> list:
        """compute outcome of the game, one value per each player"""
        raise NotImplementedError

    def compute_outcome_after_resignation(self) -> list:
        """compute outcome after all players but 1 resigned
        overwrite if necessary"""
        return [1 if i else 0 for i in self.still_playing]

    def compute_outcome_forced_draw(self) -> list:
        n = self.number_of_players
        return [1/n for _ in range(n)]

    def make_sure_move_is_legal(self, move_id) -> bool:
        pass
