from InfoSet import InfoSet

# A GameState tracks the progress of a game and can give information about it
# In particular, it can provide the infosets each player sees
class GameState:
	
	def __init__(self):
		self.player1_hole_cards = None
		self.player2_hole_cards = None
		self.flop_cards = None
		self.turn_card = None
		self.river_card = None

		self.preflop_actions = None
		self.flop_actions = None
		self.turn_actions = None
		self.river_actions = None

		# Following variables are NOT part of the InfoSet, maintained for convenience
		# Increase this on Call or Raise (increase by the amount of original bet) actions
		self.pot_size = 0
		# Set this to the other player when one player Folds, or determine at showdown
		self.winner = None
		# Keep track of what round of betting it is - 0 is preflop, 1 flop, 2 turn, 3 river
		self.round = 0

		# meta
		self.cards = [self.flop_cards, self.turn_card, self.river_card]
		self.actions = [self.preflop_actions, self.flop_actions, self.turn_actions, self.river_actions]


	def get_infoset(self, player):
		if player == 1:
			return InfoSet(self, self.player1_hole_cards)
		elif player == 2:
			return InfoSet(self, self.player2_hole_cards)
		else:
			raise Exception('player must be 1 or 2')

	def is_terminal(self):
		# note that pre-flop, player1 is the small blind
		# note that post-flop, player1 is the big blind

		if self.is_showdown():
			return True

		last_actions = None
		# find the last round where there is action
		for actions in [self.river_actions, self.turn_actions, self.flop_actions, self.preflop_actions]:
			last_actions = actions
			if actions is not None:
				break

		# each round needs at least two actions to be complete
		if len(last_actions) < 2:
			return false

		# check if the last action is fold
		return last_actions[-1] == 'Fold'

	def get_utility(self, player):
		pot_size = self.pot_size
		winner = self.get_winner()
		return pot_size if winner == player else -pot_size

	def is_showdown(self):
		# conditions for reaching showdown, last round is either check/check, bet/call, or raise/call
		if self.river_actions is not None:
			return self.is_round_complete(self.river_actions)
		return False

	def get_winner(self):
		if self.winner is not None:
			return self.winner
		return self.showdown()

	def showdown(self):
		# return the winner at showdown
		# TODO: implement correctly, compare best 5-card hands and pick best player
		return 0

	def update(self, player, action):
		# update the game state according to the player and the action
		# will need to find the current betting round if not maintained
		# raise exceptions at any point where the action does not seem valid
		# include a reason why
		# TODO: implement correctly

	def is_round_complete(self, actions):
		if len(actions) >= 2:
			last_action = actions[-1]
			second_last_action = actions[-2]
			if last_action.action == 'Check' and second_last_action.action == 'Check':
				return True
			elif last_action.action == 'Call' and second_last_action.action in ['Bet', 'Raise']:
				return True
		return False

	def get_players_turn(self):
		if self.round == 0:
			return len(self.preflop_actions) % 2 + 1
		if len(self.actions[self.round]) == 0 and self.cards[self.round] is None:
			return 0
		else:
			return len(self.actions[self.round]) + 1 % 2 + 1
