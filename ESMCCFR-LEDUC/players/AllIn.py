class AllIn:

	def __init__(self, rules, setup):
		pass

	def train(self, T=None):
		pass

	def bet(self, state):
		return state.get_possible_bets()[-1]

	def __str__(self):
		return "AllInBot"