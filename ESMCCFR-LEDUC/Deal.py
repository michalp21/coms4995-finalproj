from deuces2.card import Card

class Deal():

	def __init__(self, big, small, board):
		self.big = big
		self.small = small
		self.board = board

	def player(self, p):
		return self.big if p == 1 else self.small

	def __repr__(self):
		return '1: %s, 2: %s, Board: %s' % (
			str([Card.int_to_str(c) for c in self.big]),
			str([Card.int_to_str(c) for c in self.small]),
			str([[Card.int_to_str(c) for c in round_cards]
				for round_cards in self.board]))

	def join_board(self):
		return [card for round_cards in self.board for card in round_cards]
