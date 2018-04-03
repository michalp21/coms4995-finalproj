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

	## this is all the SECOND thing that happens after the
	## initial chance node deals out cards
	aug_get_active_player = 3 - subgame.get_active_player()
	aug_get_available_actions = lambda: ['T', 'S']
	aug_get_active_player_infoset = lambda: subgame.get_opponent
	aug_get_opponent_infoset = lambda: []
	act_T = lambda: terminal_with(value)
	act_S = lambda: subgame


	augmented = construct_subgame(subgame, action)
	solve_augmented(augmented, alternative_values,
		oppo_reach_probailities)

	for each oi in oppo_infosets:
		gifts[oi] += v_bp[oi] - v_bp(oi.move(a))


def terminal_with(value):
	get_active_player = lambda: None
	get_available_actions = lambda: []
	get_active_player_infoset = lambda: None
	get_opponent_infoset = lambda: None
	is_terminal = lambda: True
	utility = lambda: value

	return {
		get_active_player: get_active_player,
		get_available_actions: get_available_actions,
		get_active_player_infoset: get_active_player_infoset,
		get_opponent_infoset: get_opponent_infoset,
		is_terminal: is_terminal,
		utility: utility
	}
