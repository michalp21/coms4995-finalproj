from AvailableBets import AvailableBets

from Setup import Setup

# throw error when it's not my turn
available_bets = AvailableBets(
	Setup(small_blind=2, big_blind=5, stack_size=11))
exception_thrown = False
try:
	available_bets.get_bets_as_numbers(6, 5)
except:
	exception_thrown = True
assert exception_thrown

exception_thrown = False
try:
	available_bets.get_bets_by_action_type(6, 5)
except:
	exception_thrown = True
assert exception_thrown

# throw error when I'm out of chips
available_bets = AvailableBets(
	Setup(small_blind=2, big_blind=5, stack_size=11))
exception_thrown = False
try:
	available_bets.get_bets_as_numbers(8, 7)
except:
	exception_thrown = True
assert exception_thrown

exception_thrown = False
try:
	available_bets.get_bets_by_action_type(8, 7)
except:
	exception_thrown = True
assert exception_thrown

# I must meet big blind
available_bets = AvailableBets(
	Setup(small_blind=2, big_blind=5, stack_size=11))
bets = available_bets.get_bets_as_numbers(2, 5)
actions = available_bets.get_bets_by_action_type(2, 5)
assert bets == [0, 3, 8, 9], str(bets)
assert actions == {
	'fold': [0],
	'call': [3],
	'raises': [8],
	'allIn': [9]
}, str(actions)

# All in call must be available
available_bets = AvailableBets(
	Setup(small_blind=2, big_blind=5, stack_size=11))
bets = available_bets.get_bets_as_numbers(10, 11)
actions = available_bets.get_bets_by_action_type(10, 11)
assert bets == [0, 1], str(bets)
assert actions == {
	'fold': [0],
	'call': [1]
}, str(actions)

# I can check
available_bets = AvailableBets(
	Setup(small_blind=2, big_blind=5, stack_size=11))
bets = available_bets.get_bets_as_numbers(5, 5)
actions = available_bets.get_bets_by_action_type(5, 5)
assert bets == [0, 5, 6], str(bets)
assert actions == {
	'check': [0],
	'raises': [5],
	'allIn': [6]
}, str(actions)

# All in raise must be available
available_bets = AvailableBets(
	Setup(small_blind=2, big_blind=5, stack_size=11))
bets = available_bets.get_bets_as_numbers(10, 10)
actions = available_bets.get_bets_by_action_type(10, 10)
assert bets == [0, 1], str(bets)
assert actions == {
	'check': [0],
	'allIn': [1]
}, str(actions)

# Small blind can check when equal
available_bets = AvailableBets(
	Setup(small_blind=1, big_blind=1, stack_size=5))
bets = available_bets.get_bets_as_numbers(1, 1)
actions = available_bets.get_bets_by_action_type(1, 1)
assert bets == [0, 1, 2, 3, 4], str(bets)
assert actions == {
	'check': [0],
	'raises': [1, 2, 3],
	'allIn': [4]
}, str(actions)

print("AvailableBetsTest passed")