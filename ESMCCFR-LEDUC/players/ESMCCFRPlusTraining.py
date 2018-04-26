from ESMCCFR import ESMCCFR_P
import random
from Strategy import Strategy

class ESMCCFRPlusTraining:

	def __init__(self, rules, setup):
		self.rules = rules
		self.setup = setup

	def train(self, T=1000):
		esmccfr = ESMCCFR_P(self.rules, self.setup)
		self.strategy_map = esmccfr.run(T)
		return self

	def bet(self, state):
		bets = state.get_possible_bets()
		infoset = state.get_infoset()
		if infoset in self.strategy_map.keys():
			strategy = self.strategy_map[infoset]
		else:
			strategy = Strategy(len(bets))
		player_strategy = strategy.calculate_strategy()

		return bets[random.choices(list(range(len(player_strategy))),
			weights=player_strategy, k=1)[0]]

	def name(self):
		return "EsmccfrBot"