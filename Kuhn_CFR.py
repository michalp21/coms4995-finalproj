from numpy.random import choice
from random import shuffle
from collections import defaultdict

class Node:

	def __init__(self):
		self.num_actions = 2
		self.regret_sum = [0, 0]
		self.strategy = [0, 0]
		self.strategy_sum = [0, 0]

	def get_strategy(self, realization_weight):
		# strategy is derived from the regret_sum
		normalizing_sum = 0
		self.strategy = [r if r > 0 else 0 for r in self.regret_sum]
		normalizing_sum = sum(self.strategy)
		if normalizing_sum > 0:
			self.strategy = [s/normalizing_sum for s in self.strategy]
		else:
			self.strategy = [1.0/self.num_actions for i in range(self.num_actions)]
		self.strategy_sum = [self.strategy_sum[i] + realization_weight*self.strategy[i] for i in range(self.num_actions)]
		return self.strategy

	def get_average_strategy(self):
		average_strategy = []
		normalizing_sum = sum(self.strategy_sum)
		if normalizing_sum > 0:
			average_strategy = [self.strategy_sum[i]/normalizing_sum for i in range(self.num_actions)]
		else:
			average_strategy = [1.0/self.num_actions for i in range(self.num_actions)]
		return average_strategy

	def to_string(self):
		return self.info_set + ['{0:0.2f}'.format(i) for i in get_average_strategy()]

class KuhnTrainer:

	def __init__(self):
		self.num_actions = 2
		self.node_map = defaultdict(Node)
		self.terminal_states = ['pp','pbp','pbb','bp','bb']
		self.player0_wins_states = ['bp']
		self.player1_wins_states = ['pbp']
		self.showdown_potsize1_states = ['pp']
		self.showdown_potsize2_states = ['pbb', 'bb']

	def train(self, iterations):
		cards = [1, 2, 3]
		util = 0
		for i in range(iterations):
			shuffle(cards)
			util += self.cfr(cards, '', 1, 1)
		print('Average game value: ', util/iterations)

	def cfr(self, cards, history, p0, p1):
		plays = len(history)
		player = plays % 2
		opponent = 1 - player
		# return payoff for terminal state
		if plays > 1:
			terminal_pass = history[-1] == 'p'
			double_bet = history[-2:] == 'bb'
			is_player_card_higher = cards[player] > cards[opponent]
			if terminal_pass:
				if history == 'pp':
					return 1 if is_player_card_higher else -1
				else:
					return 1
			elif double_bet:
				return 2 if is_player_card_higher else -2
		# if self.is_terminal(history):
		# 	return self.payoff(cards, history)
		# else:
		# get information set node or create it if nonexistant
		info_set = str(cards[player]) + history
		node = self.node_map[info_set]
		# for each action, recursively call cfr with additional history and probability
		strategy = node.get_strategy(p0)
		util = [0, 0]
		node_util = 0
		for a in range(self.num_actions):
			next_history = history + ('p' if a == 0 else 'b')
			if player == 0:
				util[a] = -self.cfr(cards, next_history, p0*strategy[a], p1)
			elif player == 1:
				util[a] = -self.cfr(cards, next_history, p0, p1*strategy[a])
			else:
				raise Exception('Player neither 0 nor 1')
			node_util += strategy[a]*util[a]
		for a in range(self.num_actions):
			regret = util[a] - node_util
			if player == 0:
				node.regret_sum[a] += p1*regret
			elif player == 1:
				node.regret_sum[a] += p0*regret
			else:
				raise Exception('Player neither 0 nor 1')
		return node_util

	def is_terminal(self, history):
		return history in self.terminal_states

	# def payoff(self, cards, history):


		# from perspective fo player 0
		# if history in self.player0_wins_states:
		# 	return 1
		# elif history in self.player1_wins_states:
		# 	return -1
		# elif history in self.showdown_potsize1_states:
		# 	return 1 if cards[0] > cards[1] else -1
		# elif history in self.showdown_potsize2_states:
		# 	return 2 if cards[0] > cards[1] else -2
		# else:
		# 	raise Exception('cannot determine payoff of non-terminal state')

kt = KuhnTrainer()
kt.train(100000)
for k in sorted(kt.node_map.keys()):
	print(k, kt.node_map[k].get_average_strategy())