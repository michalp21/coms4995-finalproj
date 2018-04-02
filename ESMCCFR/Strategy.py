# A Strategy tracks counts and regrets to determine a distribution over actions
class Strategy:

	def __init__(self, actions):
		# actions should be defined by GameEngine based on GameState
		self.actions = actions
		self.regret = [0 for i in range(self.actions)]
		self.count = [0 for i in range(self.actions)]
