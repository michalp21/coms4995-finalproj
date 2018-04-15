# An InfoSet contains information about the GameState available to a player
# it implements __eq__ and __hash__ so it can be used as a key to look up strategies
# this class should be immutable as it is the key to look up strategies in a map

from deuces2.card import Card
class InfoSet:

	def __init__(self, gamestate, hole_cards):
		#NEED TO UPDATE THIS TO ONLY GIVE THE COMMUNITY CARDS PLAYERS CAN ACCESS!!!
		self.hole_cards = tuple(hole_cards)
		self.flop_cards = () if gamestate.round < 1 else tuple(gamestate.flop_cards)
		self.turn_card = () if gamestate.round < 2 else (gamestate.turn_card,)
		self.river_card = () if gamestate.round < 3 else (gamestate.river_card,)

		self.actions = gamestate.actions

	def __eq__(self, other):
		return self.hole_cards == other.hole_cards and self.flop_cards == other.flop_cards and self.turn_card == other.turn_card and self.river_card == other.river_card and self.actions == other.actions
	def __hash__(self):
		# print(type(tuple([(k, v) for k, v in self.actions.items()])))
		return hash((self.hole_cards, self.flop_cards, self.turn_card, self.river_card, tuple([(k, tuple(v)) for k, v in self.actions.items()])))

	def __repr__(self):
		# print('actions', self.actions)
		hc = [Card.int_to_str(c) for c in self.hole_cards]
		fc = [Card.int_to_str(c) for c in self.flop_cards] if len(self.flop_cards) > 0 else ''
		tc = Card.int_to_str(self.turn_card[0]) if len(self.turn_card) > 0 else ''
		rc = Card.int_to_str(self.river_card[0]) if len(self.river_card) > 0 else ''
		return 'Hole Cards: %s, Flop Cards: %s, Turn Card: %s, River Card: %s' % (hc, fc, tc, rc) + ' Actions: ' + ':'.join([','.join(str(h) for h in self.actions[k]) for k in sorted(self.actions)])