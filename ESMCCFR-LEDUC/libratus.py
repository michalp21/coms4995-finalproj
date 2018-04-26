import random
import sys
import pickle
from pprint import pprint

import acpc_python_client as acpc
from InfoSet import InfoSet

class Libratus(acpc.Agent):
    def __init__(self):
        super().__init__()
        self.actions = [acpc.ActionType.FOLD, acpc.ActionType.CALL, acpc.ActionType.RAISE]
        self.action_probabilities = [0] * 3
        self.action_probabilities[0] = 0.3  # fold probability
        self.action_probabilities[1] = (1 - self.action_probabilities[0]) * 0.5  # call probability
        self.action_probabilities[2] = (1 - self.action_probabilities[0]) * 0.5  # raise probability
        # self.infoset_strategy_map = pickle.load(open('strategy.pkl', 'rb'))

        # self.cards = set()
        self.bets = None
        self.contrib = None

        self.startingplayer = 0
        self.player = None

    def on_game_start(self, game):
        self.startingplayer = 1 - self.startingplayer
        self.player = self.startingplayer
        print("Self is:",self.player)

        self.bets = [[], []] #rounds
        self.contrib = {0:[], 1:[]} #players

    def on_next_turn(self, game, match_state, is_acting_player):
        vp = match_state.get_viewing_player()
        state = match_state.get_state()
        rround = state.get_round()
        num_actions = state.get_num_actions(rround)
        hole_card = state.get_hole_card(vp, 0)
        hole_card_o = state.get_hole_card(1 - vp, 0) #meaningless
        board_card = -1

        if rround > 0 and num_actions == 0:
            self.player = self.startingplayer

        # if state.get_hole_card(self.player, 0) not in self.cards:
        #     self.cards.add(state.get_hole_card(0, 0))

        print("Round:",rround,"#Actions:",num_actions)
        print("  Self is acting:",is_acting_player)

        print(" *vp",vp)

        #Keep track of total spending
        self.contrib[self.player].append(state.get_spent(self.player))

        #Find action amounts for previous action
        r,a = rround,num_actions-1
        if rround > 0:
            if a < 0: r-=1; a=state.get_num_actions(r)-1;
        if a >= 0: 
            action_type = state.get_action_type(r, a)
            action_player = state.get_acting_player(r, a)
            action_amount = 0
            if action_type == acpc.ActionType.RAISE:
                action_amount = state.get_action_size(r, a)
            elif action_type == acpc.ActionType.CALL:
                if a < 1:
                    action_amount = 0
                else:
                    caller = state.get_acting_player(r,a)
                    action_amount = self.contrib[action_player][-1] - self.contrib[action_player][-2]
            # self.bets[r].append((action_type,action_amount,state.get_spent(action_player),action_player))
            self.bets[r].append(action_amount)

        if is_acting_player:
            # infoset = InfoSet(hole_card, board_card, self.bets)
            # if infoset in infoset_strategy_map.keys():
            #     strategy = infoset_strategy_map[infoset]
            #     print("This strategy has seen this infoset before, and will play the following actions with the following probabilities")
            #     print(possible_actions, strategy.get_average_strategy())
            # else:
            #     print("This strategy has never seen the following infoset before, and will therefore play randomly")
            #     print(infoset)
            # action = utility_methods.get_random_action(strategy.get_average_strategy())
            # print("Opponent has decided to take action", possible_actions[action])
            # gamestate.update(players_turn, possible_actions[action])

            # Create current action probabilities, leave out invalid actions
            current_probabilities = [0] * 3
            if self.is_fold_valid():
                current_probabilities[0] = self.action_probabilities[0]
            # call is always valid action
            current_probabilities[1] = self.action_probabilities[1]
            if self.is_raise_valid():
                current_probabilities[2] = self.action_probabilities[2]

            # Normalize the probabilities
            probabilities_sum = sum(current_probabilities)
            current_probabilities = [p / probabilities_sum for p in current_probabilities]

            # Randomly select one action
            action_index = -1
            r = random.random()
            for i in range(3):
                if r <= current_probabilities[i]:
                    action_index = i
                else:
                    r -= current_probabilities[i]
            action_type = self.actions[action_index]
            if action_type == acpc.ActionType.RAISE \
                    and game.get_betting_type() == acpc.BettingType.NO_LIMIT:
                raise_min = self.get_raise_min()
                raise_max = self.get_raise_max()
                raise_size = raise_min + (raise_max - raise_min) * random.random()
                self.set_next_action(action_type, int(round(raise_size)))
            else:
                self.set_next_action(action_type)

        self.player = 1 - self.player


    def on_game_finished(self, game, match_state):
        pprint(self.bets)
        print()
        # print(self.cards,"\n")
        

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage {game_file_path} {dealer_hostname} {dealer_port}")
        sys.exit(1)

    client = acpc.Client(sys.argv[1], sys.argv[2], sys.argv[3])
    L = Libratus()
    client.play(L)
    # print(L.fail/L.total)
