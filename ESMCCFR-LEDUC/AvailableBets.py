class AvailableBets():
	def __init__(self, setup):
		self.setup = setup

	def _get_debt(self, pov, oppo):
		debt = oppo - pov
		if debt < 0:
			raise Exception(
				'Debt %d < 0 for pov %d and oppo %d' %
				(debt, pov, oppo))
		return debt

	def _get_remaining(self, pov):
		remaining = self.setup.stack_size - pov
		if remaining <= 0:
			raise Exception(
				'Remaining %d <= 0 for pov %d and stack %d' %
				(remaining, pov, self.setup.stack_size))
		return remaining

	def _get_minimum_raise(self, debt):
		return debt + max(self.setup.big_blind, debt)

	def get_bets_as_numbers(self, pov, oppo, abstracted=False):
		debt = self._get_debt(pov, oppo)
		remaining = self._get_remaining(pov)
		minimum_raise = self._get_minimum_raise(debt)
		if abstracted:
			minimum_raise += minimum_raise % 2
		# set dedupes
		return list(sorted(set([0, debt] +
			list(range(minimum_raise, remaining+1, 2 if abstracted else 1))
			+ [remaining])))

	def get_bets_by_action_type(self, pov, oppo, abstracted=False):
		debt = self._get_debt(pov, oppo)
		remaining = self._get_remaining(pov)
		minimum_raise = self._get_minimum_raise(debt)
		if abstracted:
			minimum_raise += minimum_raise % 2

		bets = dict()
		if debt == 0:
			bets['check'] = [0]
		else:
			bets['fold'] = [0]
			bets['call'] = [debt]

		# all in is not considered a raise here
		raises = list(range(minimum_raise, remaining, 2 if abstracted else 1))
		if len(raises) > 0:
			bets['raises'] = raises

		if debt < remaining:
			bets['allIn'] = [remaining]

		return bets

	def get_action_type_for_bet(self, pov, oppo, bet):
		by_type = self.get_bets_by_action_type(pov, oppo)
		for key in by_type.keys():
			if bet in by_type[key]:
				return key
		raise Exception("Illegal bet")

	def get_word(self, actions, bet):
		return [key for key, value in actions.items() if bet in value][0]