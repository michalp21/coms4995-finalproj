import abc
import ctypes as ctypes

import acpc_python_client.agent_lib as lib
import acpc_python_client.wrappers as wrappers
from acpc_python_client import utils
from acpc_python_client.data.action_type import ActionType
from acpc_python_client.data.game import Game
from acpc_python_client.data.match_state import MatchState


class Agent(object):
    """Base class for the agent.

    Implement all abstract methods in this class to create your poker agent.
    Pass instance of your implemented agent to Client to play.
    """

    def __init__(self):
        super().__init__()
        self._client = None
        self._possible_actions_wrapper = None

    def _setup(self, client, possible_actions_wrapper):
        self._client = client
        self._possible_actions_wrapper = possible_actions_wrapper

    def is_fold_valid(self):
        """Returns if fold is a valid action in current round.
        Returns:
            bool: True if fold is valid, False otherwise.
        """
        return self._possible_actions_wrapper.contents.foldValid

    def is_call_valid(self):
        """Returns if call is a valid action in current round.
        Returns:
            bool: True if call is valid, False otherwise.
        """
        return True

    def is_raise_valid(self):
        """Returns if raise is a valid action in current round.
        Returns:
            bool: True if raise is valid, False otherwise.
        """
        return self._possible_actions_wrapper.contents.raiseValid

    def get_raise_max(self):
        """Returns maximal valid raise size.
        Returns:
            int: Maximal valid raise size if raise is valid or -1 otherwise.
        """
        return self._possible_actions_wrapper.contents.raiseMax if self.is_raise_valid() else -1

    def get_raise_min(self):
        """Returns minimal valid raise size.
        Returns:
            int: Minimal valid raise size if raise is valid or -1 otherwise.
        """
        return self._possible_actions_wrapper.contents.raiseMin if self.is_raise_valid() else -1

    def set_next_action(self, action_type, raise_size=0):
        """Set next agent's action.

        Call this in on_next_round only when is_acting_player is set to True.

        Args:
            action_type (client.data.ActionType): Type of the action.
            raise_size (int): Size of raise. Only used when action type is raise.
        """
        self._client._set_next_action(action_type, raise_size)

    @abc.abstractmethod
    def on_game_start(self, game):
        """Called before start of each game.

        Note that one agent instance may be used to play multiple games.
        This method will be called before each game that agent plays.

        Args:
            game (client.data.Game): Definition of the game. Definition is the same
                                     for all games that one agent instance plays.
        """
        pass

    @abc.abstractmethod
    def on_next_turn(self, game, match_state, is_acting_player):
        """Called on each player's turn.

        This is called even on turns of other players when the agent is not acting.

        If is_acting_player is set to True the agent must call set_next_action method.

        Args:
            game (client.data.Game): Definition of the game.
            match_state (client.data.MatchState): Current state of the game.
            is_acting_player (bool): True if player is acting, False otherwise.
        """
        pass

    @abc.abstractmethod
    def on_game_finished(self, game, match_state):
        """Called when game is finished.

        Args:
            game (client.data.Game): Definition of the game.
            match_state (client.data.MatchState): Final state of the game.
        """
        pass


class Client(object):
    """Client that handles the game.

    Contains all logic needed to play the game, such as connection to dealer server.
    """

    def __init__(self, game_file_path, dealer_hostname, dealer_port):
        """Initializes the Client.

        Args:
            game_file_path (str): Path to game definition file.
            dealer_hostname (str): Hostname of dealer server.
            dealer_port (str): Port that dealer server accepts the connection on.
        """
        super().__init__()
        self._game_file_path = game_file_path
        self._dealer_hostname = dealer_hostname
        self._dealer_port = dealer_port

        self._agent = None

        self._action_wrapper = None

        # Data object references
        self._game = None
        self._match_state = None

        self._action_set = False

    def play(self, agent):
        """Begin playing games.

        Args:
            agent (Agent): Agent instance.
        """
        if not agent:
            raise ValueError('No agent provided to Client')
        self._agent = agent

        init_objects_func = ctypes.CFUNCTYPE(None, ctypes.POINTER(wrappers.GameWrapper),
                                             ctypes.POINTER(wrappers.MatchStateWrapper),
                                             ctypes.POINTER(wrappers.PossibleActionsWrapper),
                                             ctypes.POINTER(wrappers.ActionWrapper))(self._init_objects)
        on_game_start_func = ctypes.CFUNCTYPE(None)(self._on_game_start)
        on_next_round_func = ctypes.CFUNCTYPE(None, ctypes.c_bool)(self._on_next_round)
        on_game_finished_func = ctypes.CFUNCTYPE(None)(self._on_game_finished)
        lib.player.playGame(bytes(self._game_file_path, 'utf-8'),
                            bytes(self._dealer_hostname, 'utf-8'),
                            bytes(self._dealer_port, 'utf-8'),
                            init_objects_func, on_game_start_func, on_next_round_func, on_game_finished_func)

    def _set_next_action(self, action_type, raise_size):
        self._action_wrapper.contents.type = utils.action_type_enum_to_int(action_type)
        if action_type == ActionType.RAISE:
            self._action_wrapper.contents.size = raise_size
        else:
            self._action_wrapper.contents.size = 0
        self._action_set = True

    def _init_objects(self, game_wrapper, match_state_wrapper,
                      possible_actions_wrapper, action_wrapper):
        self._action_wrapper = action_wrapper
        self._game = Game(game_wrapper)
        self._match_state = MatchState(match_state_wrapper, self._game)
        self._agent._setup(self, possible_actions_wrapper)

    def _on_game_start(self):
        self._agent.on_game_start(self._game)

    def _on_next_round(self, is_acting_player):
        self._action_set = False
        self._agent.on_next_turn(self._game, self._match_state, is_acting_player)
        if is_acting_player and not self._action_set:
            raise RuntimeError('No action was set by agent when it was acting')

    def _on_game_finished(self):
        self._agent.on_game_finished(self._game, None)
