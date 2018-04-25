# from State import State
from State import State
from InfoSet import InfoSet
from Strategy import Strategy
from Rules import Rules
from Setup import Setup
from Utilities import *
from collections import defaultdict
import random
import cProfile
import timeit
from deuces2.card import Card
from deuces2.deck import Deck
import csv
import pickle

class ESMCCFR_P:
	def __init__(self, rules, setup):
		self.rules = rules
		self.setup = setup
		self.PLAYERS = [1,2]
		self.infoset_strategy_map = {}

	def get_random_bet(self, player_strategy):
		# return the index of the bet the strategy chooses to take
		return random.choices(list(range(len(player_strategy))),
			weights=player_strategy, k=1)[0]

	def new_game(self):
		round = 0
		return State(rules=self.rules, setup=self.setup, deal=self.rules.deal())

	def run(self,T):
		utility = 0
		start = timeit.default_timer()

		printProgressBar(0, T)
		# conduct external-sampling Monte Carlo Counterfactual Regret
		for t in range(T):
			for player in self.PLAYERS:
				utility += self.traverse_ESMCCFR(self.new_game(), player)
				printProgressBar(t+1, T)
		stop = timeit.default_timer()

		print("Time elapsed: %.2f" % (stop - start,))
		print("Average game value: %.4f" % (utility / T,))

		#Save Infosets
		with open('strategy.csv', 'w') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter = ',')

			infosets = [(k, v.calculate_strategy(), v.count, v.regret_sum) for k,v in self.infoset_strategy_map.items()]
			for i in infosets:
				csvwriter.writerow([i[0],[round(k, 3) for k in i[1]]])

		with open('strategy.pkl', 'wb') as pklfile:
			pickle.dump(self.infoset_strategy_map, pklfile, protocol=pickle.HIGHEST_PROTOCOL)

		return self.infoset_strategy_map

	def traverse_ESMCCFR(self, state, player):

		if state.is_terminal():
			return state.get_utility(player)

		#default to chance player
		other_player = 3 - player
		player_turn = state.get_players_turn()
		possible_bets = state.get_possible_bets()
		# Determine the strategy at this infoset
		infoset = state.get_infoset(player_turn)
		if infoset in self.infoset_strategy_map.keys():
			strategy = self.infoset_strategy_map[infoset]
		else:
			strategy = Strategy(len(possible_bets))
			self.infoset_strategy_map[infoset] = strategy

		player_strategy = strategy.calculate_strategy()

		if player_turn == player:
			# initialize expected value
			# value of a node h is the value player i expects to achieve if all players play according to given strategy, having reached h
			value = 0
			value_bet = [0] * len(player_strategy)
			for bet_index, bet in enumerate(possible_bets):
				# need to define adding an bet to a bets, make bet class
				memento = state.update(bet)

				# Traverse each bet (per iteration of loop) (each bet changes the bets)
				va = self.traverse_ESMCCFR(state, player)
				state.reverse_update(memento)

				value_bet[bet_index] = va

				# Update the expected value
				value += player_strategy[bet_index] * value_bet[bet_index]
			for bet_index in range(len(possible_bets)):
				# Update the cumulative regret of each bet
				strategy.regret_sum[bet_index] += value_bet[bet_index] - value

			return value

		elif player_turn == other_player:
			# Sample one bet and increment bet counter
			bet_index = self.get_random_bet(player_strategy)
			bet = possible_bets[bet_index]
			strategy.count[bet_index] += 1

			memento = state.update(bet)
			val = self.traverse_ESMCCFR(state, player)
			state.reverse_update(memento)
			return val
		else:
			raise Exception('How did we get here? There are no other players')

if __name__ == "__main__":
	# cProfile.runctx("ESMCCFR_P(100000)",globals(),locals())
	ESMCCFR_P = ESMCCFR_P(rules=Rules.leduc, setup=Setup(stack_size=5, big_blind=1, small_blind=1))
	ESMCCFR_P.run(10000)