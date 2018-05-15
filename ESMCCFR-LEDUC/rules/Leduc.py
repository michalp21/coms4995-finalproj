import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from deuces2.deck import Deck
from Deal import Deal


class Leduc:

	_pretty_cards = {1: 'A', 2: 'K', 3: 'Q'}

	def __init__(self):
		self.switch = False
		self.rounds = 2

	def _rank(self, card, flop):
		# A is 1, K is 2, Q is 3

		# Add the number of possible cards to card value
		# if there is a pair
		return card+3 if flop == card else card

	def evaluate(self, deal):
		flop = deal.board[0][0]
		small = self._rank(deal.small[0], flop)
		big = self._rank(deal.big[0], flop)
		return small - big

	def pretty(self, card):
		return Leduc._pretty_cards[card]

	def deal(self):
		deck = Deck(6)
		return Deal(rules=self, big=(deck.draw(1),),
			small=(deck.draw(1),),
			board=( (deck.draw(1),) ,) )

def unit_test():
	l = Leduc()

	flop = 1
	small = l._rank(2, flop)
	big = l._rank(3, flop)
	assert small - big < 0

	flop = 1
	small = l._rank(3, flop)
	big = l._rank(2, flop)
	assert small - big > 0

	flop = 1
	small = l._rank(3, flop)
	big = l._rank(3, flop)
	assert small - big == 0

	flop = 3
	small = l._rank(3, flop)
	big = l._rank(2, flop)
	assert small-big > 0

if __name__ == '__main__':
    unit_test()