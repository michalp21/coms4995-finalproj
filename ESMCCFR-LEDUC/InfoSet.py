# An InfoSet contains information about the GameState available to a player
# it implements __eq__ and __hash__ so it can be used as a key to look up strategies
# this class should be immutable as it is the key to look up strategies in a map

from deuces2.card import Card
from Utilities import *
import copy

class InfoSet:

	def __init__(self, hole, board, history):
		self.data = "%s:%s:%s,%s" % (hole, board, history[0], history[1])

	def __eq__(self, other):
		return self.data == other.data

	def __hash__(self):
		return hash((self.data,))

	def __repr__(self):
		return self.data