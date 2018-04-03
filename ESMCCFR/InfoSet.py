# An InfoSet contains information about the GameState available to a player
# it implements __eq__ and __hash__ so it can be used as a key to look up strategies
# this class should be immutable as it is the key to look up strategies in a map
class InfoSet:

	def __init__(self, gamestate, hole_cards):
		self.hole_cards = tuple(hole_cards)
		self.flop_cards = tuple(gamestate.flop_cards)
		self.turn_card = gamestate.turn_card
		self.river_card = gamestate.river_card

		self.preflop_actions = tuple(gamestate.preflop_actions)
		self.flop_actions = tuple(gamestate.flop_actions)
		self.turn_actions = tuple(gamestate.turn_actions)
		self.river_actions = tuple(gamestate.river_actions)

	def __eq__(self, other):
		return self.hole_cards == other.hole_cards and self.flop_cards == other.flop_cards and self.turn_card == other.turn_card and self.river_card == other.river_card and self.preflop_actions == other.preflop_actions and self.flop_actions == other.flop_actions and self.turn_actions == other.turn_actions and self.river_actions == other.river_actions

	def __hash__(self):
		return hash((self.hole_cards, self.flop_cards, self.turn_card, self.river_card, self.preflop_actions, self.flop_actions, self.turn_actions, self.river_actions))