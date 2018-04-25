import random
from ESMCCFR import ESMCCFR_P
from deuces2.deck import Deck
from deuces2.card import Card
from GameState import GameState
from GameDefinition import GameDefinition
from GameSetup import GameSetup
from Strategy import Strategy

human = random.choice([1, 2])
computer = 3 - human


print("Training strategy")

cards = 6
strategy_map = ESMCCFR_P(cards).run(5000)

print("Done training")

def pp(cards):
  if isinstance(cards, int):
    cards = [cards]
  return '[' + ' '.join([Card.int_to_pretty_str(c) for c in cards]) + ']'

def play_game():
  game_def = GameDefinition.leduc
  game_setup = GameSetup(small_blind=1, big_blind=2, stack_size=5)

  round_names = ['Pre-flop', 'Flop', 'Turn', 'River']
  round = 0
  gs = GameState(game_definition=game_def, game_setup=game_setup, deal=game_def.deal())

  print("%s round, your cards: %s" % (round_names[round], pp(gs.deal.p1 if human == 1 else gs.deal.p2)))

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
      print("%s round: %s" % (round_names[gs.round], pp(gs.deal.board[gs.round-1])))
      round = gs.round

  util = gs.get_utility(human)
  if gs.folded_player == human:
    print("Human folded")
  elif gs.folded_player == computer:
    print("Computer folded")
  else:
    print("Game went to showdown. Your cards: %s. Opponent: %s. Board: %s" %
      (pp(gs.deal.p1 if human == 1 else gs.deal.p2), pp(gs.deal.p2 if human == 1 else gs.deal.p1),
      pp((gs.deal.board[0] + gs.deal.board[1] + gs.deal.board[2]) if cards == 52 else gs.deal.board[0])))

  print(("You won %d dollars " if util > 0 else "You lost %d dollars") % abs(util))
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