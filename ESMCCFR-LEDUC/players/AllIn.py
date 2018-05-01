class AllIn:

	def __init__(self, rules, setup):
		pass

	def new_game(self):
		pass

	def take_seat(self, is_small_blind):
		self.is_small_blind = is_small_blind

	def receive_cards(self, cards):
		pass

	def train(self, T=None):
		pass

	def opponent_bets(self, bet):
		pass

	def bet(self, actions):
		print(actions)
		if 'allIn' in actions:
			return actions['allIn'][0]
		if 'check' in actions:
			return actions['check'][0]
		if 'fold' in actions:
			return actions['fold'][0]

	def __str__(self):
		return "AllInBot"