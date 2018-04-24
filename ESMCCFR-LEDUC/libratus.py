import random
import sys

import acpc_python_client as acpc
from GameState import GameState as gs

class Libratus(acpc.Agent):
    def __init__(self):
        super().__init__()
        self.actions = [acpc.ActionType.FOLD, acpc.ActionType.CALL, acpc.ActionType.RAISE]
        self.action_probabilities = [0] * 3
        self.action_probabilities[0] = 0.3  # fold probability
        self.action_probabilities[1] = (1 - self.action_probabilities[0]) * 0.5  # call probability
        self.action_probabilities[2] = (1 - self.action_probabilities[0]) * 0.5  # raise probability
        
        self.cards = set()

        self.startingplayer = int(not gs.leduc['starting_player'])
        self.player = None

    def on_game_start(self, game):
        self.startingplayer = int(not self.startingplayer)
        self.player = self.startingplayer
        print("Self is:",self.player)

    def on_next_turn(self, game, match_state, is_acting_player):
        state = match_state.get_state()
        rround = state.get_round()
        num_actions = state.get_num_actions(rround)

        if rround > 0 and num_actions == 0:
            self.player = self.startingplayer

        if state.get_hole_card(self.player, 0) not in self.cards:
            self.cards.add(state.get_hole_card(0, 0))

        print("Round:",rround,"#Actions:",num_actions)
        print("  Self is acting:",is_acting_player)

        print("  Hole card"+str(self.player)+":",state.get_hole_card(self.player, 0))
        if rround > 0:
            print("  Board card:",state.get_board_card(0))
            if state.get_hole_card(self.player, 0) == state.get_hole_card(int(not self.player), 0) or\
                state.get_hole_card(self.player, 0) == state.get_board_card(0) or \
                state.get_board_card(0) == state.get_hole_card(int(not self.player), 0):
                print(" MEGA BAD DUDUDUDUUDUDUDDE ")

        history = {0:[], 1:[]}
        for r in range(rround+1):
            for a in range(num_actions):
                action_type = state.get_action_type(r, a)
                action_player = state.get_acting_player(r, a)
                action_amount = 0
                if action_type == acpc.ActionType.RAISE:
                    action_amount = state.get_action_size(r, a)
                history[r].append(action_type)
                
        print(history)

        # if num_actions > 0:
        #     print("  p",self.player,state.get_acting_player(rround,num_actions-1) == self.player)

        if is_acting_player:
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
                # print(action_type,int(round(raise_size)))
            else:
                self.set_next_action(action_type)
                # print(action_type)


        # for i in range(num_actions):
        #     get_acting_player(rround, i)

        self.player = int(not self.player)


    def on_game_finished(self, game, match_state):
        # state = match_state.get_state()
        # rround = state.get_round()
        # num_actions = state.get_num_actions(rround)
        # for i in range(num_actions):
        #     get_acting_player(rround, i)
        print(self.cards,"\n")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage {game_file_path} {dealer_hostname} {dealer_port}")
        sys.exit(1)

    client = acpc.Client(sys.argv[1], sys.argv[2], sys.argv[3])
    client.play(Libratus())
