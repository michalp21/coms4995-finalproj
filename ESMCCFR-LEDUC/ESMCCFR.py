# from GameState import GameState
from GameState import GameState
from InfoSet import InfoSet
from Strategy import Strategy
from GameDefinition import GameDefinition
from GameSetup import GameSetup
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
	def __init__(self, deck_size):
		assert deck_size == 6 or deck_size == 52
		self.PLAYERS = [1,2]
		self.infoset_strategy_map = {}
		self.deck_size = deck_size

	def get_random_action(self, player_strategy):
		# return the index of the action the strategy chooses to take
		return random.choices(list(range(len(player_strategy))),
			weights=player_strategy, k=1)[0]

	def new_gamestate(self):
		# create a game in which "chance" has taken all actions, but the players will not be aware
		game_def = GameDefinition.leduc
		game_setup = GameSetup(small_blind=1, big_blind=2, stack_size=5)
		round = 0
		return GameState(game_definition=game_def, game_setup=game_setup, deal=game_def.deal())

	def run(self,T):
		utility = 0
		start = timeit.default_timer()

		printProgressBar(0, T)
		# conduct external-sampling Monte Carlo Counterfactual Regret
		for t in range(T):
			for player in self.PLAYERS:
				utility += self.traverse_ESMCCFR(self.new_gamestate(), player)
				printProgressBar(t+1, T)
		stop = timeit.default_timer()

		print("Time elapsed: %.2f" % (stop - start,))
		print("Average game value: %.4f" % (utility / T,))

		#Save Infosets
		with open('strategy.csv', 'w') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter = ',')

			infosets = [(k, v.calculate_strategy(), v.count, v.regret_sum) for k,v in self.infoset_strategy_map.items()]
			for i in infosets:
				csvwriter.writerow([i[0],i[1]])

		with open('strategy.pkl', 'wb') as pklfile:
			pickle.dump(self.infoset_strategy_map, pklfile, protocol=pickle.HIGHEST_PROTOCOL)

		return self.infoset_strategy_map

	def traverse_ESMCCFR(self, gamestate, player):

		if gamestate.is_terminal():
			return gamestate.get_utility(player)

		#default to chance player
		other_player = 3 - player
		player_turn = gamestate.get_players_turn()
		possible_actions = gamestate.get_possible_actions(player_turn)
		# Determine the strategy at this infoset
		infoset = gamestate.get_infoset(player_turn)
		if infoset in self.infoset_strategy_map.keys():
			strategy = self.infoset_strategy_map[infoset]
		else:
			strategy = Strategy(len(possible_actions))
			self.infoset_strategy_map[infoset] = strategy

		player_strategy = strategy.calculate_strategy()

		if player_turn == player:
			# initialize expected value
			# value of a node h is the value player i expects to achieve if all players play according to given strategy, having reached h
			value = 0
			value_action = [0] * len(player_strategy)
			for action_index, action in enumerate(possible_actions):
				# need to define adding an action to a history, make Action class
				prev_round = gamestate.round
				gamestate.update(player_turn, action)

				# Traverse each action (per iteration of loop) (each action changes the history)
				va = self.traverse_ESMCCFR(gamestate, player)
				gamestate.reverse_update(player_turn, action, prev_round)

				value_action[action_index] = va

				# Update the expected value
				value += player_strategy[action_index] * value_action[action_index]
			for action_index in range(len(possible_actions)):
				# Update the cumulative regret of each action
				strategy.regret_sum[action_index] += value_action[action_index] - value

			return value

		elif player_turn == other_player:
			# Sample one action and increment action counter
			action_index = self.get_random_action(player_strategy)
			action = possible_actions[action_index]
			strategy.count[action_index] += 1

			prev_round = gamestate.round
			gamestate.update(player_turn, action)
			val = self.traverse_ESMCCFR(gamestate, player)
			gamestate.reverse_update(player_turn, action, prev_round)
			return val
		else:
			raise Exception('How did we get here? There are no other players')

if __name__ == "__main__":
	# cProfile.runctx("ESMCCFR_P(100000)",globals(),locals())
	ESMCCFR_P = ESMCCFR_P(52)
	ESMCCFR_P.run(10000)