import random
from Logger import Logger
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

class Contest:

  def __init__(self, rules, setup, logger, players):
    self.rules = rules
    self.setup = setup
    self.logger = logger
    self.pov = players[0]
    self.opponent = players[1]

  def play(self):
    pov_seat = random.choice([1, 2])
    opponent_seat = 3 - pov_seat

    round = 0
    gs= State(rules=self.rules, setup=self.setup, deal=self.rules.deal())

    self.logger.round(gs, pov_seat)

    while not gs.is_terminal():
      turn = gs.get_players_turn()
      player = self.pov if turn == pov_seat else self.opponent
      bet = player.bet(gs)
      gs.update(bet)
      self.logger.bet(gs, player, pov_seat, bet)

      if gs.round > round and gs.round < len(gs.deal.board):
        # print round and new cards
        self.logger.round(gs, pov_seat)
        round = gs.round

    # after end
    util = gs.get_utility(pov_seat)
    self.logger.evaluate(gs, pov_seat)
    self.logger.earnings(util)
    return util

def main():
  rules = Leduc()
  setup = Setup(small_blind=1, big_blind=2, stack_size=5)
  pov = AllInExceptQueens(rules, setup)
  opponent = ESMCCFRPlusTraining(rules, setup).train(2500)

  contest = Contest(rules=rules,
    setup=setup,
    logger=Logger(rules=rules, setup=setup, players=(pov, opponent)),
    players=(pov, opponent))

  games = 0
  total = 0
  for _ in range(10000):
      total += contest.play()
      games += 1
      print("@%d %s Total: (%.2f avg) %d" % (
        games, pov, (1.0 *total) / games, total))

if __name__ == '__main__':
    main()