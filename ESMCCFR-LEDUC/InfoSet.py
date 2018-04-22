# An InfoSet contains information about the GameState available to a player
# it implements __eq__ and __hash__ so it can be used as a key to look up strategies
# this class should be immutable as it is the key to look up strategies in a map

from deuces2.card import Card
from Utilities import *
class InfoSet:

	def __init__(self, hole, board, history):
		self.hole = hole
		self.board = board
		self.history = history

	def __eq__(self, other):
		return self.hole == other.hole and self. board == other.board and self.history == other.history
	def __hash__(self):
		return hash((self.hole, self.board, tuple([(k, tuple(v)) for k, v in self.history.items()])))

	def __repr__(self):
		return ('Hole: %s, Flop: %s, Actions: %s' %
			(repr_hole(self.hole), repr_board(self.board), repr_history(self.history)))