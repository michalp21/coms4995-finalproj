import random
import sys

import acpc_python_client as acpc
from rules.Leduc import Leduc
from rules.Kuhn import Kuhn
from Setup import Setup
from players.ESMCCFRPlusTraining import ESMCCFRPlusTraining

class Libratus(acpc.Agent):
    def __init__(self):
        super().__init__()
        self.actions = [acpc.ActionType.FOLD, acpc.ActionType.CALL, acpc.ActionType.RAISE]
        self.action_probabilities = [0] * 3
        self.action_probabilities[0] = 0.3  # fold probability
        self.action_probabilities[1] = (1 - self.action_probabilities[0]) * 0.5  # call probability
        self.action_probabilities[2] = (1 - self.action_probabilities[0]) * 0.5  # raise probability

        self.bets = None
        self.contrib = None

        self.state_controller = ESMCCFRPlusTraining(rules=Leduc(),
            setup=Setup(stack_size=10, big_blind=1, small_blind=1),
            blueprint='strategy-leduc-10-1-1.csv', abstracting=False)

        self.startingplayer = 0
        self.player = None

        # print("Hole : [Board] : [Bets r0] , [Bets r1]")
        # print('\n'.join(sorted([str(k) for k in self.state_controller.strategy_map.keys()])))

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

    def _print_betscontribs(self):
        #Display contribs
        print("CONTRIB (p0): ",end="")
        print(self.contrib[0])
        print("CONTRIB (p1): ",end="")
        print(self.contrib[1])
        print("BETS (r0):    ",end="")
        print(self.bets[0])
        print("BETS (r1):    ",end="")
        print(self.bets[1])

    def _get_prev_ra(self,state,rround,action):
        action -= 1
        if action < 0:
            rround-=1
            action = state.get_num_actions(rround)-1
        return rround, action

    def _update_prev_rounds(self,state,board_card,rround,r,a):
        if a + r >= 0:
            rr, aa = self._get_prev_ra(state,r,a)
            if aa + rr > 0 and rr < r:
                if state.get_acting_player(rr, aa) == self.player:
                    self.state_controller.advance_round(self._convert_card(board_card))
                    self.state_controller.opponent_bets(self.bets[r][-1])

                if state.get_acting_player(rr, aa) != self.player:
                    self.state_controller.opponent_bets(self.bets[rr][-1])
                    self.state_controller.advance_round(self._convert_card(board_card))
                    self.state_controller.opponent_bets(self.bets[r][-1])

            elif r < rround:
                if state.get_acting_player(r, a) != self.player:
                    self.state_controller.opponent_bets(self.bets[r][-1])
                    self.state_controller.advance_round(self._convert_card(board_card))

                elif state.get_acting_player(r, a) == self.player:
                    self.state_controller.advance_round(self._convert_card(board_card))

            else:
                self.state_controller.opponent_bets(self.bets[r][-1])

    def _get_action_type(self, game, bet):
        debt = self.contrib[1-self.player][-1] - self.contrib[self.player][-1]
        remaining = game.get_stack(self.player) - self.contrib[self.player][-1]
        minimum_raise = self.get_raise_min()
        maximum_raise = self.get_raise_max()

        #Determine action type for server
        action_type = None
        if debt == 0:
            action_type = self.actions[1]
        else:
            action_type = self.actions[0] if bet == 0 else self.actions[1]
        if minimum_raise != -1 and bet >= minimum_raise - self.contrib[self.player][-1]:
            action_type = self.actions[2]

        return action_type

    def on_game_start(self, game):
        self.player = self.startingplayer

        print("==========")

        self.bets = [[], []] #rounds
        self.contrib = [[game.get_blind(0)], [game.get_blind(1)]] #players

        self.state_controller.new_game()
        
    def on_next_turn(self, game, match_state, is_acting_player):
        vp = match_state.get_viewing_player()
        state = match_state.get_state()
        rround = state.get_round()
        num_actions = state.get_num_actions(rround)
        hole_card = state.get_hole_card(vp, 0)
        board_card = -1

        if rround + num_actions == 0:
            self.state_controller.take_seat(not vp)

        if rround > 0:
            board_card = state.get_board_card(0)

        if rround > 0 and num_actions == 0:
            self.player = self.startingplayer

        print("\nP" + str(self.player) + "(" + str(vp) + ")","Round:",rround,"#Actions:",num_actions)

        #Get previous action/round
        r,a = rround,num_actions-1
        if rround > 0:
            r,a = self._get_prev_ra(state,r,a+1)
                
        #Keep track of total spending if not first move
        prev = state.get_acting_player(r, a)
        if rround + num_actions > 0:
            spent = state.get_spent(1-self.player)
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
            if action_type == acpc.ActionType.RAISE:
                action_amount = state.get_action_size(r, a) - self.contrib[action_player][-2]
            elif action_type == acpc.ActionType.CALL:
                if len(self.contrib[action_player]) >= 2:
                    caller = state.get_acting_player(r, a)
                    action_amount = self.contrib[action_player][-1] - self.contrib[action_player][-2]
                else:
                    raise Exception("Contrib too short.")
            self.bets[r].append(action_amount)

        self._print_betscontribs()

        #Perform actions for viewing player
        if is_acting_player and not state.get_player_folded(1-self.player):

            #Push cards to AvailableBets.py
            self.state_controller.receive_cards(self._convert_card(hole_card))

            #Update opponent actions for previous rounds and increment rounds if necessary
            self._update_prev_rounds(state,board_card,rround,r,a)

            #Execute self bet in +Training
            bet = self.state_controller.bet()

            #Determine action type
            action_type = self._get_action_type(game, bet)

            print("  Bet:",bet,"Type:",action_type)

            #Set action (+amount) for server
            if action_type == acpc.ActionType.RAISE and game.get_betting_type() == acpc.BettingType.NO_LIMIT:
                self.set_next_action(action_type, bet + self.contrib[self.player][-1])
            else:
                self.set_next_action(action_type)

        self.player = 1 - self.player

    def on_game_finished(self, game, match_state):
        print("==========")
        print()
        
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage {game_file_path} {dealer_hostname} {dealer_port}")
        sys.exit(1)

    client = acpc.Client(sys.argv[1], sys.argv[2], sys.argv[3])
    L = Libratus()
    client.play(L)
