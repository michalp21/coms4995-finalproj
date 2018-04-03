##### A Strategy tracks counts and regrets to determine a distribution over actions

# ExtraInfo stores certain information corresponding to each InfoSet.
class ExtraInfo:

	#if actions are enum then regret and count turn to dict?
	def __init__(self,num_actions):
		# actions should be defined by GameEngine based on GameState
		self.actions = [0 for i in range(num_actions)]
		# cumulative regret until this infoset
		self.regretSum = [0 for i in range(num_actions)]
		# how many times action is sampled during opponent traversal
		self.count = [0 for i in range(num_actions)]

	def get_average_strategy(self):
		average_strategy = []
		normalizing_sum = sum(self.count)
		if normalizing_sum > 0:
			average_strategy = [self.count[i]/normalizing_sum for i in range(len(self.actions))]
		else:
			average_strategy = [1.0/len(self.actions) for i in range(len(self.actions))]
		return average_strategy

	#input: a list of actions eg [1,3,4] corresponding to Action enum.
	def calculate_strategy(self, actions):
		for a in actions:
			self.actions[a] = 1

		# sum of regrets over current available actions
		maxRegretSum = 0
		
		strategy = [0 for i in self.actions]
		for a in actions:
			maxRegretSum += max(0,self.regretSum[a])
		for a in actions:
			strategy[a] = max(0,self.regretSum[a])/maxRegretSum if (maxRegretSum > 0) else 1/len(actions)

		self.strategy = strategy

		# Testing
		# if sum(strategy) != 0:
		# 	print(strategy)
		# 	print(sum(strategy))

		return strategy