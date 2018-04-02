# A Card consists of a rank (2-9, T, J, Q, K, A) and a suit (c, d, h, s)
class Card:

	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit

	def __eq__(self, other):
		return self.rank == other.rank and self.suit == other.suit