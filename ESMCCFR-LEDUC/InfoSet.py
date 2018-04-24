# An InfoSet contains information about the GameState available to a player
# it implements __eq__ and __hash__ so it can be used as a key to look up strategies
# this class should be immutable as it is the key to look up strategies in a map

from deuces2.card import Card
from Utilities import *

class InfoSet:

	def __init__(self, hole, board, history):
		if len(history) == 2:
			self.data = "%s:%s:%s,%s" % (hole, board, history[0], history[1])
		else:
			self.data = "%s:%s:%s,%s,%s,%s" % (hole, board, history[0], history[1], history[2], history[3])

	def __eq__(self, other):
		return self.data == other.data

	def __hash__(self):
		return hash((self.data,))

	def __repr__(self):
		return self.data