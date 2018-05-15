from ESMCCFR import ESMCCFR_P
import random
import pickle
from Utilities import *
from StrategySaver import *
from Strategy import Strategy
from State import State
from Deal import Deal
from AvailableBets import AvailableBets


class ESMCCFRPlusTraining:

	def __init__(self, rules, setup, blueprint, abstracting=False):
		self.rules = rules
		self.setup = setup
		self.available_bets = AvailableBets(setup)
		self.is_small_blind = None
		# self.train(10000)
		self.abstracting = abstracting
		# self.strategy_map = pickle.load(open('strategy-smol.pkl', 'rb'))
		self.strategy_map = load(blueprint)
		self.surplus = 0
		print("Strategy map loaded")

	def _my_seat(self):
		return 2 if self.is_small_blind else 1

	def _opponent_seat(self):
		return 3 - self._my_seat()

	def _my_contrib(self):
		return self.state._my_contrib(self._my_seat())
	def _opponent_contrib(self):
		return self.state._other_contrib(self._my_seat())

	def new_game(self):
		self.state = State(self.rules, self.setup,
			Deal(rules=self.rules, big=[], small=[], board=[]))
		self.surplus = 0

	def take_seat(self, is_small_blind):
		self.is_small_blind = is_small_blind

	def receive_cards(self, cards):
		assert self.is_small_blind != None
		if self.is_small_blind:
			self.state.deal.small = cards
		else:
			self.state.deal.big = cards

	#actions params for easy integration with Contest.py
	def bet(self, actions_by_type=None, actions_by_numbers=None, state=None):
		if self.state.player_turn != self._my_seat():
			raise Exception('Player turn %d is wrong. I am %d.'
				% (self.state.player_turn, self._my_seat()))

		bet = self._select_bet()
		self.state.update(bet)
		return bet
	def _select_bet(self):

		infoset = self.state.get_infoset()

		if infoset in self.strategy_map.keys():
			bets = self.available_bets.get_bets_as_numbers(
				self._my_contrib(), self._opponent_contrib(), self.abstracting)
			strategy = self.strategy_map[infoset]
			print("  |",infoset)
			print("  |",bets)
			print("  |",self.available_bets.get_bets_by_action_type(
				self.state._my_contrib(self.state.player_turn),
				self.state._other_contrib(self.state.player_turn)))
			print("  |",strategy.get_average_strategy())
			player_strategy = strategy.get_average_strategy()
			return bets[random.choices(list(range(len(player_strategy))),weights=player_strategy, k=1)[0]]

		print("Notice: infoset %s not found; checking/calling" % str(infoset))
		actions = self.available_bets.get_bets_by_action_type(
			self.state._my_contrib(self.state.player_turn),
			self.state._other_contrib(self.state.player_turn),
			self.abstracting)
		return actions['call'][0] if 'call' in actions else actions['check'][0]

	def advance_round(self, cards):
		self.state.deal.board.append(cards)
		if self.state.round != len(self.state.deal.board):
			raise Exception('Wrong get_bets_as_numbers of rounds, deal: %s, round: %d'
				% (str(self.state.deal), self.state.round))

	def opponent_bets(self, bet):
		if self.state.player_turn != self._opponent_seat():
			raise Exception('Player turn %d is wrong. They are %d.'
				% (self.state.player_turn, self._opponent_seat()))

		if self.abstracting:
			opponent_bets_were = self.available_bets.get_bets_by_action_type(
				self._my_contrib(), self._opponent_contrib(), False)
			if bet in opponent_bets_were['raises']:
				bet = self._round_opponent_raise(bet, opponent_bets_were)

		self.state.update(bet)

	def train(self, T=2000):
		esmccfr = ESMCCFR_P(self.rules, self.setup)
		self.strategy_map = esmccfr.run(T)
		return self

	def _round_opponent_raise(self, bet, bets_were):
		assert bet in bets_were['raises']

		# If the bet is already even, return it without rounding
		if bet % 2 == 0:
			return bet

		# if decrementing the bet is not a raise, increment it, possibly  going
		# all in
		if not (bet - 1 in bets_were['raises']):
			surplus = surplus + 1
			return bet + 1

		# if decrementing the bet is a raise and incrementing is all in, raise
		if bet - 1 in bets_were['raises'] and not bet + 1 in bets_were['raises']:
			surplus = surplus - 1
			return bet - 1

		# if neither increment or decrement is a raise, prefer to round in the
		# direction that evens out the pot total overall
		if surplus == 0:
			surplus = surplus + 1
			return bet + 1
		elif surplus > 0:
			surplus = surplus - 1
			return bet - 1
		else:
			surplus = surplus + 1
			return bet + 1



	def __str__(self):
		return "EsmccfrBot\t"