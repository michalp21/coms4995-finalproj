import collections
from deuces2.card import Card
from deuces2.deck import Deck
from deuces2.evaluator import Evaluator
from Deal import Deal

GameDefinition = collections.namedtuple('GameDefinition', 'evaluate deal rounds switch')

def _leduc_rank(card, flop_card):
	card_rank = Card.int_to_str(card)[0]
	flop_rank = Card.int_to_str(flop_card)[0]
	if card_rank == flop_rank:
		if card_rank == 'A':
			return 1
		elif card_rank == 'K':
			return 2
		elif card_rank == 'Q':
			return 3
		else:
			raise Exception('How did we get here?')
	else:
		if card_rank == 'A':
			return 4
		elif card_rank == 'K':
			return 5
		elif card_rank == 'Q':
			return 6
		else:
			raise Exception('How did we get here?')

def _leduc_evaluate(deal):
	# return positive if p1 wins
	return _leduc_rank(deal.p1[0], deal.board[0][0]) - _leduc_rank(deal.p1[0], deal.board[0][0])

def _kuhn_evaluate(deal):
	# no board, one card hole, bigger card wins
	return deal.p1[0] - deal.p2[0]

def _hunl_evaluate(deal):
	board = deal.board[0] + deal.board[1] + deal.board[2]
	return hunl_evaluator.evaluate(deal.p2, board) - hunl_evaluator.evaluate(deal.p1, board)

def _hunl_deal():
	deck = Deck(52)
	return Deal(p1=deck.draw(2),
		p2=deck.draw(2),
		board=[deck.draw(3), [deck.draw(1)], [deck.draw(1)]])

def _leduc_deal():
	deck = Deck(6)
	return Deal(p1=[deck.draw(1)],
		p2=[deck.draw(1)],
		board=[[deck.draw(1)]])

def _kuhn_deal():
	deck = Deck(3)
	return Deal(p1=[deck.draw(1)],
		p2=[deck.draw(1)],
		board=[[]])

GameDefinition.leduc = GameDefinition(evaluate=_leduc_evaluate,
	deal=_leduc_deal,
	rounds=2,
	switch=False)

GameDefinition.kuhn = GameDefinition(evaluate=_kuhn_evaluate,
	deal=_kuhn_deal,
	rounds=1,
	switch=False)

GameDefinition.hunl = GameDefinition(evaluate=Evaluator().evaluate,
	deal=_hunl_deal,
	rounds=4,
	switch=True)

