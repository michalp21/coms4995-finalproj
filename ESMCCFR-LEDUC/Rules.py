import collections
from deuces2.card import Card
from deuces2.deck import Deck
from deuces2.evaluator import Evaluator
from Deal import Deal

Rules = collections.namedtuple('Rules', 'evaluate deal rounds switch')

def _leduc_rank(card, flop_card):
	# assumes A is 1, K is 2, Q is 3 
	product = card*flop_card
	return product if flop_card == card else product + 10

def _leduc_evaluate(deal):
	# return positive if big wins
	return _leduc_rank(deal.small[0], deal.board[0][0]) - _leduc_rank(deal.big[0], deal.board[0][0])

def _kuhn_evaluate(deal):
	# no board, one card hole, bigger card wins
	return deal.big[0] - deal.small[0]

_hunl_evaluator = Evaluator()

def _hunl_evaluate(deal):
	board = deal.board[0] + deal.board[1] + deal.board[2]
	return _hunl_evaluator.evaluate(deal.small, board) - _hunl_evaluator.evaluate(deal.big, board)

def _hunl_deal():
	deck = Deck(52)
	return Deal(big=deck.draw(2),
		small=deck.draw(2),
		board=[deck.draw(3), [deck.draw(1)], [deck.draw(1)]])

def _leduc_deal():
	deck = Deck(6)
	return Deal(big=[deck.draw(1)],
		small=[deck.draw(1)],
		board=[[deck.draw(1)]])

def _kuhn_deal():
	deck = Deck(3)
	return Deal(big=[deck.draw(1)],
		small=[deck.draw(1)],
		board=[[]])

Rules.leduc = Rules(evaluate=_leduc_evaluate,
	deal=_leduc_deal,
	rounds=2,
	switch=False)

Rules.kuhn = Rules(evaluate=_kuhn_evaluate,
	deal=_kuhn_deal,
	rounds=1,
	switch=False)

Rules.hunl = Rules(evaluate=_hunl_evaluate,
	deal=_hunl_deal,
	rounds=4,
	switch=True)

