from Evaluator import Evaluator
from InfoSet import InfoSet
from copy import deepcopy
from deuces2.card import Card

# A GameState tracks the progress of a game and can give information about it
# In particular, it can provide the infosets each player sees
class GameState:

	leduc = {
		'evaluator': Evaluator(),
		'small_blind': 100,
		'big_blind': 200,
		'stack_size': 500,
		'bet_increment': 100,
		'rounds': 2,
		'starting_player': 1,
		'switch_starting_player': False
	}

	def __init__(self, poker_config, p1_card, p2_card, flop):
		self.poker_config = poker_config
		self.evaluator = poker_config['evaluator']
		self.p1_contrib = poker_config['big_blind']
		self.p2_contrib = poker_config['small_blind']
		self.stack_size = poker_config['stack_size']
		self.bet_increment = poker_config['bet_increment']
		self.rounds = poker_config['rounds']
		self.round = 0
		self.starting_player = poker_config['starting_player']
		self.switch_starting_player = poker_config['switch_starting_player']

		self.folded_player = None
		self.p1_card = p1_card
		self.p2_card = p2_card
		self.flop = flop

		self.player_turn = poker_config['starting_player']
		self.history = {0: [], 1: []}

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

	def _my_card(self, player):
		return self.p1_card if player == 1 else self.p2_card

	def _other_card(self, player):
		return self._my_card(self._other_player(player))

	def _my_hand_rank(self, player):
		return self.evaluator.evaluate(
			self.p1_card if player == 1 else self.p2_card, self.flop)

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
		fc = [Card.int_to_str(self.flop)] if self.flop else ''
		return 'Hole Card: %s, Flop Card: %s' % (hc, fc) + ' Actions: ' + ':'.join(
			[','.join(str(h) for h in self.history[k]) for k in sorted(self.history)]) + 'Round:' + str(self.round)

	def deepcopy(self):
		# copy over the fields that change.
		# stack_size and bet_increment do not change within a run of ESMCCFR
		# cards and actions will reference the correct values by default which are set
		gamestate = GameState(self.poker_config, self.p1_card, self.p2_card, self.flop)
		gamestate.folded_player = self.folded_player
		gamestate.history = deepcopy(self.history)
		gamestate.p1_contrib = self.p1_contrib
		gamestate.p2_contrib = self.p2_contrib
		gamestate.round = self.round
		gamestate.player_turn = self.player_turn
		return gamestate

	def get_possible_actions(self, player):
		# returns a list of amounts of chips that can be added to pot in appropriate increments
		minimum = abs(self.p1_contrib - self.p2_contrib) // self.bet_increment
		maximum = (self.stack_size - min(self.p1_contrib, self.p2_contrib)) // self.bet_increment
		possible_actions = [b*self.bet_increment for b in range(minimum, maximum + 1)]
		# action of 0 when less than required amount will be a fold
		if minimum > 0:
			possible_actions.insert(0, 0)
		return possible_actions

	def get_infoset(self, player):
		return InfoSet(
			hole=(self._my_card(player),),
			board=((self.flop,),) if self.flop is not None else (),
			history=self.history)

	def is_terminal(self):
		# there are 2 rounds, 0 and 1
		return self.folded_player is not None or self.round == self.rounds

	def get_utility(self, player):
		assert self.is_terminal()
		my_hand_rank = self._my_hand_rank(player)
		other_hand_rank = self._other_hand_rank(player)

		# cases where a player folded
		if self.folded_player == player:
			return -1 * self._my_contrib(player)
		elif self.folded_player == self._other_player(player):
			return self._other_contrib(player)

		# showdown cases
		hand_rank_difference = self._my_hand_rank(player) - self._other_hand_rank(player)
		if hand_rank_difference == 0:
			return 0
		elif hand_rank_difference < 0:
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

	def get_players_turn(self):
		return self.player_turn
