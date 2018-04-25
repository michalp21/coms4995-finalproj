import pickle
import random
from ESMCCFR import ESMCCFR_P
from deuces2.card import Card
from Strategy import Strategy

print("Welcome to Heads Up Texas No Limit Hold'Em")

infoset_strategy_map = pickle.load(open('strategy.pkl', 'rb'))
utility_methods = ESMCCFR_P()
State = utility_methods.initialize_State()

player = random.randint(1, 2)
print("You are player", player)
if player == 1:
	print("You are the big blind, you post", State.p1_contrib)
	print("Your private card is", Card.int_to_str(State.p1_card))
elif player == 2:
	print("You are the small blind, you post", State.p2_contrib)
	print("Your private card is", Card.int_to_str(State.p2_card))

while not State.is_terminal():
	players_turn = State.get_players_turn()
	possible_actions = State.get_possible_actions(players_turn)
	infoset = State.get_infoset(players_turn)
	if players_turn == player:
		print("The current community card is", [Card.int_to_str(c) for c in infoset.flop_card])
		print("You can bet the following amounts:", possible_actions)
		action = int(input('Your action: '))
		State.update(players_turn, action)
	else:
		strategy = Strategy(len(possible_actions))
		if infoset in infoset_strategy_map.keys():
			strategy = infoset_strategy_map[infoset]
			print("This strategy has seen this infoset before, and will play the following actions with the following probabilities")
			print(possible_actions, strategy.get_average_strategy())
		else:
			print("This strategy has never seen the following infoset before, and will therefore play randomly")
			print(infoset)
		action = utility_methods.get_random_action(strategy.get_average_strategy())
		print("Opponent has decided to take action", possible_actions[action])
		State.update(players_turn, possible_actions[action])

print("The game is over, your utility is", State.get_utility(player))
