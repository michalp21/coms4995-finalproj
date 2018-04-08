from Card import Card
from Enums import *
from enum import Enum
import random

class ActionK(Enum):
	PASS = 0
	BET = 1
	NEWCARD = 2

class InfosetK:

	def __init__(self, hole_card, bet_sequence):
		self.hole_card = hole_card
		self.bet_sequence = bet_sequence

	def __repr__(self):
		trans = {ActionK.PASS: "p", ActionK.BET: "b", ActionK.NEWCARD: "n"}
		s = ""
		for a in reversed(self.bet_sequence[1:]):
			s = trans[a] + s
		s = str(self.hole_card) + s
		while len(s) != 3:
			s += " "
		return s

	def __lt__(self,other):
		return self.__repr__() < other.__repr__()

	def __eq__(self, other):
		return self.hole_card == other.hole_card and self.bet_sequence == other.bet_sequence

	def __hash__(self):
		return hash((self.hole_card, self.bet_sequence))

# A GameState tracks the progress of a game and can give information about it
# In particular, it can provide the infosets each player sees
class GameStateK:
	allowable_bet_sequences = {(), (ActionK.NEWCARD,), (ActionK.NEWCARD, ActionK.PASS), (ActionK.NEWCARD, ActionK.BET), (ActionK.NEWCARD, ActionK.PASS, ActionK.PASS), (ActionK.NEWCARD, ActionK.PASS, ActionK.BET), (ActionK.NEWCARD, ActionK.PASS, ActionK.BET, ActionK.PASS), (ActionK.NEWCARD, ActionK.PASS, ActionK.BET, ActionK.BET), (ActionK.NEWCARD, ActionK.BET, ActionK.PASS), (ActionK.NEWCARD, ActionK.BET, ActionK.BET)}
	terminal_bet_sequences = {(ActionK.NEWCARD, ActionK.PASS, ActionK.PASS), (ActionK.NEWCARD, ActionK.PASS, ActionK.BET, ActionK.PASS), (ActionK.NEWCARD, ActionK.PASS, ActionK.BET, ActionK.BET), (ActionK.NEWCARD, ActionK.BET, ActionK.PASS), (ActionK.NEWCARD, ActionK.BET, ActionK.BET)}
	
	def __init__(self):
		# Kuhn is small, so we can easily define all possible states
		self.player1_hole_card = None
		self.player2_hole_card = None
		self.bet_sequence = ()

	def deepcopy(self):
		gsk = GameStateK()
		gsk.player1_hole_card = self.player1_hole_card
		gsk.player2_hole_card = self.player2_hole_card
		gsk.bet_sequence = self.bet_sequence
		return gsk

	#Always bet and call in Kuhn
	def get_possible_actions(self):
		return [0,1]

	#Get Infoset
	def get_infoset(self, player):
		if player == 1:
			return InfosetK(self.player1_hole_card, self.bet_sequence)
		elif player == 2:
			return InfosetK(self.player2_hole_card, self.bet_sequence)
		else:
			raise Exception('player must be 1 or 2')

	def is_terminal(self):
		return self.bet_sequence in GameStateK.terminal_bet_sequences

	def get_utility(self, player):
		utility = None
		if self.bet_sequence == (ActionK.NEWCARD, ActionK.PASS, ActionK.PASS):
			utility = 1
		elif self.bet_sequence == (ActionK.NEWCARD, ActionK.PASS, ActionK.BET, ActionK.PASS):
			utility = 1
		elif self.bet_sequence == (ActionK.NEWCARD, ActionK.PASS, ActionK.BET, ActionK.BET):
			utility = 2
		elif self.bet_sequence == (ActionK.NEWCARD, ActionK.BET, ActionK.PASS):
			utility = 1
		elif self.bet_sequence == (ActionK.NEWCARD, ActionK.BET, ActionK.BET):
			utility = 2
		else:
			raise Exception('Invalid bet sequence?')

		winner = None
		if self.bet_sequence == (ActionK.NEWCARD, ActionK.BET, ActionK.PASS):
			winner = 1
		elif self.bet_sequence == (ActionK.NEWCARD, ActionK.PASS, ActionK.BET, ActionK.PASS):
			winner = 2
		else:
			if self.player1_hole_card > self.player2_hole_card:
				winner = 1
			else:
				winner = 2
		return utility if player == winner else -utility

	def update(self, player, action):
		action = (ActionK(action),)
		new_bet_sequence = self.bet_sequence + action

		if player == 0 and self.bet_sequence == ():
			
			if new_bet_sequence not in GameStateK.allowable_bet_sequences:
				raise Exception('Chance chose invalid action', new_bet_sequence)
			else:
				self.bet_sequence = new_bet_sequence
				sample = random.sample(range(1, 4), 2)
				self.player1_hole_card, self.player2_hole_card = sample[0], sample[1]

		elif player == (len(self.bet_sequence)+1) % 2 + 1:
			
			if new_bet_sequence not in GameStateK.allowable_bet_sequences:
				raise Exception('Player', player, 'chose invalid action', new_bet_sequence)
			else:
				self.bet_sequence = new_bet_sequence
		else:
			raise Exception('Player', player, 'cannot act on history', self.bet_sequence)

	def get_players_turn(self):
		if len(self.bet_sequence) == 0:
			return 0
		else:
			return (len(self.bet_sequence)+1) % 2 +1





