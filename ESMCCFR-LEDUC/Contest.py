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
from State import State
from AvailableBets import AvailableBets

class Contest:

  def __init__(self, rules, setup, logger, players):
    self.rules = rules
    self.setup = setup
    self.logger = logger
    self.pov = players[0]
    self.opponent = players[1]
    self.available_bets = AvailableBets(setup)

  def play(self):
    self.pov.new_game()
    self.opponent.new_game()

    pov_seat = random.choice([1, 2])
    opponent_seat = 3 - pov_seat
    self.pov.take_seat(pov_seat == 2)
    self.opponent.take_seat(opponent_seat == 2)

    deal = self.rules.deal()
    if pov_seat == 2:
      self.pov.receive_cards(deal.small)
      self.opponent.receive_cards(deal.big)
    else:
      self.pov.receive_cards(deal.big)
      self.opponent.receive_cards(deal.small)

    round = 0
    gs= State(rules=self.rules, setup=self.setup, deal=deal)

    self.logger.round(gs, pov_seat)

    while not gs.is_terminal():
      turn = gs.get_players_turn()
      player = self.pov if turn == pov_seat else self.opponent
      other = self.opponent if turn == pov_seat else self.pov

      bet = player.bet(self.available_bets.get_bets_by_action_type(gs._my_contrib(turn), gs._other_contrib(turn)),
                       self.available_bets.get_bets_as_numbers(gs._my_contrib(turn), gs._other_contrib(turn)))
      other.opponent_bets(bet)

      gs.update(bet)
      self.logger.bet(gs, player, pov_seat, bet)

      if (not gs.is_terminal()) and gs.round > round:
        # print round and new cards
        self.pov.advance_round(deal.board[round])
        self.opponent.advance_round(deal.board[round])
        self.logger.round(gs, pov_seat)
        round = gs.round

    # after end
    util = gs.get_utility(pov_seat)
    self.logger.evaluate(gs, pov_seat)
    self.logger.earnings(util)
    return util

def main():
  rules = Leduc()
  setup = Setup(small_blind=1, big_blind=1, stack_size=10)
  pov = Human(rules, setup)
  opponent = ESMCCFRPlusTraining(rules, setup, 'strategy-leduc-10-1-1.csv')

  contest = Contest(rules=rules,
    setup=setup,
    logger=Logger(rules=rules, setup=setup, players=(pov, opponent)),
    players=(pov, opponent))

  games = 0
  total = 0
  for _ in range(100):
      total += contest.play()
      games += 1
      print("@%d %s Total: (%.2f avg) %d" % (
        games, pov, (1.0 *total) / games, total))

if __name__ == '__main__':
    main()