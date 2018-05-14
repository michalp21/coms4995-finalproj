# An InfoSet contains information about the State available to a player
# it implements __eq__ and __hash__ so it can be used as a key to look up strategies
# this class should be immutable as it is the key to look up strategies in a map

from deuces2.card import Card

class InfoSet:

	def __init__(self, hole, board, bets):
		self.hole = hole[0]
		self.board = 0 if len(board) == 0 else board[0][0]
		self.bets_0 = tuple(bets[0])
		self.bets_1 = tuple(bets[1])
	def __eq__(self, other):
		return self.hole == other.hole and self.board == other.board and self.bets_0 == other.bets_0 and self.bets_1 == other.bets_1

	def __lt__(self, other):
		if self.hole == other.hole:
			if self.board == other.board:
				if self.bets_0 == other.bets_0:
					return self.bets_1 < other.bets_1
				else:
					return self.bets_0 < other.bets_0
			else:
				return self.board < other.board
		else:
			return self.hole < other.hole

	def __hash__(self):
		return hash((self.hole, self.board, self.bets_0, self.bets_1))

	def __repr__(self):
		return "hole=%d,board=%d,bets_0=%s,bets_1=%s" % (
			self.hole, self.board, str(self.bets_0), str(self.bets_1))
