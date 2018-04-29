from deuces2.card import Card

class Deal():

	def __init__(self, rules, big, small, board):
		self.rules = rules
		self.big = big
		self.small = small
		self.board = board

	def player(self, p):
		return self.big if p == 1 else self.small

	def __repr__(self):
		return '1: %s, 2: %s, Board: %s' % (
			str([self.rules.pretty(c) for c in self.big]),
			str([self.rules.pretty(c) for c in self.small]),
			str([[self.rules.pretty(c) for c in round_cards]
				for round_cards in self.board]))

	def join_board(self):
		return [card for round_cards in self.board for card in round_cards]
