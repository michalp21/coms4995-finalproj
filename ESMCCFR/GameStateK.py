from Card import Card
from Enums import *
from InfoSet import InfoSet
from ActionAndAmount import ActionAndAmount
from copy import deepcopy
from enum import Enum

class Actions(Enum):
	FOLD = 0
	CHECK = 1
	CALL = 2
	BET = 3

class InfoSetKuhn:

	def __init__(self, hole_card, bet_sequence):
		self.hole_card = hole_card
		self.bet_sequence = bet_sequence

# A GameState tracks the progress of a game and can give information about it
# In particular, it can provide the infosets each player sees
class GameStateKuhn:
	
	def __init__(self):
		# Kuhn is small, so we can easily define all possible states
		self.player1_hole_card = None
		self.player2_hole_card = None
		self.bet_sequence = ()
		self.allowable_bet_sequences = set([(), (Actions.CHECK), (Actions.CHECK, Actions.CHECK), (Actions.CHECK, Actions.BET), (Actions.CHECK, Actions.BET, Actions.FOLD), (Actions.CHECK, Actions.BET, Actions.CALL), (Actions.BET, Actions.FOLD), (Actions.BET, Actions.CALL)])
		self.terminal_bet_sequences = set([(Actions.CHECK, Actions.CHECK), (Actions.CHECK, Actions.BET, Actions.FOLD), (Actions.CHECK, Actions.BET, Actions.CALL), (Actions.BET, Actions.FOLD), (Actions.BET, Actions.CALL)])
		self.pot_size = 2

	def __deepcopy__(self, memo):
		cls = self.__class__
		result = cls.__new__(cls)
		memo[id(self)] = result
		for k, v in self.__dict__.items():
			setattr(result, k, deepcopy(v, memo))
		return result

	def get_infoset(self, player):
		if player == 1:
			return InfoSet(self.player1_hole_card, self.bet_sequence)
		elif player == 2:
			return InfoSet(self.player2_hole_card, self.bet_sequence)
		else:
			raise Exception('player must be 1 or 2')

	def is_terminal(self):
		return self.bet_sequence in self.terminal_bet_sequences

	def get_utility(self, player):
		if player == 1:
			if self.player1_hole_card > self.player2_hole_card:
				return self.pot_size
			else:
				return -self.pot_size
		elif player == 2:
			if self.player1_hole_card > self.player2_hole_card:
				return -self.pot_size
			else:
				return self.pot_size

	def update(self, player, action):
		if player != len(self.bet_sequence) % 2:
			bet_sequence_list = list(self.bet_sequence)
			bet_sequence_list.append(action)
			bet_sequence_tuple = tuple(bet_sequence_list)
			if bet_sequence_tuple not in self.allowable_bet_sequences:
				raise Exception('Player', player, 'chose invalid action', bet_sequence_tuple)
			else:
				self.bet_sequence = bet_sequence_tuple
			if action == Actions.CALL or action == Actions.BET:
				self.pot_size += 1
		else:
			raise Exception('Player', player, 'cannot act on history', self.bet_sequence)


	def get_players_turn(self):
		return len(bet_sequence) % 2 + 1
