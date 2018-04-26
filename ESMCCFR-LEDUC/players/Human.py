class Human:
	def __init__(self, rules, setup):
		self.rules = rules
		self.setup = setup

	def train(self, T=None):
		self._name = str(input("What's your name?\n"))

	def bet(self, state):
		bets = state.get_possible_bets()
		action = -1
		while (action not in bets):
			action = int(input("\tSelect action from %s:\n\t>" % str(bets)))
		return action

	def __str__(self):
		return self._name

