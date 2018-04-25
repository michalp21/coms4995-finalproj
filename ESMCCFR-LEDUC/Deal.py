class Deal():

	def __init__(self, p1, p2, board):
		self.p1 = p1
		self.p2 = p2
		self.board = board

	def player(self, p):
		return self.p1 if p == 1 else self.p2

	def __repr__():
		return '1: %s, 2: %s, Board: %s' % (
			str([Card.int_to_str(c) for c in p1]),
			str([Card.int_to_str(c) for c in p2]),
			str([[Card.int_to_str(c) for c in round_cards]
				for round_cards in board]))

