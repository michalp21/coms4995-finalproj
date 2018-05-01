# ExtraInfo stores certain information corresponding to each InfoSet.
class Strategy:

	#if actions are enum then regret and count turn to dict?
	def __init__(self, num_actions):
		self.num_actions = num_actions
		# cumulative regret until this infoset
		self.regret_sum = [0] * num_actions
		# how many times action is sampled during opponent traversal
		self.count = [0] * num_actions
		# average strategy (only set by csv)
		self.average_strategy = None

	def get_average_strategy(self):
		if self.average_strategy:
			return self.average_strategy
		else:
			average_strategy = []
			normalizing_sum = sum(self.count)
			if normalizing_sum > 0:
				average_strategy = [self.count[i]/normalizing_sum for i in range(self.num_actions)]
			else:
				average_strategy = [1.0/self.num_actions] * self.num_actions
			return average_strategy

	#input: a list of actions eg [1,3,4] corresponding to Action enum.
	def calculate_strategy(self):
		# sum of regrets over current available actions
		max_regret_sum = 0

		strategy = [0] * self.num_actions
		for a in range(self.num_actions):
			max_regret_sum += max(0,self.regret_sum[a])
		for a in range(self.num_actions):
			strategy[a] = (max(0,self.regret_sum[a])/max_regret_sum
				if (max_regret_sum > 0) else 1/self.num_actions)

		return strategy