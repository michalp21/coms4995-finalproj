def traverse_ESMCCFR_P(gamestate, player, probability, C = -100, K = 2):
	# C is a negative constant, paper does not provide any more information
	# K is a positive constant, paper does not provide any more information
	if gamestate.is_terminal():
		return gamestate.get_utility(player)
	elif gamestate.get_players_turn() == player:
		strategy = infoset_strategy_map[infoset]
		value = 0
		for action in gamestate.get_actions():
			threshold = 1
			# if action_index fails, something is wrong
			# the gamestate should generate the same actions for the same infoset
			action_index = strategy.action.index(action)
			action_regret = strategy.regret[action_index]
			if action_regret < C:
				threshold = max(0.02/probability, K/(K+C-action_regret))
			if uniform() < threshold:
				g = gamestate.deepcopy()
				g.update(player, action)
				value_action = traverse_ESMCCFR_P(g, player, probability * min(threshold, 1))
				# believe we need to store the value_action associated with the action
				# the pseudo-code doesn't persist value_action outside of this for loop
				# otherwise not possible to access in the next for loop over actions
				action.set_value(value_action)
				value += strategy.probability[action_index] * value_action
				action.set_explored(True)
			else:
				action.set_explored(False)
		# value has been computed over all actions now
		for action in gamestate.get_actions():
			action_index = strategy.action.index(action)
			if action.get_explored():
				strategy.regret[action_index] += action.get_value() - value
		return value
	elif gamestate.get_players_turn() == 0 if player == 1 else 0:
		infoset = gamestate.get_infoset(0 if player == 1 else 1)
		strategy = infoset_strategy_map[infoset]
		action_index = get_random_action(strategy)
		action = strategy.actions[action_index]
		strategy.count[action_index] += 1/p
		g = gamestate.deepcopy()
		g.update(player, action)
		return traverse_ESMCCFR_P(g, 0 if player == 1 else 1, probability)
	else:
		# chance randomly selects a new card(s), note that chance updates differently
		action = get_random_action(chance)
		g = gamestate.deepcopy()
		g.update(chance, action)
		return traverse_ESMCCFR(g, player)
