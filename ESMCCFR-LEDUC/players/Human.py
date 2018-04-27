class Human:
	def __init__(self, rules, setup):
		self.rules = rules
		self.setup = setup

	def train(self, T=None):
		self._name = str(input("What's your name?\n"))
		return self

	def bet(self, state):
		pretty = state.get_possible_bets(pretty=True)
		bets = state.get_possible_bets(pretty=False)
		action = -1
		while (action not in bets):
			action = int(input("\tSelect action from %s:\n\t>" % str(pretty)))
		return action

	def __str__(self):
		return self._name

