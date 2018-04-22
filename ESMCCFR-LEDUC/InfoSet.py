# An InfoSet contains information about the GameState available to a player
# it implements __eq__ and __hash__ so it can be used as a key to look up strategies
# this class should be immutable as it is the key to look up strategies in a map

from deuces2.card import Card
class InfoSet:

	def __init__(self, gamestate, hole_card):
		self.hole_card = tuple([hole_card])
		self.flop_card = () if gamestate.round < 1 else tuple([gamestate.flop_card])
		self.history = gamestate.history

	def __eq__(self, other):
		return self.hole_card == other.hole_card and self.flop_card == other.flop_card and self.history == other.history
	def __hash__(self):
		return hash((self.hole_card, self.flop_card, tuple([(k, tuple(v)) for k, v in self.history.items()])))

	def __repr__(self):
		hc = [Card.int_to_str(c) for c in self.hole_card]
		fc = [Card.int_to_str(c) for c in self.flop_card] if len(self.flop_card) > 0 else ''
		return ('Hole: %s, Flop: %s' % (hc, fc) + ' Actions: ' +
			':'.join([','.join(str(h) for h in self.history[k])
			 for k in sorted(self.history)]))