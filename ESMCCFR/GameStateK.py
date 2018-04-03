from Card import Card
from Enums import *
from InfoSet import InfoSet
from ActionAndAmount import ActionAndAmount
from copy import deepcopy

# A GameState tracks the progress of a game and can give information about it
# In particular, it can provide the infosets each player sees
class GameStateK:
	
	def __init__(self):
		self.player1_hole_cards = []
		self.player2_hole_cards = []
		self.actions = ""

		# Following variables are NOT part of the InfoSet, maintained for convenience
		# Increase this on Call or Raise (increase by the amount of original bet) actions
		self.pot_size = 0
		# Set this to the other player when one player Folds, or determine at showdown
		self.winner = None
		# Keep track of what round of betting it is - 0 is preflop, 1 flop, 2 turn, 3 river
		self.round = 0

	def __deepcopy__(self, memo):
		cls = self.__class__
		result = cls.__new__(cls)
		memo[id(self)] = result
		for k, v in self.__dict__.items():
			setattr(result, k, deepcopy(v, memo))
		return result

	def get_infoset(self, player):
		if player == 1:
			return InfoSet(self, self.player1_hole_cards)
		elif player == 2:
			return InfoSet(self, self.player2_hole_cards)
		else:
			raise Exception('player must be 1 or 2')

	def is_terminal(self):
		##### TEMP
		if self.round >= 3:
			return True

		# note that pre-flop, player1 is the small blind
		# note that post-flop, player1 is the big blind

		if self.is_showdown():
			return True

		# find the last round where there is action
		if all(len(a)==0 for a in reversed(self.actions)):
			return False
		last_actions = next(a for a in reversed(self.actions) if a)

		# each round needs at least two actions to be complete
		if len(last_actions) < 2:
			return False

		# check if the last action is fold
		return last_actions[-1] == Action.FOLD

	def get_utility(self, player):
		pot_size = self.pot_size
		winner = self.get_winner()
		return pot_size if winner == player else -pot_size

	def is_showdown(self):
		# conditions for reaching showdown, last round is either check/check, bet/call, or raise/call
		
		#### NEED to do for all rounds
		if self.river_actions:
			return self.is_round_complete(self.river_actions)
		return False

	def get_winner(self):
		if self.winner:
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

		##### TEMP
		self.round+=1

	def is_round_complete(self, actions):
		if len(actions) >= 2:
			last_action = actions[-1]
			second_last_action = actions[-2]
			if last_action.action == Action.CHECK and second_last_action.action == Action.CHECK:
				return True
			elif last_action.action == Action.CALL and second_last_action.action in [Action.BET, Action.RAISE]:
				return True
		return False

	def get_players_turn(self):
		if self.round == 0:
			return len(self.preflop_actions) % 2 + 1
		if len(self.actions[self.round]) == 0 and self.cards[self.round] is None:
			return 0
		else:
			return len(self.actions[self.round]) + 1 % 2 + 1
