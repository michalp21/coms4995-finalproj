round_names = ['Preflop', 'Flop', 'Turn', 'River']

class Logger:
	def __init__(self, rules, setup, players):
		self.rules = rules
		self.setup = setup
		self.pov = players[0]
		self.opponent = players[1]

	def _cards(self, cards):
		if isinstance(cards, int):
			cards = [cards]
		return '[%s]' % ' '.join(self.rules.pretty(c) for c in cards)

	def round(self, gs, pov_seat):
	  	print("\tround=%s\t%s=%s, %s turn"  % (
  			round_names[gs.round],
  			self.pov,
  			self._cards(gs.deal.big if pov_seat == 1 else gs.deal.small),
  			self.pov if gs.get_players_turn() == pov_seat else self.opponent))

	def bet(self, gs, player, pov_seat, bet):
		print("\t\t%s\tbet=%d; %d v %d\n" % (
			player,
			bet, gs._my_contrib(pov_seat), gs._other_contrib(pov_seat)))

	def evaluate(self, gs, pov_seat):
		if gs.folded_player > 0:
			print("\t%s\tfolded" %
				(self.pov if gs.folded_player == pov_seat else self.opponent))
		else:
			print("\tShowdown: %s=%s. %s=%s. Board=%s." % (
				self.pov,
				self._cards(gs.deal.big if pov_seat == 1 else gs.deal.small),
				self.opponent,
				self._cards(gs.deal.small if pov_seat == 1 else gs.deal.big),
				self._cards(gs.deal.join_board())))

	def earnings(self, util):
		if util == 0:
			verb = 'tied'
		elif util > 0:
			verb = 'won'
		else:
			verb = 'lost'
		print("\t%s %s %d dollars \n" % (self.pov, verb, util))

