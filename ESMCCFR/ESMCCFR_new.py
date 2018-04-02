from Card import Card
from Action import Action
from GameState import GameState
from InfoSet import InfoSet
from Strategy import Strategy

players = range(2)

def ESMCCFR_P(T):
	# conduct external-sampling Monte Carlo Counterfactual Regret
	infoset_map = {}
	for t in range(T):
		for p in players:
			# what is "None"/empty set? presumably empty gamestate
			g = GameState()
			traverse_ESMCCFR_P(None, p, 1) if t > T/2 else traverse_ESMCCFR(None, p)

def traverse_ESMCCFR(gamestate, player):
	if gamestate.is_terminal():
		return gamestate.get_utility(player)



		
	elif h.get_players_turn() == p:
		info_set = h.get_info_set_key(p)
		# next line sounds like it's just computing the strategy, logic in InfoSet
		# Determine the strategy at this infoset
		strategy = info_set.get_strategy()
		value = 0
		for a in h.get_actions()
			# need to define adding an action to a history, make Action class
			# make sure to copy history and not change it if making multiple calls!
			history = h
			history.add(a)
			# Traverse each action (each action changes the history)
			value_a = traverse_ESMCCFR(history, p)
			# Update the expected value
			value += strategy[a] * value_a
			# Update the regret of each action
			info_set.regret_sum[a] += value_a - value
		return value
	elif h.get_players_turn() == 0 if p == 1 else 1:
		info_set = h.get_info_set_key(p)
		strategy = info_set.get_strategy()
		action = get_random_action(strategy)
		info_set.strategy[action] += 1
		history = h
		history.add(action)
		return traverse_ESMCCFR(history, 0 if p == 1 else 1)
	else:
		action = get_random_action(chance)
		h.add(action)
		# if I am first player I go first after chance?
		return traverse_ESMCCFR(h, p)









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