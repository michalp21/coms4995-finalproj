import random
from ESMCCFR import ESMCCFR_P
from deuces2.deck import Deck
from deuces2.card import Card
from players.Human import Human
from players.ESMCCFRPlusTraining import ESMCCFRPlusTraining
from State import State
from Rules import Rules
from Setup import Setup
from Strategy import Strategy

round_names = ['Pre-flop', 'Flop', 'Turn', 'River']

def pp(cards):
  if isinstance(cards, int):
    cards = [cards]
  return '[' + ' '.join([Card.int_to_pretty_str(c) for c in cards]) + ']'

def play_game(rules, setup, pov_player, opponent):
  pov_seat = random.choice([1, 2])
  opponent_seat = 3 - pov_seat

  round = 0
  gs= State(rules=rules, setup=setup, deal=rules.deal())

  print("%s round, your cards: %s" % (round_names[round], pp(gs.deal.big if pov_seat == 1 else gs.deal.small)))

  while not gs.is_terminal():
    player_turn = gs.get_players_turn()
    player = pov_player if player_turn == pov_seat else opponent
    bet = player.bet(gs)
    gs.update(bet)
    print("Contributions: %s %d, %s %d" %
      (pov_player.name(),
       gs._my_contrib(pov_seat),
       opponent.name(),
       gs._other_contrib(pov_seat)))

    if gs.round > round and gs.round < len(gs.deal.board):
      print("%s round: %s" % (round_names[gs.round], pp(gs.deal.board[gs.round-1])))
      round = gs.round

  # after end
  util = gs.get_utility(pov_seat)

  if gs.folded_player > 0:
    print("%s folded" % (pov_player
      if gs.folded_player == pov_seat else opponent).name())
  else:
    print("Showdown: player cards: %s. Opponent: %s. Board: %s" %
      (pp(gs.deal.big if pov_seat == 1 else gs.deal.small),
       pp(gs.deal.small if pov_seat == 1 else gs.deal.big),
       pp(gs.deal.join_board())))

  print("You won %d dollars " if util >= 0 else "You lost %d dollars"
    % abs(util))
  return util


def main():
  rules = Rules.hunl
  setup = Setup(small_blind=1, big_blind=2, stack_size=5)
  pov_player = Human(rules, setup)
  opponent = ESMCCFRPlusTraining(rules, setup)

  pov_player.train(1)
  opponent.train(1000)

  games = 0
  total = 0
  for _ in range(10000):
      total += play_game(rules=rules,
       setup=setup, pov_player=pov_player, opponent=opponent)
      games += 1
      print("Total: (%.2f avg) %d / %d games" % ((1.0 *total) / games, total, games))

if __name__ == '__main__':
    main()