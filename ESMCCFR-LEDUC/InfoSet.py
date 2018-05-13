# An InfoSet contains information about the State available to a player
# it implements __eq__ and __hash__ so it can be used as a key to look up strategies
# this class should be immutable as it is the key to look up strategies in a map

from deuces2.card import Card

class InfoSet:

	def __init__(self, hole, board, bets):
		self.cards = hole[0]
		if len(board) >= 1:
			self.cards += 3 * board[0][0]
		self.bets_0 = tuple(bets[0])
		self.bets_1 = tuple(bets[1])
	def __eq__(self, other):
		return self.cards == other.cards and self.bets_0 == other.bets_0 and self.bets_1 == other.bets_1
		return self.data == other.data

	def __hash__(self):
		return hash((self.cards, self.bets_0, self.bets_1))