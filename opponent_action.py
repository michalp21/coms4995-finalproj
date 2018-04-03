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

# infoset: a set of public state and private state
# subgame: a collection of top-level histories
def opponent_action(subgame, action, gifts, oppo_reach_prob_fn):
	if gifts is None:
		gifts = {}
	oppo_reach_prob_values = {}
	v_bp = {}
	for history in subgame:
		oppo_reach_prob_values[history] = oppo_reach_prob_fn[history]
	for oppo_infoset in set([h.get_opponent_infoset() for h in subgame]):
		cards = oppo_infoset.private_state()
		v_bp[oppo_infoset] = 0 # initial value
		v_alt

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