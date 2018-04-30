import random
import sys
import pickle
from pprint import pprint

import acpc_python_client as acpc
from InfoSet import InfoSet
from State import State
from rules.Leduc import Leduc
from Setup import Setup
from AvailableBets import AvailableBets
from players.ESMCCFRPlusTraining import ESMCCFRPlusTraining
# from ESMCCFR import ESMCCFR_P

class Libratus(acpc.Agent):
    def __init__(self):
        super().__init__()
        self.actions = [acpc.ActionType.FOLD, acpc.ActionType.CALL, acpc.ActionType.RAISE]
        self.action_probabilities = [0] * 3
        self.action_probabilities[0] = 0.3  # fold probability
        self.action_probabilities[1] = (1 - self.action_probabilities[0]) * 0.5  # call probability
        self.action_probabilities[2] = (1 - self.action_probabilities[0]) * 0.5  # raise probability
        self.infoset_strategy_map = pickle.load(open('strategy1.pkl', 'rb'))
        self.setup = Setup(stack_size=5, big_blind=1, small_blind=1)
        # self.available_bets = AvailableBets(self.setup)
        # self.cards = set()
        self.bets = None
        self.contrib = None

        self.charizard = ESMCCFRPlusTraining(rules=Leduc(), setup=Setup(stack_size=5, big_blind=1, small_blind=1))

        self.startingplayer = 0
        self.player = None

        print("Hole / Board / Bets0 / Bets1")
        print('\n'.join(sorted([str(k) for k in self.infoset_strategy_map.keys()])))

    def _get_random_bet(self, player_strategy):
        return random.choices(list(range(len(player_strategy))),
            weights=player_strategy, k=1)[0]

    def _convert_card(self, card):
        if card in {42, 43}:
            return [1]
        elif card in {46, 47}:
            return [2]
        elif card in {50, 51}:
            return [3]
        elif card == -1:
            return []
        else:
            raise Exception('Invalid card')

    def _get_prev_ra(self,state,rround,action):
        action -= 1
        if action < 0:
            rround-=1
            action = state.get_num_actions(rround)-1
        return rround, action


    def on_game_start(self, game):
        self.player = self.startingplayer

        print("==========")

        self.bets = [[], []] #rounds
        self.contrib = [[game.get_blind(0)], [game.get_blind(1)]] #players

        self.charizard.new_game()
        self.charizard.take_seat(self.player == 0)

    def on_next_turn(self, game, match_state, is_acting_player):
        vp = match_state.get_viewing_player()
        state = match_state.get_state()
        rround = state.get_round()
        num_actions = state.get_num_actions(rround)
        hole_card = state.get_hole_card(vp, 0)
        hole_card_o = state.get_hole_card(1 - vp, 0) #meaningless
        board_card = -1

        if rround > 0:
            board_card = state.get_board_card(0)

        if rround > 0 and num_actions == 0:
            self.player = self.startingplayer

        spent = state.get_spent(1-self.player)

        # if state.get_hole_card(self.player, 0) not in self.cards:
        #     self.cards.add(state.get_hole_card(0, 0))

        print("\nP" + str(self.player) + "(" + str(vp) + ")","Round:",rround,"#Actions:",num_actions)

        #Get previous action/round
        r,a = rround,num_actions-1
        if rround > 0:
            r,a = self._get_prev_ra(state,r,a+1)
                
                # if state.get_action_type(r, a) == acpc.ActionType.RAISE:
                #     print("~pre",state.get_action_type(r, a),state.get_action_size(r, a))
                # else:
                #     print("~pre",state.get_action_type(r, a))
                
        #Keep track of total spending
        #If not first move
        prev = state.get_acting_player(r, a)
        if rround + num_actions > 0:
            self.contrib[prev].append(spent)
            if state.get_action_type(r, a) == acpc.ActionType.RAISE:
                action_player = state.get_acting_player(r, a)
                print("~pre",state.get_action_type(r, a),state.get_action_size(r, a) - self.contrib[action_player][-2])
            else:
                print("~pre",state.get_action_type(r, a))

        #Find action amounts for previous action
        if a >= 0:
            action_type = state.get_action_type(r, a)
            action_player = state.get_acting_player(r, a)
            action_amount = 0
            # print("-----")
            # print(self.contrib[action_player])
            # print("-----")
            if action_type == acpc.ActionType.RAISE:
                action_amount = state.get_action_size(r, a) - self.contrib[action_player][-2]
            elif action_type == acpc.ActionType.CALL:
                if len(self.contrib[action_player]) >= 2:
                    # print("~pre > 2")
                    caller = state.get_acting_player(r, a)
                    action_amount = self.contrib[action_player][-1] - self.contrib[action_player][-2]
                else:
                    raise Exception("What")
            self.bets[r].append(action_amount)
            # self.bets[r].append((action_type,action_amount,state.get_spent(action_player),action_player))

        # print("Stack:",game.get_stack(self.player),"Blind",game.get_blind(self.player))
        print("CONTRIB (p0): ",end="")
        pprint(self.contrib[0])
        print("CONTRIB (p1): ",end="")
        pprint(self.contrib[1])
        print("BETS (r0):    ",end="")
        pprint(self.bets[0])
        print("BETS (r1):    ",end="")
        pprint(self.bets[1])

        if is_acting_player and not state.get_player_folded(1-self.player):

            #Push cards to AvailableBets.py
            self.charizard.receive_cards(self._convert_card(hole_card))

            #If opponent played 2 rounds ago, execute opponent bet in +Training
            if a + r > 0:
                rr, aa = self._get_prev_ra(state,r,a)
                if state.get_acting_player(rr ,aa) != self.player:
                    print(" (opp_a) ",self.bets[rr][-1])
                    self.charizard.opponent_bets(self.bets[rr][-1])
                # print("    opponent bet:",self.bets[r][-1])

            #If opponent played in last round, execute opponent bet in +Training
            if a + r >= 0 and state.get_acting_player(r,a) != self.player:
                print(" (opp_b) ",self.bets[r][-1],end=" ")
                self.charizard.opponent_bets(self.bets[r][-1])

            #At beginning of round, add board cards
            if rround > 0:
                if (num_actions == 0 and self.player == 0 or \
                    num_actions == 1 and self.player == 1):
                    self.charizard.advance_round(self._convert_card(board_card))
                    # print("...r",self.charizard.state.round," l",len(self.charizard.state.deal.board))

            #Determine action_type
            debt = self.contrib[1-self.player][-1] - self.contrib[self.player][-1]
            remaining = 5 - self.contrib[self.player][-1]
            minimum_raise = self.get_raise_min()
            maximum_raise = self.get_raise_max()
            print("Min:",minimum_raise,"Max:",maximum_raise)

            #Execute self bet in +Training
            # print("^^^ Round:",self.charizard.state.round)
            bet = self.charizard.bet()

            # print("vvv Round:",self.charizard.state.round)

            action_type = None
            if debt == 0:
                action_type = self.actions[1]
            else:
                action_type = self.actions[0] if bet == 0 else self.actions[1]
            if minimum_raise != -1 and bet >= minimum_raise - self.contrib[self.player][-1]:
                action_type = self.actions[2]


            print(" | Bet:",bet,"Type:",action_type)

            # if action_type == acpc.ActionType.FOLD and not self.is_fold_valid():
            #     print("Fold :(")
            # if action_type == acpc.ActionType.RAISE and not self.is_raise_valid():
            #     print("Raise :( " + str(bet) + "contrib " + str(state.big_contrib) + " " + str(state.small_contrib))

            # print(" |", infoset)
            if action_type == acpc.ActionType.RAISE and game.get_betting_type() == acpc.BettingType.NO_LIMIT:
                self.set_next_action(action_type, bet + self.contrib[self.player][-1])
            else:
                self.set_next_action(action_type)

            

        self.player = 1 - self.player

    def on_game_finished(self, game, match_state):
        print("==========")
        # print("CONTRIB (p0): ",end="")
        # pprint(self.contrib[0])
        # print("CONTRIB (p1): ",end="")
        # pprint(self.contrib[1])
        # print("BETS (r0):    ",end="")
        # pprint(self.bets[0])
        # print("BETS (r1):    ",end="")
        # pprint(self.bets[1])
        # print(self.cards,"\n")
        print()
        
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage {game_file_path} {dealer_hostname} {dealer_port}")
        sys.exit(1)

    client = acpc.Client(sys.argv[1], sys.argv[2], sys.argv[3])
    L = Libratus()
    client.play(L)
