# An InfoSet contains information about the GameState available to a player
# it implements __eq__ and __hash__ so it can be used as a key to look up strategies
# this class should be immutable as it is the key to look up strategies in a map

from deuces2.card import Card
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
		hc = [Card.int_to_str(c) for c in self.hole]
		fc = [[Card.int_to_str(c) for c in round_cards] for round_cards in self.board]
		return ('Hole: %s, Flop: %s' % (hc, fc) + ' Actions: ' +
			':'.join([','.join(str(h) for h in self.history[k])
			 for k in sorted(self.history)]))