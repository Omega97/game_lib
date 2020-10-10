if __name__ == "__main__":
    from state import *
else:
    from ..state import *


class GameState(State):
    """contains all info about a board state"""
    number_of_players = 2
    length = 4
    stones = 2
    squares = length * 2 + 2

    def __init__(self, board=None, player=0, plys=0, handicap=-.5):
        """

        :param board:
        :param player:
        :param plys:
        :param handicap:
        """
        super().__init__(board=board, player=player, plys=plys)
        self.handicap = handicap

        # draft variables
        self._switch = None
        self._still_playing = [True, True]

        if len(self.board) != GameState.squares:
            raise ValueError(f'Board must be of length {2 * (GameState.length + 1)}')

    def __len__(self):
        return self.length

    def _rotate(self, n):
        return self.player * (self.length + 1) + n

    def do_switch(self):
        return self._switch

    def resign(self, player_id):
        self._still_playing[player_id] = False

    def show(self, switch_side=True, side=None, width=3):
        """

        :param switch_side: the current player is always below
        :param side: this player is always below
        :param width:
        :return:
        """

        if switch_side:
            side = self.player

        your_side_is_playing = self.player == side

        n1 = 0
        n2 = len(self) + 1
        if side == 0:
            n1, n2 = n2, n1

        l1 = 'O' if side else '#'
        l2 = '#' if side else 'O'
        l1 += '  ' if your_side_is_playing else ' >'
        l2 += ' >' if your_side_is_playing else '  '
        l1 += '\t\t' + ' '.join([f'{i:>{width}}' for i in reversed(self[n1:n1 + len(self)])])
        l2 += '\t\t' + ' '.join([f'{i:>{width}}' for i in self[n2:n2 + len(self)]])

        bins = '\t  ' + f'{self[n1+len(self)]}' + ' '*(width*(self.length+2)+4) + f'{self[n2+len(self)]}'

        out = f'\n\n{self.compute_score():+.1f}' + '\t' * (width*3) + ' ' * 2 + f'{self.plys}' + '\n' * 2
        out += l1 + '\n'
        out += bins + '\n'
        out += l2 + '\n'

        return out

    def __iter__(self):
        return (i for i in range(GameState.length))

    def set_initial_state(self):
        self.board = ([GameState.stones] * GameState.length + [0]) * 2

    def compute_score(self):
        """at the end of the game the score is computed (score is NOT outcome)"""
        return self[len(self)] - self[-1] + self.handicap

    def plain_state(self) -> list:
        """
        :returns list that describes state of the board from perspective of the current player
        white_stones , black_stones , score
        """
        score = self.compute_score()
        score = round(score * 2)
        left = self.board[:len(self)]
        right = self.board[len(self)+1:-1]
        if self.player == 0:
            return left + right + [self.player] + [+score]  # first player
        else:
            return right + left + [self.player] + [-score]  # nero player

    def legal_moves(self):
        """all legal moves"""
        return self.action_distribution([1 if self[self._rotate(i)] > 0 else 0 for i in self])

    def switch_player(self):
        if self.do_switch():
            self.player = 1 - self.player

    def make_move(self, move_id):
        self._switch = None
        n0 = self._rotate(move_id)
        stones = self[n0]
        self[n0] = 0
        last = None
        for i in special_loop(start=n0, end=GameState.squares, length=stones):
            last = i  # optimize
            self[i] += 1
        self._switch = last != self._rotate(len(self))

    def is_game_over(self):
        if sum(self._still_playing) == 1:   # todo check
            return True
        return self.count_legal_moves() == 0

    def compute_outcome(self):
        """:return final score for each player"""
        if sum(self._still_playing) == 1:
            return [1 if i else 0 for i in self._still_playing]     # todo check
        score = self.compute_score()
        if score > 0:
            outcome = [1., 0.]
        elif score < 0:
            outcome = [0., 1.]
        else:
            outcome = [.5, .5]
        return outcome

    def make_sure_move_is_legal(self, move_id):
        if self.is_game_over():
            raise ValueError('applying move on a finished game')
        if not 0 <= move_id < len(self) + 1:
            raise IndexError(f'Make sure 0 <= n < {len(self) + 1}')
        stones = self[self._rotate(move_id)]
        if not stones:
            raise ValueError(f'Illegal move (square {move_id} has no stones)')


# ------------------------------------------
# ------------------------------------------


def special_loop(start, end, length):
    out = start
    count = length
    while count:
        out = (out + 1) % end
        if out != start:
            yield out
            count -= 1
