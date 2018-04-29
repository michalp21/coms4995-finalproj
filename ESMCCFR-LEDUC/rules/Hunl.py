from deuces2.evaluator import Evaluator
from deuces2.deck import Deck
from deuces2.card import Card
from Deal import Deal

class Hunl:
	_evaluator = Evaluator()
	def __init__(self):
		self.switch = True
		self.rounds = 4
		pass

	def evaluate(self, deal):
		return (_evaluator.evaluate(deal.small, deal.join_board()) -
		_evaluator.evaluate(deal.big, deal.join_board()))

	def deal(self):
		deck = Deck(52)
		return Deal(rules=self, big=deck.draw(2),
			small=deck.draw(2),
			board=[deck.draw(s) for s in (3, 1, 1)])

	def pretty(self, card):
		return Card.int_to_pretty_str(card)
