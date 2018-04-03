# Kuhn poker has these info sets:
# 1: _
# 2: 1:b
# 2: 1:p
# 1: 1:p,2:b

# times cards private cards

# assume history has methods
# .get_active_player
# .get_available_actions
# .get_active_player_infoset
# .get_opponent_infoset

# infosets need to implement equals

# oppo_reach_probabilities must be defined over top level histories in h
# infoset: a set of public state and private state
# subgame: a collection of top-level histories
def opponent_action(
	subgame,
	action,
	gifts,
	blueprint_values,
	oppo_reach_probabilities):
	gifts = gifts if gifts is not None else defaultdict(int)

	oppo_infosets = set([h.get_opponent_infoset() for h in subgame])

	alternative_values = [(gifts[oi] + blueprint_values[oi])
		for oi in oppo_infosets]

	augmented = construct_subgame(subgame, action)
	solve_augmented(augmented, alternative_values,
		oppo_reach_probailities)

	for each oi in oppo_infosets:
		gifts[oi] += v_bp[oi] - v_bp(oi.move(a))


# run kuhn poker

opponent_action([])