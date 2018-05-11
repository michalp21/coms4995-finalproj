from acpc_python_client import utils
from acpc_python_client.data.base_data_object import BaseDataObject


class Game(BaseDataObject):
    """Game definition."""

    def __init__(self, wrapper):
        super().__init__(wrapper)
        self.board_card_counts = [self.get_num_board_cards(round_index)
                                  for round_index in range(self.get_num_rounds())]
        for i in range(1, self.get_num_rounds()):
            self.board_card_counts[i] = self.board_card_counts[i - 1] + self.board_card_counts[i]

    def get_stack(self, player_index):
        """Returns stack size of player.

        Args:
            player_index (int): Index of the player

        Returns:
            int: Player's stack size.

        Raises:
            ValueError: When player_index is greater or equal
                        to number of players in the game.
        """
        if player_index >= self.get_num_players():
            raise ValueError(
                'Cannot retrieve stack for player %s with %s players total'
                % (player_index, self.get_num_players()))
        return self._data_holder.stack[player_index]

    def get_blind(self, player_index):
        """Returns player's entry fee.

        Args:
            player_index (int): Index of the player

        Returns:
            int: Player's entry fee (blind).

        Raises:
            ValueError: When player_index is greater or equal
                        to number of players in the game.
        """
        if player_index >= self.get_num_players():
            raise ValueError(
                'Cannot retrieve stack for player %s with %s players total'
                % (player_index, self.get_num_players()))
        return self._data_holder.blind[player_index]

    def get_raise_size(self, round_index):
        """Returns the size of raise for limit games in given round.

        Args:
            round_index (int): Index of the round

        Returns:
            int: Size of the raise in given round.

        Raises:
            ValueError: When round_index is greater or equal
                        to number of rounds in the game.
        """
        if round_index >= self.get_num_rounds():
            raise ValueError(
                'Cannot retrieve raise size in round %s in game with %s rounds'
                % (round_index, self.get_num_rounds()))
        return self._data_holder.raiseSize[round_index]

    def get_betting_type(self):
        """Betting type of the game, that is either limited or no-limit.

        Returns:
            BettingType: Betting type of the game.
        """
        return utils.betting_type_int_to_enum(self._data_holder.bettingType)

    def get_num_players(self):
        """Returns number of players in the game.

        Returns:
            int: Number of players in the game.
        """
        return self._data_holder.numPlayers

    def get_num_rounds(self):
        """Returns number of rounds in the game.

        Returns:
            int: Number of rounds in the game.
        """
        return self._data_holder.numRounds

    def get_first_player(self, round_index):
        """Returns first layer in given round of the game.

        Args:
            round_index (int): Index of the round

        Returns:
            int: First layer in given round of the game.

        Raises:
            ValueError: When round_index is greater or equal
                        to number of rounds in the game.
        """
        if round_index >= self.get_num_rounds():
            raise ValueError(
                'Cannot retrieve first player in round %s in game with %s rounds'
                % (round_index, self.get_num_rounds()))
        return self._data_holder.firstPlayer[round_index]

    def get_max_raises(self, round_index):
        """Returns number of bets/raises that may be made in given round.

        Args:
            round_index (int): Index of the round

        Returns:
            int: Number of bets/raises that may be made in each round.

        Raises:
            ValueError: When round_index is greater or equal
                        to number of rounds in the game.
        """
        if round_index >= self.get_num_rounds():
            raise ValueError(
                'Cannot retrieve max number of raises in round %s in game with %s rounds'
                % (round_index, self.get_num_rounds()))
        return self._data_holder.maxRaises[round_index]

    def get_num_suits(self):
        """Returns number of card suits in the game.

        Returns:
            int: Number of card suits in the game.
        """
        return self._data_holder.numSuits

    def get_num_ranks(self):
        """Returns number of card ranks in the game.

        Returns:
            int: Number of card ranks in the game.
        """
        return self._data_holder.numRanks

    def get_num_hole_cards(self):
        """Returns number of hole cards each player receives at the beginning of the game.

        Returns:
            int: Number of hole cards each player receives at the beginning of the game.
        """
        return self._data_holder.numHoleCards

    def get_num_board_cards(self, round_index):
        """Returns number of board cards that are revealed in given round.

        Args:
            round_index (int): Index of the round

        Returns:
            int: Number of board cards that are revealed in given round.

        Raises:
            ValueError: When round_index is greater or equal
                        to number of rounds in the game.
        """
        if round_index >= self.get_num_rounds():
            raise ValueError(
                'Cannot retrieve number of board cards in round %s in game with %s rounds'
                % (round_index, self.get_num_rounds()))
        return self._data_holder.numBoardCards[round_index]

    def get_total_num_board_cards(self, round_index):
        """Returns total number of board cards that are on the board in given round.

        Args:
            round_index (int): Index of the round

        Returns:
            int: Total number of board cards that are on the board in given round.

        Raises:
            ValueError: When round_index is greater or equal
                        to number of rounds in the game.
        """
        if round_index >= self.get_num_rounds():
            raise ValueError(
                'Cannot retrieve number of board cards in round %s in game with %s rounds'
                % (round_index, self.get_num_rounds()))
        return self.board_card_counts[round_index]
