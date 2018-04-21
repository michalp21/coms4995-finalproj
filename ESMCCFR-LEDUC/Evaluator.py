from deuces2.card import Card

class Evaluator:

	def __init__(self):
		pass

	def evaluate(self, card, board):
		card_rank = Card.int_to_str(card)[0]
		board_rank = Card.int_to_str(board)[0]
		if card_rank == board_rank:
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
