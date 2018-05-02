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

	augmented = {
		get_active_player: 3 - subgame.aug_get_active_player(),
		get_available_actions: lambda: ['T', 'S'],
		get_active_player_infoset: lambda: subgame.get_opponent_infoset(),
		get_opponent_infoset: lambda: [], # not needed
		is_terminal: lambda: False
	}
	augmented.act = (lambda action: subgame if action == 'S'
		else terminal_with(alternative_values))

	chance = chance_deals()
	chance.act = lambda action: augmented

	new_strategy = cfr(chance, oppo_reach_probabilities)
	# merge new_strategy with v_bp

	for each oi in oppo_infosets:
		gifts[oi] += v_bp[oi] - v_bp(oi.move(a))


def chance_deals():
	is_chance: lambda: True
	get_active_player = lambda: None
	# Temporary way to deal cards. Should be aware of existing flop
	get_available_actions = lambda: ["cards: " + i + "," + j + ";" + k + "," + l
		 for i,j,k,l in itertools.product(52, 4)]
	get_active_player_infoset = lambda: None # not relevant
	get_opponent_infoset = lambda: None # not relevant
	is_terminal = lambda: False

	return {
		get_active_player: get_active_player,
		get_available_actions: get_available_actions,
		get_active_player_infoset: get_active_player_infoset,
		get_opponent_infoset: get_opponent_infoset,
		is_terminal: is_terminal,
		utility: utility
	}

def terminal_with(values):
	is_chance: False
	get_active_player = lambda: None
	get_available_actions = lambda: []
	get_active_player_infoset = lambda: None
	get_opponent_infoset = lambda: None
	is_terminal = lambda: True
	# todo
	utility = lambda private_state: values[private_state['p1cards']]

	return {
		get_active_player: get_active_player,
		get_available_actions: get_available_actions,
		get_active_player_infoset: get_active_player_infoset,
		get_opponent_infoset: get_opponent_infoset,
		is_terminal: is_terminal,
		utility: utility
	}
