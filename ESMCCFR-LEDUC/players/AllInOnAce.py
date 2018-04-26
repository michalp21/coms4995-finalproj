class AllInOnAce:

	def __init__(self, rules, setup):
		self.rules = rules

	def train(self, T=None):
		pass

	def bet(self, state):
		if state.get_infoset().hole[0] == 1
			return state.get_possible_bets()[-1]
		return 0

	def name(self):
		return "AllIBot"