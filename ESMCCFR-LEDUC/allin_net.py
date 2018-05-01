import random
import sys

import acpc_python_client as acpc
from rules.Leduc import Leduc

class AllInNet(acpc.Agent):
    def __init__(self):
        super().__init__()
        self.actions = [acpc.ActionType.FOLD, acpc.ActionType.CALL, acpc.ActionType.RAISE]

    def on_game_start(self, game):
        pass
        
    def on_next_turn(self, game, match_state, is_acting_player):
        vp = match_state.get_viewing_player()

        if is_acting_player:

            if self.is_raise_valid():
                self.set_next_action(self.actions[2], game.get_stack(vp))
            elif self.is_call_valid():
                self.set_next_action(self.actions[1])

    def on_game_finished(self, game, match_state):
        pass
        
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage {game_file_path} {dealer_hostname} {dealer_port}")
        sys.exit(1)

    client = acpc.Client(sys.argv[1], sys.argv[2], sys.argv[3])
    client.play(AllInNet())
