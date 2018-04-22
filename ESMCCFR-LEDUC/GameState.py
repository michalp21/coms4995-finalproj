from Evaluator import Evaluator
from InfoSet import InfoSet
from copy import deepcopy
from deuces2.card import Card

# A GameState tracks the progress of a game and can give information about it
# In particular, it can provide the infosets each player sees
class GameState:
	
	def __init__(self, p1_card, p2_card, flop_card):
		self.evaluator = Evaluator()
		self.players = set([1,2])
		self.p1_card = p1_card
		self.p2_card = p2_card
		self.flop_card = flop_card

		# original contribution is blinds. p1 goes first on every round except first one
		self.p1_contrib = 200
		self.p2_contrib = 100
		# stack size is always 2,000 (scale later), bet abstraction is 100 for now
		self._stack_size = 500
		self._bet_increment = 100

		# Keep track of what round of betting it is - 0 is preflop, 1 flop, 2 terminal
		self.round = 0

		# meta
		self.player_turn = 2
		self.actions = {0: [], 1: []}

	def __deepcopy__(self, memo):
		cls = self.__class__
		result = cls.__new__(cls)
		memo[id(self)] = result
		for k, v in self.__dict__.items():
			setattr(result, k, deepcopy(v, memo))
		return result

	def __repr__(self):
		hc = [Card.int_to_str(self.p1_card), Card.int_to_str(self.p2_card)]
		fc = [Card.int_to_str(self.flop_card)] if self.flop_card else ''
		return 'Hole Card: %s, Flop Card: %s' % (hc, fc) + ' Actions: ' + ':'.join([','.join(str(h) for h in self.actions[k]) for k in sorted(self.actions)]) + 'Round:' + str(self.round)

	def deepcopy(self):
		# copy over the fields that change.
		# stack_size and bet_increment do not change within a run of ESMCCFR
		# cards and actions will reference the correct values by default which are set
		gamestate = GameState(self.p1_card, self.p2_card, self.flop_card)
		gamestate.players = deepcopy(self.players)
		gamestate.actions = deepcopy(self.actions)
		gamestate.p1_contrib = self.p1_contrib
		gamestate.p2_contrib = self.p2_contrib
		gamestate.round = self.round
		gamestate.player_turn = self.player_turn 
		return gamestate

	def get_possible_actions(self, player):
		# returns a list of amounts of chips that can be added to pot in appropriate increments
		minimum = abs(self.p1_contrib - self.p2_contrib)//self._bet_increment
		maximum = (self._stack_size - min(self.p1_contrib, self.p2_contrib))//self._bet_increment
		possible_actions = [b*self._bet_increment for b in range(minimum, maximum + 1)]
		# action of 0 when less than required amount will be a fold
		if minimum > 0:
			possible_actions.insert(0, 0)
		return possible_actions

	def get_infoset(self, player):
		if player == 1:
			return InfoSet(self, self.p1_card)
		elif player == 2:
			return InfoSet(self, self.p2_card)
		else:
			raise Exception('player must be 1 or 2')

	def is_terminal(self):
		return len(self.players) == 1 or self.round == 2

	def get_utility_folder(self, player):
		# print('folder!!!', self.round)
		# if p1 wins, p1 wins what p2 contributed and vice versa
		# if p1 loses, p1 loses what p1 contributed and vice versa
		if player in self.players:
			return self.p2_contrib if player == 1 else self.p1_contrib
		else:
			return -self.p1_contrib if player == 1 else -self.p2_contrib

	def get_utility_showdown(self, player):
		p1_hand_rank = self.evaluator.evaluate(self.p1_card, self.flop_card)
		p2_hand_rank = self.evaluator.evaluate(self.p2_card, self.flop_card)
		if p1_hand_rank == p2_hand_rank:
			return 0
		elif p1_hand_rank < p2_hand_rank:
			return self.p2_contrib if player == 1 else -self.p2_contrib
		elif p2_hand_rank < p1_hand_rank:
			return self.p1_contrib if player == 2 else -self.p1_contrib
		else: raise Exception ('How did we get here?')

	def get_utility(self, player):
		# print(self)
		if len(self.players) == 1:
			return self.get_utility_folder(player)
		else:
			return self.get_utility_showdown(player)


	def update(self, player, amount):
		# print('before', self.p1_contrib, self.p2_contrib, player, amount)
		# print(player, amount)
		if player == 1:
			# always record what the player did
			self.actions[self.round].append(amount)
			# change turn to other player, even if round advances, as per rules!!!
			self.player_turn = 2
			# player folds or checks
			if amount == 0:
				# player folds, removed from game
				if self.p1_contrib < self.p2_contrib:
					# print('removing player', player)
					self.players.remove(player)
				# player checks
				elif self.p1_contrib == self.p2_contrib:
					# do not advance round if first-turn check!
					if len(self.actions[self.round]) > 1:
						self.round += 1
				else: raise Exception('How did we get here?')
			# player calls, round advances
			elif self.p1_contrib + amount == self.p2_contrib:
				self.p1_contrib += amount
				self.round += 1
			# player raises, round does not advance
			elif self.p1_contrib + amount > self.p2_contrib:
				self.p1_contrib += amount
			else: raise Exception('How did we get here?')

		# the exact opposite of the above
		elif player == 2:
			# change turn to the other player, unless the round advances!!!
			self.player_turn = 1
			self.actions[self.round].append(amount)
			if amount == 0:
				if self.p2_contrib < self.p1_contrib:
					# print('removing player', player)
					self.players.remove(player)
				elif self.p2_contrib == self.p1_contrib:
					if len(self.actions[self.round]) > 1:
						self.round += 1
						self.player_turn = 2
				else: raise Exception('How did we get here?')
			elif self.p2_contrib + amount == self.p1_contrib:
				self.p2_contrib += amount
				# if p2_contrib == 200, then it was a big blind call, big blind needs option
				if self.p2_contrib > 200:
					self.round += 1
			elif self.p2_contrib + amount > self.p1_contrib:
				self.p2_contrib += amount
			else: 
				# print(amount, self.p1_contrib, self.p2_contrib)
				raise Exception('How did we get here?')
		else: raise Exception('How did we get here?')

		# print('after', self.p1_contrib, self.p2_contrib, player, amount, self.players)

	def get_players_turn(self):
		return self.player_turn
