class Human:
	def __init__(self, rules, setup):
		self.rules = rules
		self.setup = setup
		self._name = str(input("What's your name?\n"))

	def new_game(self):
		pass

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

	def bet(self, actions_by_type, actions_by_number=None):
		action = -1
		while (action not in actions_by_number):
			action = int(input("\tSelect action from %s:\n\t>" % str(actions_by_type)))
		return action

	def __str__(self):
		return self._name

