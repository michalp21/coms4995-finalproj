from deuces2.card import Card

from InfoSet import InfoSet
from Utilities import *

# A State tracks the progress of a game and can give information about it
# In particular, it can provide the infosets each player sees
class State:

	def __init__(self, rules, setup, deal):
		self.rules = rules
		self.setup = setup
		self.deal = deal

		self.round = 0
		self.player_turn = 2
		self.folded_player = 0

		self.big_contrib = self.setup.big_blind
		self.small_contrib = self.setup.small_blind

		self.bets = [[] for _ in range(self.rules.rounds)]

	def _other_player(self, player):
		return 3 - player

	def _my_contrib(self, player):
		return self.big_contrib if player == 1 else self.small_contrib

	def _increase_contrib(self, player, amount):
		if player == 1:
			self.big_contrib += amount
		else:
			self.small_contrib += amount

	def _other_contrib(self, player):
		return self._my_contrib(self._other_player(player))

	def __repr__(self):
		return ('%s, bets: %s, Round: %d' %
			(str(self.deal), repr_bets(self.bets), self.round))

	def get_possible_bets(self, pretty=False):
		player = self.player_turn

		debt = self._other_contrib(player) - self._my_contrib(player)
		remaining_chips = self.setup.stack_size - self._my_contrib(player)

		if debt == 0:
			check = 0
			call = -1
			fold = -1
		else:
			check = -1
			call = debt
			fold = 0

		if debt < remaining_chips:
			all_in = remaining_chips
		else:
			all_in = -1

		if player == 2 and self._my_contrib(player) == self.setup.small_blind:
			min_raise = call + self.setup.big_blind
		elif call == 0:
			min_raise = 1
		else:
			min_raise = 2 * call

		raises = list(range(min_raise, remaining_chips))

		if not pretty:
			return (([check] if check >= 0 else [])
			+ ([call] if call >= 0 else [])
			+ ([fold] if fold >= 0 else [])
			+ raises
			+ ([all_in] if all_in >= 0 else []))

		else:
			ret = dict()
			if check >= 0:
				ret['check'] = check
			if fold >= 0:
				ret['fold'] = 0
			if call >= 0:
				ret['call'] = call
			if len(raises) > 0:
				ret['raises'] = raises
			if all_in >= 0:
				ret['allIn'] = all_in
			return ret

	def get_infoset(self, player=0):
		return InfoSet(
			hole=self.deal.player(player if player > 0 else self.get_players_turn()),
			board=self.deal.board[0:self.round],
			bets=self.bets)

	def is_terminal(self):
		# there are 2 rounds, 0 and 1
		return (self.folded_player == 1 or self.folded_player == 2
			 or (self.big_contrib == self.small_contrib == self.setup.stack_size)
			 or self.round == self.rules.rounds)

	def get_utility(self, player):
		assert self.is_terminal()

		# cases where a player folded
		if self.folded_player == player:
			return -1 * self._my_contrib(player)
		elif self.folded_player == self._other_player(player):
			return self._other_contrib(player)

		# showdown cases
		result = self.rules.evaluate(self.deal)
		reverse_pov = 1 if player == 2 else -1
		if result == 0:
			return 0
		elif result > 0:
			return reverse_pov * self._other_contrib(player)
		else:
			return -1 * reverse_pov * self._my_contrib(player)


	def update(self, bet):
		memento = (self.player_turn, bet, self.round)
		player = self.player_turn
		assert self.folded_player == 0
		assert self._my_contrib(player) <= self._other_contrib(player)
		self.bets[self.round].append(bet)

		assert bet >= 0
		self._increase_contrib(player, bet)

		# on fold, remove player
		if self._my_contrib(player) < self._other_contrib(player):
			self.folded_player = player

		# on check or call, if not first bet in round, advance round
		elif self._my_contrib(player) == self._other_contrib(player) and len(self.bets[self.round]) > 1:
			self.round += 1
			self.player_turn = 1 if self.rules.switch else 2
		else:
			self.player_turn = self._other_player(player)

		return memento

	def reverse_update(self, memento):
		self.player_turn = memento[0]
		self._increase_contrib(self.player_turn, -1 * memento[1])
		self.round = memento[2]

		del self.bets[self.round][-1]
		self.folded_player = 0

	def get_players_turn(self):
		return self.player_turn
