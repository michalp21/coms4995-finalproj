from Card import Card
from ActionAndAmount import ActionAndAmount
from GameState import GameState
from GameStateK import GameStateK
from InfoSet import InfoSet
from ExtraInfo import ExtraInfo
from Enums import *
from collections import defaultdict
from numpy.random import choice
from copy import deepcopy

players = [1,2]
infoset_extrainfo_map = defaultdict(lambda: ExtraInfo(len(Action)))

def get_random_action(strategy):
	# return the index of the action the strategy chooses to take
	return choice(range(len(strategy)), 1, p=strategy)[0]

def ESMCCFR_P(T):
	# conduct external-sampling Monte Carlo Counterfactual Regret
	for t in range(T):
		for p in players:
			# what is "None"/empty set? presumably empty gamestate
			# g = GameState()
			g = GameState()
			#traverse_ESMCCFR_P(g, p, 1) if t > T/2 else traverse_ESMCCFR(g, p)
			traverse_ESMCCFR(g, p)

def traverse_ESMCCFR(gamestate, player):
	#default to chance player
	other_player = 0
	if player == 1:
		other_player = 2
	elif player == 2:
		other_player = 1

	if gamestate.is_terminal():
		return gamestate.get_utility(player)

	elif gamestate.get_players_turn() == player:
		infoset = gamestate.get_infoset(player)

		# Determine the strategy at this infoset
		extrainfo = infoset_extrainfo_map[infoset]
		strategy = extrainfo.calculate_strategy(gamestate.possible_actions)

		# initialize expected value
		# value of a node h is the value player i expects to achieve if all players play according to given strategy, having reached h
		value = 0
		for action in gamestate.possible_actions:

			# need to define adding an action to a history, make Action class
			# make sure to copy history and not change it if making multiple calls!
			g = deepcopy(gamestate)
			g.update(player, action)

			# Traverse each action (per iteration of loop) (each action changes the history)
			value_action = traverse_ESMCCFR(g, player)

			# Update the expected value
			value += strategy[action] * value_action

			# Update the cumulative regret of each action
			extrainfo.regretSum[action] += value_action - value

		return value

	elif gamestate.get_players_turn() == other_player:
		infoset = gamestate.get_infoset(other_player)

		# Determine the strategy at this infoset
		extrainfo = infoset_extrainfo_map[infoset]
		strategy = extrainfo.calculate_strategy(gamestate.possible_actions)

		# Sample one action and increment action counter
		action_index = get_random_action(strategy)
		action = extrainfo.actions[action_index]
		extrainfo.count[action_index] += 1

		# Copy history, traverse one action
		g = deepcopy(gamestate)
		g.update(player, action)
		return traverse_ESMCCFR(g, player)

	else:
		chance = 0

		# chance randomly selects a new card(s), note that chance updates differently
		# update needs to remove card from gamestate
		action = Action.NEWCARD
		g = deepcopy(gamestate)
		g.update(chance, action)
		
		# if I am first player I go first after chance?
		return traverse_ESMCCFR(g, player)

def test_equality():
	c1 = Card(10, Suit.SPADES)
	c2 = Card(11, Suit.CLUBS)
	infoset1 = InfoSet()
	infoset1.hole_cards = [c1, c2]

	d1 = Card(10, Suit.SPADES)
	d2 = Card(11, Suit.CLUBS)
	infoset2 = InfoSet()
	infoset2.hole_cards = [d1, d2]

	print(infoset1 == infoset2)

def test_retrieval():
	infoset1 = InfoSet()
	infoset2 = InfoSet()

	s = {}
	s[infoset1] = 1
	s[infoset2] = 2

	print(s[infoset1])

if __name__ == "__main__":
	ESMCCFR_P(10)









