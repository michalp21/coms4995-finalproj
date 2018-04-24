from deuces2.card import Card
from deuces2.evaluator import Evaluator

hunl_evaluator = Evaluator()

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

def leduc_evaluate(p1_hole, p2_hole, board):
	# return positive if p1 wins
	return _leduc_rank(p2_hole[0], board[0][0]) - _leduc_rank(p1_hole[0], board[0][0])

def kuhn_evaluate(p1_hole, p2_hole, board):
	# no board, one card hole, bigger card wins
	return p1_hole[0] - p2_hole[0]

def hunl_evaluate(p1_hole, p2_hole, board):
	board = board[0] + board[1] + board[2]
	return hunl_evaluator.evaluate(p2_hole, board) - hunl_evaluator.evaluate(p1_hole, board)
