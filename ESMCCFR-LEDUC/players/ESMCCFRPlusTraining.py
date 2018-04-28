from ESMCCFR import ESMCCFR_P
import random
from Strategy import Strategy
from State import State
from Deal import Deal
from AvailableBets import AvailableBets


class ESMCCFRPlusTraining:

	def __init__(self, rules, setup):
		self.rules = rules
		self.setup = setup
		self.available_bets = AvailableBets(setup)
		self.is_small_blind = None

	def new_game(self):
		self.state = State(self.rules, self.setup, Deal(big=[], small=[], board=[]))

	def take_seat(self, is_small_blind):
		self.is_small_blind = is_small_blind

	def receive_cards(self, cards):
		assert self.is_small_blind != None
		if self.is_small_blind:
			self.state.deal.small = cards
		else:
			self.state.deal.big = cards

	def bet(self, actions):
		if (self.state.player_turn == 2) != self.is_small_blind:
			raise Exception('Player turn is wrong. I am small: %s, player turn: %d'
				% (str(self.is_small_blind), self.state.player_turn))

		bets = self.available_bets.get_bets_as_numbers(
			self.state._my_contrib(self.state.player_turn),
			self.state._other_contrib(self.state.player_turn))

		if bets != [v for val in actions.values() for v in val]:
			raise Exception('Internal bets <%s> are not input bets <%s>'
				% (bets, actions))

		infoset = self.state.get_infoset()
		print(str(self.is_small_blind) + " " + str(infoset))

		if infoset not in self.strategy_map.keys():
			raise Exception('We are not fully trained on %s' % str(infoset))

		strategy = self.strategy_map[infoset]
		player_strategy = strategy.calculate_strategy()

		bet = bets[random.choices(list(range(len(player_strategy))),
			weights=player_strategy, k=1)[0]]

		self.state.update(bet)
		return bet

	def advance_round(self, cards):
		self.state.deal.board.append(cards)
		if self.state.round != len(self.state.deal.board):
			raise Exception('Wrong get_bets_as_numbers of rounds, deal: %s, round: %d'
				% (str(self.state.deal), self.state.round))

	def opponent_bets(self, bet):
		if (self.state.player_turn == 1) != self.is_small_blind:
			raise Exception('Opponent turn is wrong. I am small: %s, player turn: %d'
				% (str(self.is_small_blind), self.state.player_turn))
		self.state.update(bet)

	def train(self, T=10000):
		esmccfr = ESMCCFR_P(self.rules, self.setup)
		self.strategy_map = esmccfr.run(T)
		return self

	def __str__(self):
		return "EsmccfrBot\t"