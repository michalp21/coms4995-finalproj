##### A Strategy tracks counts and regrets to determine a distribution over actions

# ExtraInfo stores certain information corresponding to each InfoSet.
class ExtraInfo:

	#if actions are enum then regret and count turn to dict?
	def __init__(self, actions):
		# actions should be defined by GameEngine based on GameState
		self.actions = actions
		# cumulative regret until this infoset
		self.regretSum = [0 for i in range(self.actions)]
		# how many times action is sampled during opponent traversal
		self.count = [0 for i in range(self.actions)]

	def calculate_regret(self):
		# sum of regrets over current available actions
		maxRegretSum = 0
		
		strategy = [0 for i in range(self.actions)]
		for a in self.actions:
			maxRegretSum += max(0,self.regret[a])
		for a in self.actions:
			strategy[a] = max(0,self.regret[a])/maxRegretSum if (maxRegretSum > 0) else 1/len(actions)
		return strategy