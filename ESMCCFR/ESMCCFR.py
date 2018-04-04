from Card import Card
# from ActionAndAmount import ActionAndAmount
# from GameState import GameState
from GameStateK import *
from InfoSet import InfoSet
from ExtraInfo import ExtraInfo
from Enums import *
from collections import defaultdict
import random
import cProfile
import timeit

players = [1,2]
infoset_extrainfo_map = defaultdict(lambda: ExtraInfo(len(Action)-1))

def get_random_action(strategy):
	# return the index of the action the strategy chooses to take
	# return choice(range(len(strategy)), 1, p=strategy)[0]
	return random.choices([i for i in range(len(strategy))], weights=strategy, k=1)[0]

def ESMCCFR_P(T):
	util = 0

	start = timeit.default_timer()
	# conduct external-sampling Monte Carlo Counterfactual Regret
	for t in range(T):
		for p in players:
			# g = GameState()
			g = GameStateK()
			# util += traverse_ESMCCFR_P(g, p, 1) if t > T//2 else traverse_ESMCCFR(g, p)
			util += traverse_ESMCCFR(g, p)
	stop = timeit.default_timer()

	print("Time elapsed: " + str(stop-start))
	print("Average game value: " + str(util / T))

	#Print Infosets
	infosets = []
	for k,v in infoset_extrainfo_map.items():
		infosets.append((k,v.get_average_strategy(),v.count,v.regretSum))
	for i in sorted(infosets, key=lambda i:i[0]):
		print(i[0],i[1],i[3])

def traverse_ESMCCFR(gamestate, player):
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
		extrainfo = infoset_extrainfo_map[infoset]
		strategy = extrainfo.calculate_strategy(possible_actions)

		# initialize expected value
		# value of a node h is the value player i expects to achieve if all players play according to given strategy, having reached h
		value = 0
		value_action = [0]*len(strategy)
		for action in possible_actions:

			# need to define adding an action to a history, make Action class
			# make sure to copy history and not change it if making multiple calls!
			g = gamestate.deepcopy()
			g.update(player, action)

			# Traverse each action (per iteration of loop) (each action changes the history)
			value_action[action] = traverse_ESMCCFR(g, player)

			# Update the expected value
			value += strategy[action] * value_action[action]

		for action in possible_actions:
			# Update the cumulative regret of each action
			extrainfo.regretSum[action] += value_action[action] - value

		return value

	elif player_turn == other_player:
		infoset = gamestate.get_infoset(other_player)

		# Determine the strategy at this infoset
		extrainfo = infoset_extrainfo_map[infoset]
		strategy = extrainfo.calculate_strategy(possible_actions)

		# Sample one action and increment action counter
		action = get_random_action(strategy)
		extrainfo.count[action] += 1

		# Copy history, traverse one action
		g = gamestate.deepcopy()
		g.update(other_player, action)
		return traverse_ESMCCFR(g, player)

	else:
		chance = 0

		# chance randomly selects a new card(s), note that chance updates differently
		# update needs to remove card from gamestate in HUNL
		action = Action.NEWCARD
		g = gamestate.deepcopy()
		g.update(chance, action)
		
		return traverse_ESMCCFR(g, player)

def traverse_ESMCCFR_P(gamestate, player, p, C = -1000, K = 2):
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
		extrainfo = infoset_extrainfo_map[infoset]
		strategy = extrainfo.calculate_strategy(possible_actions)

		# initialize expected value
		# value of a node h is the value player i expects to achieve if all players play according to given strategy, having reached h
		value = 0
		value_action = [0]*len(strategy)
		explored = [False]*len(strategy)
		for action in possible_actions:

			threshold = 1
			if extrainfo.regretSum[action] < C:
				threshold = max(0.02/p, K/(K+C-action_regret))

			if random.random() < threshold:
				g = gamestate.deepcopy()
				g.update(player, action)

				# Traverse each action (per iteration of loop) (each action changes the history)
				value_action[action] = traverse_ESMCCFR_P(g, player, p * min(threshold,1))
				explored[action] = True

				# Update the expected value
				value += strategy[action] * value_action[action]
			else:
				explored[action] = False

		for action in possible_actions:
			if explored[action]:
				extrainfo.regretSum[action] += value_action[action] - value

		return value

	elif player_turn == other_player:
		infoset = gamestate.get_infoset(other_player)

		# Determine the strategy at this infoset
		extrainfo = infoset_extrainfo_map[infoset]
		strategy = extrainfo.calculate_strategy(possible_actions)

		# Sample one action and increment action counter
		action = get_random_action(strategy)
		extrainfo.count[action] += 1/p

		# Copy history, traverse one action
		g = gamestate.deepcopy()
		g.update(other_player, action)
		return traverse_ESMCCFR(g, player)
	else:
		chance = 0

		# chance randomly selects a new card(s), note that chance updates differently
		# update needs to remove card from gamestate in HUNL
		action = Action.NEWCARD
		g = gamestate.deepcopy()
		g.update(chance, action)
		
		return traverse_ESMCCFR(g, player)

if __name__ == "__main__":
	# cProfile.runctx("ESMCCFR_P(100000)",globals(),locals())
	ESMCCFR_P(200000)









