# An Action consists of an action = fold, check, call, bet, raise and an amount
class Action:

	def __init__(self, action, amount):
		self.action = action
		self.amount = amount

	def __eq__(self, other):
		return self.action == other.action and self.amount == other.amount