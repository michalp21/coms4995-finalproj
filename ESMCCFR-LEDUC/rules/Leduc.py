from deuces2.deck import Deck
from Deal import Deal

class Leduc:

	_pretty_cards = {1: 'A', 2: 'K', 3: 'Q'}

	def __init__(self):
		self.switch = False
		self.rounds = 2

	def _rank(self, card, flop):
		# A is 1, K is 2, Q is 3
		product = card * flop
		return product if flop == card else product + 10

	def evaluate(self, deal):
		flop = deal.board[0][0]
		small = self._rank(deal.small[0], flop)
		big = self._rank(deal.big[0], flop)
		return big - small

	def pretty(self, card):
		return Leduc._pretty_cards[card]

	def deal(self):
		deck = Deck(6)
		return Deal(rules=self, big=[deck.draw(1)],
			small=[deck.draw(1)],
			board=[[deck.draw(1)]])