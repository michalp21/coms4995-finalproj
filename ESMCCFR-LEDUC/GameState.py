from Evaluator import leduc_evaluate
from InfoSet import InfoSet
from copy import deepcopy
from deuces2.card import Card

from Utilities import *

# A GameState tracks the progress of a game and can give information about it
# In particular, it can provide the infosets each player sees
class GameState:

	leduc = {
		'evaluate': leduc_evaluate,
		'small_blind': 100,
		'big_blind': 200,
		'stack_size': 500,
		'bet_increment': 100,
		'rounds': 2,
		'starting_player': 1,
		'switch_starting_player': False
	}

	def __init__(self, poker_config, p1_hole, p2_hole, board):
		self.poker_config = poker_config
		self.evaluate = poker_config['evaluate']
		self.p1_contrib = poker_config['big_blind']
		self.p2_contrib = poker_config['small_blind']
		self.stack_size = poker_config['stack_size']
		self.bet_increment = poker_config['bet_increment']
		self.num_rounds = poker_config['rounds']
		self.round = 0
		self.starting_player = poker_config['starting_player']
		self.switch_starting_player = poker_config['switch_starting_player']

		self.folded_player = None
		self.p1_hole = p1_hole
		self.p2_hole = p2_hole
		self.board = board

		self.player_turn = poker_config['starting_player']
		self.history = {0: [], 1: []}

		assert len(self.board) == self.num_rounds - 1

	def _other_player(self, player):
		return 3 - player

	def _my_contrib(self, player):
		return self.p1_contrib if player == 1 else self.p2_contrib

	def _increase_contrib(self, player, amount):
		if player == 1:
			self.p2_contrib += amount
		else:
			self.p2_contrib += amount

	def _other_contrib(self, player):
		return self._my_contrib(self._other_player(player))

	def _my_hole(self, player):
		return self.p1_hole if player == 1 else self.p2_hole

	def _other_hole(self, player):
		return self._my_hole(self._other_player(player))

	def __repr__(self):
		return 'Hole 1: %s, Hole 2: %s, Board: %s, Actions: %s, Round: %d' % (
			repr_hole(self.p1_hole), repr_hole(self.p2_hole),
			repr_board(self.board), repr_history(self.history), self.round)

	def get_possible_actions(self, player):
		# returns a list of amounts of chips that can be added to pot in appropriate increments
		minimum = self._other_contrib(player) - self._my_contrib(player)
		maximum = self.stack_size - self._my_contrib(player)
		return ([] if minimum == 0 else [0]) + list(range(minimum, maximum + 1, self.bet_increment))

	def get_infoset(self, player):
		return InfoSet(
			hole=self._my_hole(player),
			board=self.board[0:self.round],
			history=self.history)

	def is_terminal(self):
		# there are 2 rounds, 0 and 1
		return self.folded_player is not None or self.round == self.num_rounds

	def get_utility(self, player):
		assert self.is_terminal()

		# cases where a player folded
		if self.folded_player == player:
			return -1 * self._my_contrib(player)
		elif self.folded_player == self._other_player(player):
			return self._other_contrib(player)

		# showdown cases
		result = self.evaluate(self.p1_hole, self.p2_hole, self.board)
		if result == 0:
			return 0
		elif result > 0:
			return self._other_contrib(player)
		else:
			return -1 * self._my_contrib(player)


	def update(self, player, amount):
		assert self.folded_player is None
		self.history[self.round].append(amount)

		self._increase_contrib(player, amount)

		# on fold, remove player
		if self._my_contrib(player) < self._other_contrib(player):
			self.folded_player = player
			return

		# on check, if not first action in round, advance round
		if self._my_contrib(player) == self._other_contrib(player) and len(self.history[self.round]) > 1:
			self.round += 1
			self.player_turn = (self._other_player(self.starting_player)
			 if self.switch_starting_player else self.starting_player)
		else:
			self.player_turn = self._other_player(player)

	def reverse_update(self, player, amount, round):
		self.round = round
		self.history[self.round].pop()
		self._increase_contrib(player, -1 * amount)
		self.folded_player = None
		self.player_turn = player

	def get_players_turn(self):
		return self.player_turn
