# from GameState import GameState
from GameState import GameState
from InfoSet import InfoSet
from Strategy import Strategy
from Enums import *
from Utilities import *
from collections import defaultdict
import random
import cProfile
import timeit
from deuces2.card import Card
from deuces2.deck import Deck
import csv

class ESMCCFR_P:
	def __init__(self):
		self.PLAYERS = [1,2]
		self.infoset_strategy_map = {}

	def get_random_action(self, player_strategy):
		# return the index of the action the strategy chooses to take
		return random.choices([i for i in range(len(player_strategy))], weights=player_strategy, k=1)[0]

	def initialize_gamestate(self):
		# create a game in which "chance" has taken all actions, but the players will not be aware
		deck = Deck()
		p1_cards = deck.draw(2)
		p2_cards = deck.draw(2)
		flop_cards = deck.draw(3)
		turn_card = deck.draw(1)
		river_card = deck.draw(1)
		gamestate = GameState(p1_cards, p2_cards, flop_cards, turn_card, river_card)
		return gamestate

	def run(self,T):
		util = 0
		start = timeit.default_timer()
		printProgressBar(0, T, prefix = ' Iter '+str(0)+"/"+str(T), suffix = 'Complete', length = 50)
		# conduct external-sampling Monte Carlo Counterfactual Regret
		for t in range(T):
			for player in self.PLAYERS:
				gamestate = self.initialize_gamestate()
				# g = GameStateK()
				# util += traverse_ESMCCFR_P(g, p, 1) if t > T//2 else traverse_ESMCCFR(g, p)
				util += self.traverse_ESMCCFR(gamestate, player)
				printProgressBar(t+1, T, prefix = ' Iter '+str(t)+"/"+str(T), suffix = 'Complete', length = 50)
		stop = timeit.default_timer()

		print("Time elapsed: " + str(stop-start))
		print("Average game value: " + str(util / T))

		#Save Infosets
		with open('strategy.csv', 'w') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter = ',')

			infosets = []
			for k,v in self.infoset_strategy_map.items():
				infosets.append((k,v.get_average_strategy(),v.count,v.regretSum))
			for i in infosets:
				csvwriter.writerow([i[0],i[1]])

	def traverse_ESMCCFR(self, gamestate, player):
		#default to chance player
		other_player = 2 if player == 1 else 1
		player_turn = gamestate.get_players_turn()
		possible_actions = gamestate.get_possible_actions(player_turn)
		strategy = Strategy(len(possible_actions))

		# print('player:', player, 'possible actions:', possible_actions)

		if gamestate.is_terminal():
			return gamestate.get_utility(player)

		elif player_turn == player:
			infoset = gamestate.get_infoset(player)

			# Determine the strategy at this infoset
			if infoset in self.infoset_strategy_map.keys():
				strategy = self.infoset_strategy_map[infoset]
			else:
				self.infoset_strategy_map[infoset] = strategy

			player_strategy = strategy.calculate_strategy(possible_actions)

			# initialize expected value
			# value of a node h is the value player i expects to achieve if all players play according to given strategy, having reached h
			value = 0
			value_action = [0]*len(player_strategy)
			for action in range(len(possible_actions)):

				# need to define adding an action to a history, make Action class
				# make sure to copy history and not change it if making multiple calls!
				g = gamestate.deepcopy()
				g.update(player, possible_actions[action])

				# Traverse each action (per iteration of loop) (each action changes the history)
				value_action[action] = self.traverse_ESMCCFR(g, player)

				# Update the expected value
				value += player_strategy[action] * value_action[action]

			for action in range(len(possible_actions)):
				# Update the cumulative regret of each action
				strategy.regretSum[action] += value_action[action] - value

			return value

		elif player_turn == other_player:
			infoset = gamestate.get_infoset(other_player)

			# Determine the strategy at this infoset
			if infoset in self.infoset_strategy_map.keys():
				strategy = self.infoset_strategy_map[infoset]
			else: self.infoset_strategy_map[infoset] = strategy

			player_strategy = strategy.calculate_strategy(possible_actions)

			# Sample one action and increment action counter
			action = self.get_random_action(player_strategy)
			strategy.count[action] += 1

			# Copy history, traverse one action
			g = gamestate.deepcopy()
			g.update(other_player, possible_actions[action])
			return self.traverse_ESMCCFR(g, player)

	def traverse_ESMCCFR_P(self, gamestate, player, p, C = -1000, K = 2):
		# C is a negative constant, paper does not provide any more information
		# K is a positive constant, paper does not provide any more information

		#default to chance player
		other_player = 0
		if player == 1:
			other_player = 2
		elif player == 2:
			other_player = 1
		player_turn = gamestate.get_players_turn()
		possible_actions = gamestate.get_possible_actions()

		if gamestate.is_terminal():
			return gamestate.get_utility(player)

		elif player_turn == player:
			infoset = gamestate.get_infoset(player)

			# Determine the strategy at this infoset
			strategy = self.infoset_strategy_map[infoset]
			player_strategy = strategy.calculate_strategy(possible_actions)

			# initialize expected value
			# value of a node h is the value player i expects to achieve if all players play according to given strategy, having reached h
			value = 0
			value_action = [0]*len(player_strategy)
			explored = [False]*len(player_strategy)
			for action in possible_actions:

				threshold = 1
				if strategy.regretSum[action] < C:
					threshold = max(0.02/p, K/(K+C-action_regret))

				if random.random() < threshold:
					g = gamestate.deepcopy()
					g.update(player, action)

					# Traverse each action (per iteration of loop) (each action changes the history)
					value_action[action] = self.traverse_ESMCCFR_P(g, player, p * min(threshold,1))
					explored[action] = True

					# Update the expected value
					value += player_strategy[action] * value_action[action]
				else:
					explored[action] = False

			for action in possible_actions:
				if explored[action]:
					strategy.regretSum[action] += value_action[action] - value

			return value

		elif player_turn == other_player:
			infoset = gamestate.get_infoset(other_player)

			# Determine the strategy at this infoset
			strategy = self.infoset_strategy_map[infoset]
			player_strategy = strategy.calculate_strategy(possible_actions)

			# Sample one action and increment action counter
			action = self.get_random_action(player_strategy)
			strategy.count[action] += 1/p

			# Copy history, traverse one action
			g = gamestate.deepcopy()
			g.update(other_player, action)
			return self.traverse_ESMCCFR(g, player)
		else:
			chance = 0

			# chance randomly selects a new card(s), note that chance updates differently
			# update needs to remove card from gamestate in HUNL
			action = ActionK.NEWCARD
			g = gamestate.deepcopy()
			g.update(chance, action)
			
			return self.traverse_ESMCCFR(g, player)

if __name__ == "__main__":
	# cProfile.runctx("ESMCCFR_P(100000)",globals(),locals())
	ESMCCFR_P = ESMCCFR_P()
	ESMCCFR_P.run(100)









