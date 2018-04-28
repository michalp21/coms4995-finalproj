class AllInExceptQueens:

	def __init__(self, rules, setup):
		self.rules = rules

	def take_seat(self, is_small_blind):
		self.is_small_blind = is_small_blind

	def receive_cards(self, cards):
		self.has_queen = (cards[0] == 3)

	def train(self, T=None):
		pass

	def advance_round(self, cards):
		pass

	def opponent_bets(self, bet):
		pass

	def bet(self, actions):

		if not self.has_queen and 'allIn' in actions:
			return actions['allIn'][0]
		if not self.has_queen and 'call' in actions:
			return actions['call'][0]
		if 'check' in actions:
			return actions['check'][0]
		if 'fold' in actions:
			return actions['fold'][0]

		raise Error("actions seem bad: %s", str(actions))

	def __str__(self):
		return "AllInExceptQueens"