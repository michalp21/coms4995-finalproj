import random
from ESMCCFR import ESMCCFR_P
from deuces2.deck import Deck
from deuces2.card import Card
from players.Human import Human
from players.AllIn import AllIn
from players.AllInExceptQueens import AllInExceptQueens
from players.ESMCCFRPlusTraining import ESMCCFRPlusTraining
from State import State
from rules.Hunl import Hunl
from rules.Leduc import Leduc
from rules.Kuhn import Kuhn
from Setup import Setup
from Strategy import Strategy
from players.AllInOnAce import AllInOnAce

round_names = ['Preflop', 'Flop', 'Turn', 'River']

class Contest:

  def __init__(self, rules, setup, pov, opponent):
    self.rules = rules
    self.setup = setup
    self.pov = pov
    self.opponent = opponent

  def pp(self, cards):
    if isinstance(cards, int):
      cards = [cards]
    return '[' + ' '.join([self.rules.pretty(c) for c in cards]) + ']'

  def play(self):
    pov_seat = random.choice([1, 2])
    opponent_seat = 3 - pov_seat

    round = 0
    gs= State(rules=self.rules, setup=self.setup, deal=self.rules.deal())

    print("\tround=%s, %s=%s, %s starts" %
      (round_names[round], self.pov.name(),
       self.pp(gs.deal.big if pov_seat == 1 else gs.deal.small),
       self.pov.name() if pov_seat == 2 else self.opponent.name()))

    while not gs.is_terminal():
      turn = gs.get_players_turn()
      player = self.pov if turn == pov_seat else self.opponent
      bet = player.bet(gs)
      gs.update(bet)
      print("\t\t%s bet=%d. %d v. %d" %
        (self.pov.name(), bet,
         gs._my_contrib(pov_seat),
         gs._other_contrib(pov_seat)))

      if gs.round > round and gs.round < len(gs.deal.board):
        # print round and new cards
        print("\t%s=%s" % (round_names[gs.round], self.pp(gs.deal.board[gs.round-1])))
        round = gs.round

    # after end
    util = gs.get_utility(pov_seat)

    if gs.folded_player > 0:
      print("\t%s folded" % (self.pov
        if gs.folded_player == pov_seat else self.opponent).name())
    else:
      print("\tShowdown:  %s=%s. %s=%s. Board=%s." %
        (self.pov.name(), self.pp(gs.deal.big if pov_seat == 1 else gs.deal.small),
         self.opponent.name(), self.pp(gs.deal.small if pov_seat == 1 else gs.deal.big),
         self.pp(gs.deal.join_board())))

    print("\t%s %s %d dollars" % (self.pov.name(), ('won' if util >= 0 else 'lost'), abs(util)))
    return util


def main():
  rules = Leduc()
  setup = Setup(small_blind=1, big_blind=2, stack_size=5)
  pov = AllInExceptQueens(rules, setup)
  opponent = ESMCCFRPlusTraining(rules, setup).train(2500)

  contest = Contest(rules=rules, setup=setup, pov=pov, opponent=opponent)

  games = 0
  total = 0
  for _ in range(10000):
      total += contest.play()
      games += 1
      print("%s Total: (%.2f avg) %d / %d games" % (pov.name(), (1.0 *total) / games, total, games))

if __name__ == '__main__':
    main()