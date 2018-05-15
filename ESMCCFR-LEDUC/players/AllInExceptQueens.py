class AllInExceptQueens:

	def __init__(self, rules, setup):
		self.rules = rules

	def new_game(self):
		pass

	def take_seat(self, is_small_blind):
		self.is_small_blind = is_small_blind

	def receive_cards(self, cards):
		self.has_queen = (cards[0] == 3)

	def advance_round(self, cards):
		pass

	def opponent_bets(self, bet):
		pass

	def bet(self, actions_by_type=None, actions_by_numbers=None):

		if not self.has_queen and 'allIn' in actions_by_type:
			return actions_by_type['allIn'][0]
		if not self.has_queen and 'call' in actions_by_type:
			return actions_by_type['call'][0]
		if 'check' in actions_by_type:
			return actions_by_type['check'][0]
		if 'fold' in actions_by_type:
			return actions_by_type['fold'][0]

		raise Exception("actions seem bad: %s", str(actions))

	def __str__(self):
		return "AllInExceptQueens"