from acpc_python_client.data.base_data_object import BaseDataObject
from acpc_python_client.utils import action_type_int_to_enum


class State(BaseDataObject):
    """State of the game."""

    def __init__(self, wrapper, game):
        super().__init__(wrapper)
        self._game = game

    def get_max_spent(self):
        """Returns the largest bet so far, including all previous rounds.

        Returns:
            int: The largest bet so far, including all previous rounds.
        """
        return self._data_holder.maxSpent

    def get_min_no_limit_raise_to(self):
        """Returns minimum number of chips a player must have spend in total to raise.

        Only used for noLimitBetting games.

        Returns:
            int: Minimum number of chips a player must have spend in total to raise.
        """
        return self._data_holder.minNoLimitRaiseTo

    def get_spent(self, player_index):
        """Returns the total amount put into the pot by given player.

        Args:
            player_index (int): Index of the player

        Returns:
            int: The total amount put into the pot by given player.

        Raises:
            ValueError: When player_index is greater or equal
                        to number of players in the game.
        """
        if player_index >= self._game.get_num_players():
            raise ValueError(
                'Cannot retrieve spent amount for player %s with %s players total'
                % (player_index, self._game.get_num_players()))
        return self._data_holder.spent[player_index]

    def get_action_type(self, round_index, action_index):
        """Returns type of action on given index taken in given round.

        Args:
            round_index (int): Index of the round.
            action_index (int): Index of the action.

        Returns:
            ActionType: Action type for given action in given round.

        Raises:
            ValueError: When round_index is greater or equal
                        to number of rounds in the game so far.
            ValueError: When action_index is greater or equal
                        to number of actions in given round.
        """
        if round_index > self.get_round():
            raise ValueError(
                'Cannot retrieve action %s in round %s, game is in round %s'
                % (action_index, round_index, self.get_round()))
        if action_index >= self.get_num_actions(round_index):
            raise ValueError(
                'Cannot retrieve action %s in round %s, '
                'there are only %s actions in round %s'
                % (action_index, round_index, self.get_num_actions(round_index), self.get_round()))
        action_type_int = self._data_holder.action[round_index][action_index].type
        return action_type_int_to_enum(action_type_int)

    def get_action_size(self, round_index, action_index):
        """Returns size action on given index taken in given round.

        Note that the size is relevant only when corresponding action
        is ActionType.RAISE.

        Args:
            round_index (int): Index of the round.
            action_index (int): Index of the action.

        Returns:
            int: Size of given raise action in given round.

        Raises:
            ValueError: When round_index is greater or equal
                        to number of rounds in the game so far.
            ValueError: When action_index is greater or equal
                        to number of actions in given round.
        """
        if round_index > self.get_round():
            raise ValueError(
                'Cannot retrieve action %s in round %s, game is in round %s'
                % (action_index, round_index, self.get_round()))
        if action_index >= self.get_num_actions(round_index):
            raise ValueError(
                'Cannot retrieve action %s in round %s, '
                'there are only %s actions in round %s'
                % (action_index, round_index, self.get_num_actions(round_index), self.get_round()))
        return self._data_holder.action[round_index][action_index].size

    def get_acting_player(self, round_index, action_index):
        """Returns index of the acting player for given action in given round.

        Args:
            round_index (int): Index of the round.
            action_index (int): Index of the action.

        Returns:
            int: Index of the acting player for given action in given round.

        Raises:
            ValueError: When round_index is greater or equal
                        to number of rounds in the game so far.
            ValueError: When action_index is greater or equal
                        to number of actions in given round.
        """
        if round_index > self.get_round():
            raise ValueError(
                'Cannot retrieve acting player in round %s and action %s, game is in round %s'
                % (round_index, action_index, self.get_round()))
        if action_index >= self.get_num_actions(round_index):
            raise ValueError(
                'Cannot retrieve acting player in round %s and action %s, '
                'there are only %s actions in round %s'
                % (round_index, action_index, self.get_num_actions(round_index), self.get_round()))
        return self._data_holder.actingPlayer[round_index][action_index]

    def get_num_actions(self, round_index):
        """Returns number of actions in given round.

        Args:
            round_index (int): Index of the round.

        Returns:
            int: Number of actions in given round.

        Raises:
            ValueError: When round_index is greater or equal
                        to number of rounds in the game so far.
        """
        if round_index > self.get_round():
            raise ValueError(
                'Cannot retrieve number of actions in round %s, game is in round %s'
                % (round_index, self.get_round()))
        return self._data_holder.numActions[round_index]

    def get_round(self):
        """Returns index of the current round of the game.

        Returns:
            int: Index of the current round of the game.
        """
        return self._data_holder.round

    def get_player_folded(self, player_index):
        """Returns whether given player has folded.

        Args:
            player_index (int): Index of the player.

        Returns:
            bool: True if player has folded, False otherwise.

        Raises:
            ValueError: When player_index is greater or equal
                        to number of players in the game.
        """
        if player_index >= self._game.get_num_players():
            raise ValueError(
                'Cannot know if player %s folded with %s players total'
                % (player_index, self._game.get_num_players()))
        return self._data_holder.playerFolded[player_index] != 0

    def get_board_card(self, card_index):
        """Returns board card.

        Args:
            card_index (int): Index of the board card.

        Returns:
            Board card on given index.

        Raises:
            ValueError: When card_index is greater or equal
                        to number of board cards in current
                        round.
        """
        if card_index >= self._game.get_total_num_board_cards(self.get_round()):
            raise ValueError(
                'Cannot retrieve board card %s, there are only %s board cards in round %s'
                % (card_index, self._game.get_num_board_cards(self.get_round()), self.get_round()))
        return self._data_holder.boardCards[card_index]

    def get_hole_card(self, player_index, card_index):
        """Returns player's hole card

        Args:
            player_index (int): Index of the player.
            card_index (int): Index of the hole card.

        Returns:
            Hole card of given player on given index.

        Raises:
            ValueError: When card_index is greater or equal
                        to number of hole cards in the game.
        """
        if card_index >= self._game.get_num_hole_cards():
            raise ValueError(
                'Cannot retrieve hole card %s, there are only %s hole cards'
                % (card_index, self._game.get_num_hole_cards()))
        return self._data_holder.holeCards[player_index][card_index]
