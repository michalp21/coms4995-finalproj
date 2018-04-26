# An InfoSet contains information about the State available to a player
# it implements __eq__ and __hash__ so it can be used as a key to look up strategies
# this class should be immutable as it is the key to look up strategies in a map

from deuces2.card import Card
from Utilities import *

class InfoSet:

	def __init__(self, hole, board, bets):
		self.hole = hole
		if len(bets) == 2:
			self.data = "%s:%s:%s,%s" % (hole[0], board, bets[0], bets[1])
		else:
			self.data = "%s:%s:%s,%s,%s,%s" % (hole, board, bets[0], bets[1], bets[2], bets[3])

	def __eq__(self, other):
		return self.data == other.data

	def __hash__(self):
		return hash((self.data,))

	def __repr__(self):
		return self.data