class AllInOnAce:

	def __init__(self, rules, setup):
		self.rules = rules

	def new_game(self):
		pass

	def take_seat(self, is_small_blind):
		self.is_small_blind = is_small_blind

	def receive_cards(self, cards):
		self.has_ace = (cards[0] == 1)

	def advance_round(self, cards):
		pass

	def opponent_bets(self, bet):
		pass

	def bet(self, actions_by_type=None, actions_by_numbers=None):
		if self.has_ace:
			return actions_by_numbers[-1]
		return 0

	def __str__(self):
		return "AllInOnAce"