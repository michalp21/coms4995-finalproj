from Card import Card
from Action import Action
from GameState import GameState
from InfoSet import InfoSet
from Strategy import Strategy
from collections import defaultdict
from numpy.random import choice

players = range(2)
infoset_strategy_map = defaultdict(Strategy)

def get_random_action(strategy):
	# return the index of the action the strategy chooses to take
	return choice(range(len(strategy.actions)), 1, p=strategy.strategy)[0]

def ESMCCFR_P(T):
	# conduct external-sampling Monte Carlo Counterfactual Regret
	infoset_map = {}
	for t in range(T):
		for p in players:
			# what is "None"/empty set? presumably empty gamestate
			g = GameState()
			traverse_ESMCCFR_P(None, p, 1) if t > T/2 else traverse_ESMCCFR(None, p)

def traverse_ESMCCFR(gamestate, player):
	infoset = gamestate.get_infoset(player)
	if gamestate.is_terminal():
		return gamestate.get_utility(player)
	elif gamestate.get_players_turn() == player:
		# Determine the strategy at this infoset
		strategy = infoset_strategy_map[infoset]
		value = 0
		for action in gamestate.get_actions()
			# need to define adding an action to a history, make Action class
			# make sure to copy history and not change it if making multiple calls!
			g = gamestate.deepcopy()
			g.update(player, action)
			# Traverse each action (each action changes the history)
			value_action = traverse_ESMCCFR(g, player)
			# Update the expected value
			value += strategy[action] * value_action
			# Update the regret of each action
			strategy.regret_sum[action] += value_action - value
		return value
	elif gamestate.get_players_turn() == 0 if player == 1 else 1:
		strategy = infoset_strategy_map[infoset]
		action_index = get_random_action(strategy)
		action = strategy.actions[action_index]
		strategy.count[action_index] += 1
		g = gamestate.deepcopy()
		g.update(player, action)
		return traverse_ESMCCFR(g, 0 if player == 1 else 1)
	else:
		# chance randomly selects a new card(s), note that chance updates differently
		action = get_random_action(chance)
		g = gamestate.deepcopy()
		g.update(chance, action)
		# if I am first player I go first after chance?
		return traverse_ESMCCFR(h, player)

def test_equality():
	c1 = Card(10, 'spades')
	c2 = Card(11, 'clubs')
	infoset1 = InfoSet()
	infoset1.hole_cards = [c1, c2]

	d1 = Card(10, 'spades')
	d2 = Card(11, 'clubs')
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