class AllInExceptQueen:

	def __init__(self, rules, setup):
		self.rules = rules

	def train(self, T=None):
		pass

	def bet(self, state):
		bets = state.get_possible_bets()
		# if starting player, throw out queens
		# all in otherwise
		if state.get_players_turn() == 2 and len(bets) > 2:
			if state.get_infoset().hole[0] in (1, 2):
				return bets[-1]
			else:
				return 0
		else:
			return bets[-1]

	def name(self):
		return "AllInExceptQueen"