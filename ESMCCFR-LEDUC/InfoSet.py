# An InfoSet contains information about the State available to a player
# it implements __eq__ and __hash__ so it can be used as a key to look up strategies
# this class should be immutable as it is the key to look up strategies in a map

from deuces2.card import Card

class InfoSet:

	def __init__(self, hole, board, bets):
		self.hole = hole
		if len(bets) == 1:
			hash(hole[0])
			hash(board)
			self.data = (hole[0], board, tuple(bets[0]))
		elif len(bets) == 2:
			hash(hole[0])
			hash(board)
			self.data = (hole[0], board, tuple(bets[0]), tuple(bets[1]))
		else:
			self.data = (hole, board,
				tuple(bets[0]),
				tuple(bets[1]),
				tuple(bets[2]),
				tuple(bets[3]))

	def __eq__(self, other):
		return self.data == other.data

	def __hash__(self):
		return hash((self.data,))

	def __repr__(self):
		return str(self.data)
