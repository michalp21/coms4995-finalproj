from Card import Card
from Enums import *
from InfoSet import InfoSet
from ActionAndAmount import ActionAndAmount
from copy import deepcopy
from enum import Enum
import random

class Action(Enum):
	PASS = 0
	BET = 1
	NEWCARD = 2

class InfoSetKuhn:

	def __init__(self, hole_card, bet_sequence):
		self.hole_card = hole_card
		self.bet_sequence = bet_sequence

	def __repr__(self):
		trans = {Action.PASS: "p", Action.BET: "b", Action.NEWCARD: "n"}
		s = ""
		for a in reversed(self.bet_sequence):
			s = trans[a] + s
		s = str(self.hole_card) + s
		while len(s) != 4:
			s += " "
		return s

	def __eq__(self, other):
		return self.hole_card == other.hole_card and self.bet_sequence == other.bet_sequence

	def __hash__(self):
		return hash((self.hole_card, self.bet_sequence))

# A GameState tracks the progress of a game and can give information about it
# In particular, it can provide the infosets each player sees
class GameStateK:
	
	def __init__(self):
		# Kuhn is small, so we can easily define all possible states
		self.player1_hole_card = None
		self.player2_hole_card = None
		self.bet_sequence = ()
		self.allowable_bet_sequences = set([(), (Action.NEWCARD,), (Action.NEWCARD, Action.PASS), (Action.NEWCARD, Action.BET), (Action.NEWCARD, Action.PASS, Action.PASS), (Action.NEWCARD, Action.PASS, Action.BET), (Action.NEWCARD, Action.PASS, Action.BET, Action.PASS), (Action.NEWCARD, Action.PASS, Action.BET, Action.BET), (Action.NEWCARD, Action.BET, Action.PASS), (Action.NEWCARD, Action.BET, Action.BET)])
		self.terminal_bet_sequences = set([(Action.NEWCARD, Action.PASS, Action.PASS), (Action.NEWCARD, Action.PASS, Action.BET, Action.PASS), (Action.NEWCARD, Action.PASS, Action.BET, Action.BET), (Action.NEWCARD, Action.BET, Action.PASS), (Action.NEWCARD, Action.BET, Action.BET)])
		self.pot_size = 2

	def __deepcopy__(self, memo):
		cls = self.__class__
		result = cls.__new__(cls)
		memo[id(self)] = result
		for k, v in self.__dict__.items():
			setattr(result, k, deepcopy(v, memo))
		return result

	def get_possible_actions(self):
		return {0,1}

	def get_infoset(self, player):
		if player == 1:
			return InfoSetKuhn(self.player1_hole_card, self.bet_sequence)
		elif player == 2:
			return InfoSetKuhn(self.player2_hole_card, self.bet_sequence)
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
		action = Action(action)
		if player == 0 and self.bet_sequence == ():
			bet_sequence_list = list(self.bet_sequence)
			bet_sequence_list.append(action)
			bet_sequence_tuple = tuple(bet_sequence_list)
			if bet_sequence_tuple not in self.allowable_bet_sequences:
				raise Exception('Chance chose invalid action', bet_sequence_tuple)
			else:
				self.bet_sequence = bet_sequence_tuple
				sample = random.sample(range(1, 4), 2)
				self.player1_hole_card, self.player2_hole_card = sample[0], sample[1]

		elif player == (len(self.bet_sequence)+1) % 2 + 1:
			bet_sequence_list = list(self.bet_sequence)
			bet_sequence_list.append(action)
			bet_sequence_tuple = tuple(bet_sequence_list)
			if bet_sequence_tuple not in self.allowable_bet_sequences:
				raise Exception('Player', player, 'chose invalid action', bet_sequence_tuple)
			else:
				self.bet_sequence = bet_sequence_tuple
			if action == Action.PASS or action == Action.BET:
				self.pot_size += 1
		else:
			raise Exception('Player', player, 'cannot act on history', self.bet_sequence)

	def get_players_turn(self):
		if len(self.bet_sequence) == 0:
			return 0
		else:
			return (len(self.bet_sequence)+1) % 2 +1





