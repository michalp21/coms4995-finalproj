import random
from ESMCCFR import ESMCCFR_P
from deuces2.deck import Deck
from deuces2.card import Card
from GameState import GameState
from Strategy import Strategy

human = random.choice([1, 2])
computer = 3 - human


print("Training strategy")

cards = 6
strategy_map = ESMCCFR_P(cards).run(20000)

print("Done training")

def play_game():
  if cards == 52:
    deck = Deck(52)
    p1 = deck.draw(2)
    p2 = deck.draw(2)
    board = [ deck.draw(3), [deck.draw(1)], [deck.draw(1)] ]
  else:
    deck = Deck(6)
    p1 = [deck.draw(1)]
    p2 = [deck.draw(1)]
    board = [[deck.draw(1)]]

  round_names = ['Pre-flop', 'Flop', 'Turn', 'River']
  round = 0


  gs = GameState(p1_hole=p1, p2_hole=p2,
    poker_config=(GameState.hunl if cards == 52 else GameState.leduc),
    board=board)

  print("Your cards:")
  Card.print_pretty_cards(p1 if human == 1 else p2)
  print("%s round" % round_names[round])

  while not gs.is_terminal():
    player_turn = gs.get_players_turn()
    possible_actions = gs.get_possible_actions(player_turn)

    if player_turn == human:
      action = -1
      while action not in possible_actions:
        # action = int(input("Human's turn: select bet from %s:\n" % str(possible_actions)))
        action = possible_actions[-1]
    else:
      infoset = gs.get_infoset(player_turn)
      if infoset in strategy_map.keys():
        strategy = strategy_map[infoset]
      else:
        strategy = Strategy(len(possible_actions))
      now_strategy = strategy.calculate_strategy()
      action = possible_actions[random.choices(list(range(len(now_strategy))),
        weights=now_strategy, k=1)[0]]

      print("Computer's turn: computer bets: %d" % action)


    gs.update(player_turn, action)
    print("Contributions: human %d, computer %d" % (gs._my_contrib(human), gs._other_contrib(human)))

    if gs.round > round:
      print("%s round:" % (round_names[round]))
      Card.print_pretty_cards(board[round-1])
      round = gs.round

  util = gs.get_utility(human)
  if gs.folded_player == human:
    print("Human folded")
  elif gs.folded_player == computer:
    print("Computer folded")
  else:
    print("Game went to showdown")
    print("Your cards: ")
    Card.print_pretty_cards(p1 if human == 1 else p2)
    Card.print_pretty_cards(p2 if human == 1 else p1)
    print("Board:")
    Card.print_pretty_cards((board[0] + board[1] + board[2]) if cards == 52 else board[0])

  print(("You won %d dollars " if util > 0 else "You lost %d dollars") % util)
  return util

games = 0
total = 0
while True:
  total += play_game()
  games += 1
  print("Total winnings: (%.2f avg) %d / %d games" % ((1.0 *total) / games, total, games))
#  print("-------------------------")
#  print("|     Playing again     |")
#  print("-------------------------")