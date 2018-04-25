from deuces2.card import Card

from InfoSet import InfoSet
from Utilities import *

# A GameState tracks the progress of a game and can give information about it
# In particular, it can provide the infosets each player sees
class GameState:

	def __init__(self, game_definition, game_setup, deal):
		self.game_def = game_definition
		self.game_setup = game_setup
		self.deal = deal

		self.round = 0
		self.player_turn = 2
		self.folded_player = 0

		self.p1_contrib = self.game_setup.big_blind
		self.p2_contrib = self.game_setup.small_blind

		self.history = [[] for _ in range(self.game_def.rounds)]

	def _other_player(self, player):
		return 3 - player

	def _my_contrib(self, player):
		return self.p1_contrib if player == 1 else self.p2_contrib

	def _increase_contrib(self, player, amount):
		if player == 1:
			self.p1_contrib += amount
		else:
			self.p2_contrib += amount

	def _other_contrib(self, player):
		return self._my_contrib(self._other_player(player))

	def __repr__(self):
		return ('%s, Actions: %s, Round: %d' %
			(str(self.deal), repr_history(self.history), self.round))

	def get_possible_actions(self, player):

		# returns a list of amounts of chips that can be added to pot in appropriate increment
		call = self._other_contrib(player) - self._my_contrib(player)
		remaining_chips = self.game_setup.stack_size - self._my_contrib(player)
		if self._my_contrib(player) == self.game_setup.small_blind:
			min_raise = self.game_setup.small_blind + self.game_setup.big_blind
		elif call == 0:
			min_raise = 1
		else:
			min_raise = min(call + call, remaining_chips)

		if call == 0:
			return [0] + list(range(min_raise, remaining_chips + 1))
		else:
			return [0, call] + list(range(min_raise, remaining_chips + 1))

	def get_infoset(self, player):
		return InfoSet(
			hole=self.deal.player(player),
			board=self.deal.board[0:self.round],
			history=self.history)

	def is_terminal(self):
		# there are 2 rounds, 0 and 1
		return (self.folded_player == 1 or self.folded_player == 2
			 or (self.p1_contrib == self.p2_contrib == self.game_setup.stack_size)
			 or self.round == self.game_def.rounds)

	def get_utility(self, player):
		assert self.is_terminal()

		# cases where a player folded
		if self.folded_player == player:
			return -1 * self._my_contrib(player)
		elif self.folded_player == self._other_player(player):
			return self._other_contrib(player)

		# showdown cases
		result = self.game_def.evaluate(self.deal)
		if result == 0:
			return 0
		elif result > 0:
			return self._other_contrib(player)
		else:
			return -1 * self._my_contrib(player)


	def update(self, player, amount):
		assert self.folded_player == 0
		assert self._my_contrib(player) <= self._other_contrib(player)
		self.history[self.round].append(amount)

		assert amount >= 0
		self._increase_contrib(player, amount)

		# on fold, remove player
		if self._my_contrib(player) < self._other_contrib(player):
			self.folded_player = player
			return

		# on check, if not first action in round, advance round
		if self._my_contrib(player) == self._other_contrib(player) and len(self.history[self.round]) > 1:
			self.round += 1
			self.player_turn = 1 if self.game_def.switch else 2
		else:
			self.player_turn = self._other_player(player)

	def reverse_update(self, player, amount, round):
		self.round = round
		del self.history[self.round][-1]
		self._increase_contrib(player, -1 * amount)
		self.folded_player = 0
		self.player_turn = player

		assert self._my_contrib(player) <= self._other_contrib(player)

	def get_players_turn(self):
		return self.player_turn
