"""
- every player starts from 0 points
- each round you can either increase them by 1
- each round you can either decrease them by 1 up to 0
- first player that reaches the goal score wins
"""
from state import *
from useful import shift_range


class GameState(State):
    """contains all info about a board state"""

    number_of_players = 3
    goal = 5

    def __init__(self, board=None, player=0):
        super().__init__(board=board, player=player)
        self._still_playing = [True for _ in range(GameState.number_of_players)]

    def __len__(self):
        return GameState.number_of_players

    def resign(self, player_id):
        self._still_playing[player_id] = False

    def show(self):
        return '\n' + '\n'.join([str(i) for i in self.board])

    def __iter__(self):
        return (i for i in range(2))

    def set_initial_state(self):
        self.board = [0 for _ in range(len(self))]

    def plain_state(self) -> list:
        """
        :returns list that describes state of the board from perspective of the current player
        white_stones , black_stones , score
        """
        return [self.board[i] for i in shift_range(len(self), self.player)]

    def legal_moves(self):
        """all legal moves"""
        v = [1, 1] if self.board[self.player] > 0 else [0, 1]
        return self.action_distribution(v)

    def switch_player(self):
        self.player = (self.player + 1) % len(self)

    def make_move(self, move_id):
        self.board[self.player] += 1 if move_id == 1 else -1
        assert self.board[self.player] >= 0

    def is_game_over(self):
        for i in range(len(self)):
            if self.board[i] >= GameState.goal:
                return True
        return False

    def compute_outcome(self):
        """:return final score for each player"""
        max_ = max(self.board)
        return [1 if i == max_ else 0 for i in range(len(self))]

    def make_sure_move_is_legal(self, move_id):
        return True
