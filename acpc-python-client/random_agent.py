import random
import sys

import acpc_python_client as acpc

class RandomAgent(acpc.Agent):
    def __init__(self):
        super().__init__()
        self.actions = [acpc.ActionType.FOLD, acpc.ActionType.CALL, acpc.ActionType.RAISE]
        self.action_probabilities = [0] * 3
        self.action_probabilities[0] = 0.3  # fold probability
        self.action_probabilities[1] = (1 - self.action_probabilities[0]) * 0.5  # call probability
        self.action_probabilities[2] = (1 - self.action_probabilities[0]) * 0.5  # raise probability

    def on_game_start(self, game):
        pass

    def on_next_turn(self, game, match_state, is_acting_player):
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
            else:
                self.set_next_action(action_type)

    def on_game_finished(self, game, match_state):
        pass

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage {game_file_path} {dealer_hostname} {dealer_port}")
        sys.exit(1)

    client = acpc.Client(sys.argv[1], sys.argv[2], sys.argv[3])
    client.play(RandomAgent())
