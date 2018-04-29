from deuces2.deck import Deck
from Deal import Deal

class Kuhn():

	def __init__(self):
		self.switch = False
		self.rounds = 1

	def evaluate(self, deal):
		return deal.small[0] - deal.big[0]

	def pretty(self, card):
		return str(card)

	def deal(self):
		deck = Deck(3)
		return Deal(rules=self, big=[deck.draw(1)],
			small=[deck.draw(1)],
			board=[])