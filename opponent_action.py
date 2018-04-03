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
	 v_bp,
	 oppo_reach_probabilities):
	gifts = gifts if gifts is not None else defaultdict(int)

	oppo_infosets = set([h.get_opponent_infoset() for h in subgame])

	v_alt = [(gifts[oi] + v_bp[oi]) for oi in oppo_infosets]

	augmented = construct_subgame(subgame, action)
	solve_augmented(augmented, v_alt, oppo_reach_prob_values)

	for each oi in oppo_infosets:
		gifts[oi] += v_bp[oi] - v_bp(oi.move(a))

# Literally, the pseudocode
'''
def function opponent_action(S, a, g):
	for each node h in S_top:
		pi_oppo[history] = pi_oppo(history) # copy
	for each oppo_infoset in S_top:
		c = oppo_infoset.oppo_cards()
		v_bp[oppo_infoset] = v_bp(oppo_infoset) # copy
		v_alt[oppo_infoset] = g[c] + v_bp[oppo_infoset]
	S_aug = construct_subgame(S, a)
	solve_augmented(S_aug, v_alt, pi_oppo)
	for each oppo_infoset in S_top:
		c = oppo_infoset.oppo_cards()
		g_new[c] = g[c] + v_bp[oppo_infoset] - v_bp[oppo_infoset, a]
	return g_new
'''

# run kuhn poker

opponent_action([])