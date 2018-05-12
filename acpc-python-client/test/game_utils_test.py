import unittest
import acpc_python_client as acpc
from acpc_python_client.data.state import State
from acpc_python_client.data.action_type import ActionType
from acpc_python_client.wrappers import StateWrapper


class GameUtilsTest(unittest.TestCase):
    def test_read_game_file(self):
        game = acpc.read_game_file('test.game')
        self.assertEqual(game.get_num_players(), 3)
        self.assertEqual(game.get_num_rounds(), 4)

        self.assertEqual(game.get_blind(0), 5)
        self.assertEqual(game.get_blind(1), 10)
        self.assertEqual(game.get_blind(2), 0)

        self.assertEqual(game.get_num_hole_cards(), 2)

        self.assertEqual(game.get_num_board_cards(0), 0)
        self.assertEqual(game.get_num_board_cards(1), 3)
        self.assertEqual(game.get_num_board_cards(2), 1)
        self.assertEqual(game.get_num_board_cards(3), 1)

        self.assertEqual(game.get_num_ranks(), 13)
        self.assertEqual(game.get_num_suits(), 4)

    def test_parse_state(self):
        state = acpc.parse_state(
            'leduc.limit.2p.game',
            'STATE:36:rc/rrc:Ks|As/Qh:-11|11:Random_1|CFR_trained')
        self.assertEqual(state.get_num_actions(0), 2)
        self.assertEqual(state.get_num_actions(1), 3)

        self.assertEqual(state.get_acting_player(0, 0), 0)
        self.assertEqual(state.get_action_type(0, 0), ActionType.RAISE)
        self.assertEqual(state.get_acting_player(0, 1), 1)
        self.assertEqual(state.get_action_type(0, 1), ActionType.CALL)
        self.assertEqual(state.get_acting_player(1, 0), 0)
        self.assertEqual(state.get_action_type(1, 0), ActionType.RAISE)
        self.assertEqual(state.get_acting_player(1, 1), 1)
        self.assertEqual(state.get_action_type(1, 1), ActionType.RAISE)
        self.assertEqual(state.get_acting_player(1, 2), 0)
        self.assertEqual(state.get_action_type(1, 2), ActionType.CALL)

        self.assertEqual(state.get_hole_card(0, 0), 47)
        self.assertEqual(state.get_hole_card(1, 0), 51)
        self.assertEqual(state.get_board_card(0), 42)
