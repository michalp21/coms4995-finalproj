# from GameState import GameState
from GameState import GameState
from InfoSet import InfoSet
from Strategy import Strategy
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
	def __init__(self):
		self.PLAYERS = [1,2]
		self.infoset_strategy_map = {}

	def get_random_action(self, player_strategy):
		# return the index of the action the strategy chooses to take
		return random.choices([i for i in range(len(player_strategy))], weights=player_strategy, k=1)[0]

	def initialize_gamestate(self):
		# create a game in which "chance" has taken all actions, but the players will not be aware
		deck = Deck()
		p1_card = deck.draw(1)
		p2_card = deck.draw(1)
		flop_card = deck.draw(1)
		gamestate = GameState(poker_config=GameState.leduc,
			p1_card=p1_card,
			p2_card=p2_card,
			flop_card=flop_card)
		return gamestate

	def run(self,T):
		util = 0
		start = timeit.default_timer()
		printProgressBar(0, T, prefix = ' Iter '+str(0)+"/"+str(T), suffix = 'Complete', length = 50)
		# conduct external-sampling Monte Carlo Counterfactual Regret
		for t in range(T):
			for player in self.PLAYERS:
				gamestate = self.initialize_gamestate()
				# util += self.traverse_ESMCCFR_P(gamestate, player, 1) if t > T//2 else self.traverse_ESMCCFR(gamestate, player)
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
				infosets.append((k,v.calculate_strategy(),v.count,v.regret_sum))
			for i in infosets:
				# print(i)
				csvwriter.writerow([i[0],i[1]])

		with open('strategy.pkl', 'wb') as pklfile:
			pickle.dump(self.infoset_strategy_map, pklfile, protocol=pickle.HIGHEST_PROTOCOL)

	def traverse_ESMCCFR(self, gamestate, player):

		if gamestate.is_terminal():
			# print('terminal', gamestate.get_utility(player))
			return gamestate.get_utility(player)

		#default to chance player
		other_player = 2 if player == 1 else 1
		player_turn = gamestate.get_players_turn()
		# print(player, player_turn, gamestate)
		# print('we care about player', player, 'and it is', player_turn, 's turn')
		possible_actions = gamestate.get_possible_actions(player_turn)
		strategy = Strategy(len(possible_actions))

		if player_turn == player:
			infoset = gamestate.get_infoset(player)

			# Determine the strategy at this infoset
			if infoset in self.infoset_strategy_map.keys():
				strategy = self.infoset_strategy_map[infoset]
			else:
				# print('found new infoset:', infoset)
				self.infoset_strategy_map[infoset] = strategy
			player_strategy = strategy.calculate_strategy()
			# initialize expected value
			# value of a node h is the value player i expects to achieve if all players play according to given strategy, having reached h
			value = 0
			value_action = [0 for i in range(len(player_strategy))]
			for action_index in range(len(possible_actions)):
				action = possible_actions[action_index]
				# need to define adding an action to a history, make Action class
				# make sure to copy history and not change it if making multiple calls!
				g = gamestate.deepcopy()
				# print('updating', player, action)
				g.update(player, action)

				# Traverse each action (per iteration of loop) (each action changes the history)
				va = self.traverse_ESMCCFR(g, player)
				# print(Card.int_to_str(gamestate.p1_card))
				# print('action:', action, 'value:', va)

				value_action[action_index] = va

				# Update the expected value
				value += player_strategy[action_index] * value_action[action_index]
			# print('value', value)
			# print('value_action', value_action)
			for action_index in range(len(possible_actions)):
				# Update the cumulative regret of each action
				strategy.regret_sum[action_index] += value_action[action_index] - value

			return value

		elif player_turn == other_player:
			infoset = gamestate.get_infoset(other_player)

			# Determine the strategy at this infoset
			if infoset in self.infoset_strategy_map.keys():
				strategy = self.infoset_strategy_map[infoset]
			else:
				# print('found new infoset:', infoset)
				self.infoset_strategy_map[infoset] = strategy

			player_strategy = strategy.calculate_strategy()
			# Sample one action and increment action counter
			action_index = self.get_random_action(player_strategy)
			action = possible_actions[action_index]
			# print('action:', action)
			strategy.count[action_index] += 1

			# Copy history, traverse one action
			g = gamestate.deepcopy()
			# print('other player picked action:', possible_actions[action_index])
			g.update(other_player, action)
			return self.traverse_ESMCCFR(g, player)
		else:
			raise Exception('How did we get here? There are no other players')

	def traverse_ESMCCFR_P(self, gamestate, player, p, C = -1000, K = 2):
		# C is a negative constant, paper does not provide any more information
		# K is a positive constant, paper does not provide any more information
		other_player = 2 if player == 1 else 1
		player_turn = gamestate.get_players_turn()
		possible_actions = gamestate.get_possible_actions(player_turn)
		strategy = Strategy(len(possible_actions))

		if gamestate.is_terminal():
			return gamestate.get_utility(player)

		elif player_turn == player:
			infoset = gamestate.get_infoset(player)

			# Determine the strategy at this infoset
			if infoset in self.infoset_strategy_map.keys():
				strategy = self.infoset_strategy_map[infoset]
			else:
				# print('found new infoset', other_player)
				self.infoset_strategy_map[infoset] = strategy

			player_strategy = strategy.calculate_strategy()

			# initialize expected value
			# value of a node h is the value player i expects to achieve if all players play according to given strategy, having reached h
			value = 0
			value_action = [0 for i in range(len(player_strategy))]
			explored = [False for i in range(len(player_strategy))]
			for action_index in range(len(possible_actions)):
				action = possible_actions[action_index]
				threshold = 1
				if strategy.regret_sum[action_index] < C:
					threshold = max(0.02/p, K/(K+C-strategy.regret_sum[action_index]))

				if random.random() < threshold:
					g = gamestate.deepcopy()
					g.update(player, action)

					# Traverse each action (per iteration of loop) (each action changes the history)
					value_action[action_index] = self.traverse_ESMCCFR_P(g, player, p * min(threshold,1))
					explored[action_index] = True

					# Update the expected value
					value += player_strategy[action_index] * value_action[action_index]
				else:
					explored[action_index] = False

			for action_index in range(len(possible_actions)):
				if explored[action_index]:
					strategy.regret_sum[action_index] += value_action[action_index] - value

			return value

		elif player_turn == other_player:
			infoset = gamestate.get_infoset(other_player)

						# Determine the strategy at this infoset
			if infoset in self.infoset_strategy_map.keys():
				strategy = self.infoset_strategy_map[infoset]
			else: 
				# print('found new infoset:', infoset)
				self.infoset_strategy_map[infoset] = strategy

			player_strategy = strategy.calculate_strategy()

			# Sample one action and increment action counter
			action_index = self.get_random_action(player_strategy)
			strategy.count[action_index] += 1/p

			# Copy history, traverse one action
			g = gamestate.deepcopy()
			g.update(other_player, possible_actions[action_index])
			return self.traverse_ESMCCFR(g, player)
		else:
			raise Exception('How did we get here?', 'Player:', player)

if __name__ == "__main__":
	# cProfile.runctx("ESMCCFR_P(100000)",globals(),locals())
	ESMCCFR_P = ESMCCFR_P()
	ESMCCFR_P.run(10000)