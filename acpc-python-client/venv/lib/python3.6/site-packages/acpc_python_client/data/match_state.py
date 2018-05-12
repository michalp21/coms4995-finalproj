from acpc_python_client.data.base_data_object import BaseDataObject
from acpc_python_client.data.state import State


class MatchState(BaseDataObject):
    """State of the match as perceived by agent."""

    def __init__(self, wrapper, game):
        super().__init__(wrapper)
        self._state = State(self._data_holder.state, game)

    def get_state(self):
        """State of the game.

        Returns:
            MatchState: State of the game.
        """
        return self._state

    def get_viewing_player(self):
        """Return index of the player that is viewing this state.

        Returns:
            int: Index of the player that is viewing this state.
        """
        return self._data_holder.viewingPlayer
