from Evaluator import Evaluator
from InfoSet import InfoSet
from copy import deepcopy
from deuces2.card import Card

# A GameState tracks the progress of a game and can give information about it
# In particular, it can provide the infosets each player sees
class GameState:

	def __init__(self, p1_card, p2_card, flop_card):
		self.evaluator = Evaluator()
		self.players = set([1,2])
		self.p1_card = p1_card
		self.p1_is_in_game = True
		self.p2_is_in_game = True
		self.p2_card = p2_card
		self.flop_card = flop_card

		# original contribution is blinds. p1 goes first on every round except first one
		self.p1_contrib = 200
		self.p2_contrib = 100
		# stack size is always 2,000 (scale later), bet abstraction is 100 for now
		self._stack_size = 500
		self._bet_increment = 100

		# Keep track of what round of betting it is - 0 is preflop, 1 flop, 2 terminal
		self.round = 0

		# meta
		self.player_turn = 2
		self.actions = {0: [], 1: []}

	def _pot(self):
		return self.p1_contrib + self.p2_contrib

	def _other_player(self, player):
		return 3 - player

	def _my_contrib(self, player):
		return self.p1_contrib if player == 1 else self.p2_contrib

	def _other_contrib(self, player):
		return self._my_contrib(self._other_player(player))

	def _my_card(self, player):
		return self.p1_card if player == 1 else self.p2_card

	def _other_card(self, player):
		return self._my_card(self._other_player(player))

	def _my_hand_rank(self, player):
		return self.evaluator.evaluate(
			self.p1_card if player == 1 else self.p2_card, self.flop_card)

	def _other_hand_rank(self, player):
		return self._my_hand_rank(self._other_player(player))

	def __deepcopy__(self, memo):
		cls = self.__class__
		result = cls.__new__(cls)
		memo[id(self)] = result
		for k, v in self.__dict__.items():
			setattr(result, k, deepcopy(v, memo))
		return result

	def __repr__(self):
		hc = [Card.int_to_str(self.p1_card), Card.int_to_str(self.p2_card)]
		fc = [Card.int_to_str(self.flop_card)] if self.flop_card else ''
		return 'Hole Card: %s, Flop Card: %s' % (hc, fc) + ' Actions: ' + ':'.join(
			[','.join(str(h) for h in self.actions[k]) for k in sorted(self.actions)]) + 'Round:' + str(self.round)

	def deepcopy(self):
		# copy over the fields that change.
		# stack_size and bet_increment do not change within a run of ESMCCFR
		# cards and actions will reference the correct values by default which are set
		gamestate = GameState(self.p1_card, self.p2_card, self.flop_card)
		gamestate.players = deepcopy(self.players)
		gamestate.actions = deepcopy(self.actions)
		gamestate.p1_contrib = self.p1_contrib
		gamestate.p2_contrib = self.p2_contrib
		gamestate.round = self.round
		gamestate.player_turn = self.player_turn
		return gamestate

	def get_possible_actions(self, player):
		# returns a list of amounts of chips that can be added to pot in appropriate increments
		minimum = abs(self.p1_contrib - self.p2_contrib) // self._bet_increment
		maximum = (self._stack_size - min(self.p1_contrib, self.p2_contrib)) // self._bet_increment
		possible_actions = [b*self._bet_increment for b in range(minimum, maximum + 1)]
		# action of 0 when less than required amount will be a fold
		if minimum > 0:
			possible_actions.insert(0, 0)
		return possible_actions

	def get_infoset(self, player):
		return InfoSet(self, self._my_card(player))

	def is_terminal(self):
		return len(self.players) == 1 or self.round == 2

	def get_utility_folder(self, player):
		# print('folder!!!', self.round)
		# if p1 wins, p1 wins what p2 contributed and vice versa
		# if p1 loses, p1 loses what p1 contributed and vice versa
		if player in self.players:
			return self._other_contrib(player)
		else:
			return -1 * self._my_contrib(player)

	def get_utility_showdown(self, player):
		my_hand_rank = self._my_hand_rank(player)
		other_hand_rank = self._other_hand_rank(player)

		if my_hand_rank == other_hand_rank:
			return 0
		elif my_hand_rank < other_hand_rank:
			return self._other_contrib(player)
		else:
			return -1 * self._my_contrib(player)

	def get_utility(self, player):
		# print(self)
		if len(self.players) == 1:
			return self.get_utility_folder(player)
		else:
			return self.get_utility_showdown(player)


	def update(self, player, amount):
		# record player action
		self.actions[self.round].append(amount)

		# update player contributions
		if player == 1:
			self.p1_contrib += amount
		else:
			self.p2_contrib += amount

		# on fold, remove player
		if self._my_contrib(player) < self._other_contrib(player):
			self.players.remove(player)
			return

		# on check, if not first action in round, advance round
		if self._my_contrib(player) == self._other_contrib(player) and len(self.actions[self.round]) > 1:
			self.round += 1
			self.player_turn = 1 # player 2 goes first on the first round and player 1 goes first for every round after
		else:
			self.player_turn = self._other_player(player)

	def get_players_turn(self):
		return self.player_turn
