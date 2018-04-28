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
        self.available_bets = AvailableBets(self.setup)
        # self.cards = set()
        self.bets = None
        self.contrib = None

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

    def on_game_start(self, game):
        self.player = self.startingplayer

        print("==========")

        self.bets = [[], []] #rounds
        self.contrib = [[game.get_blind(0)], [game.get_blind(1)]] #players

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
            if a < 0: r-=1; a=state.get_num_actions(r)-1;

        #Keep track of total spending
        #If not first move
        prev = state.get_acting_player(r, a)
        if rround + num_actions > 0:
            self.contrib[prev].append(spent)
            if state.get_action_type(r, a) == acpc.ActionType.RAISE:
                print("~pre",state.get_action_type(r, a),state.get_action_size(r, a))
            else:
                print("~pre",state.get_action_type(r, a))

        #Find action amounts for previous action
        if a >= 0:
            action_type = state.get_action_type(r, a)
            action_player = state.get_acting_player(r, a)
            action_amount = 0
            if action_type == acpc.ActionType.RAISE:
                action_amount = state.get_action_size(r, a)
            elif action_type == acpc.ActionType.CALL:
                if a < 1:
                    # print("==0")
                    action_amount = 0
                elif a < 2:
                    # print("==1")
                    action_amount = self.contrib[action_player][-1]
                else:
                    # print(">=2")
                    caller = state.get_acting_player(r, a)
                    action_amount = self.contrib[action_player][-1] - self.contrib[action_player][-2]
            self.bets[r].append(action_amount)
            # self.bets[r].append((action_type,action_amount,state.get_spent(action_player),action_player))

        print("~pre",state.get_action_type(r, a))
        print("Stack:",game.get_stack(self.player),"Blind",game.get_blind(self.player))
        print("CONTRIB (p0): ",end="")
        pprint(self.contrib[0])
        print("CONTRIB (p1): ",end="")
        pprint(self.contrib[1])
        print("BETS (r0):    ",end="")
        pprint(self.bets[0])
        print("BETS (r1):    ",end="")
        pprint(self.bets[1])

        if is_acting_player and not state.get_player_folded(1-self.player):
            #Build InfoSet
            hole_card = self._convert_card(hole_card)
            board_card = [self._convert_card(board_card)]
            board_card = [] if board_card == [[]] else board_card
            # infoset = InfoSet(hole_card, board_card, self.bets)
            infoset = tuple() #uncomment to go to else

            #fix deal
            state = State(Leduc(), self.setup, Leduc().deal())
            state.round = rround
            state.player_turn = 2 if vp == 0 else 1
            state.folded_player = 0
            state.big_contrib = self.contrib[1][-1]
            state.small_contrib = self.contrib[0][-1]
            state.bets = self.bets

            infoset = state.get_infoset(vp)

            strategy = None
            if infoset not in self.infoset_strategy_map:
                print(infoset)
                assert(infoset in self.infoset_strategy_map)
            if infoset in self.infoset_strategy_map:
                strategy = self.infoset_strategy_map[infoset]
                assert(strategy)
                pov = state._my_contrib(state.get_players_turn())
                oppo = state._other_contrib(state.get_players_turn())
                bet = self._get_random_bet(strategy.get_average_strategy())
                bet = self.available_bets.get_bets_as_numbers(pov, oppo)
                print(" |",self.available_bets.get_bets_by_action_type(pov, oppo))
                d = self.available_bets.get_word(
                    self.available_bets.get_bets_by_action_type(pov, oppo), bet)
                action_type = None

                action_type = {
                    'fold': self.actions[0],
                    'check': self.actions[1],
                    'call': self.actions[1],
                    'raises': self.actions[2],
                    'allIn': self.actions[2]
                }[d]
                
                print(" | Bet:",bet,"Type:",action_type)


                if action_type == acpc.ActionType.FOLD and not self.is_fold_valid():
                    print("Fold :(")
                if action_type == acpc.ActionType.RAISE and not self.is_raise_valid():
                    print("Raise :( " + str(bet) + "contrib " + str(state.big_contrib) + " " + str(state.small_contrib))

                print(" |", infoset)
                if action_type == acpc.ActionType.RAISE and game.get_betting_type() == acpc.BettingType.NO_LIMIT:
                    self.set_next_action(action_type, bet)
                else:
                    self.set_next_action(action_type)
            else:
                # print("This strategy has never seen the following infoset before, and will therefore play randomly")
                print(infoset)

                # Create current action probabilities, leave out invalid actions
                strategy = [0] * 3
                if self.is_fold_valid():
                    strategy[0] = self.action_probabilities[0]
                # call is always valid action
                strategy[1] = self.action_probabilities[1]
                if self.is_raise_valid():
                    strategy[2] = self.action_probabilities[2]

                # Normalize the probabilities
                probabilities_sum = sum(strategy)
                strategy = [p / probabilities_sum for p in strategy]

                action_type = self.actions[self._get_random_bet(strategy)]
                if action_type == acpc.ActionType.RAISE \
                        and game.get_betting_type() == acpc.BettingType.NO_LIMIT:
                    raise_min = self.get_raise_min()
                    raise_max = self.get_raise_max()
                    raise_size = raise_min + (raise_max - raise_min) * random.random()
                    self.set_next_action(action_type, int(round(raise_size)))
                    print(" ", action_type, int(round(raise_size)))
                else:
                    self.set_next_action(action_type)
                    print(" ", action_type)

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
