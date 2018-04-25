from random import shuffle
from deuces2.card import Card

class Deck:
    """
    Class representing a deck. The first time we create, we seed the static
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it.
    """
    _FULL_DECK_LEDUC = [1, 1, 2, 2, 3, 3]
    _FULL_DECK_HUNL = [Card.new(rank + suit)
        for suit, val in Card.CHAR_SUIT_TO_INT_SUIT.items()
        for rank in Card.STR_RANKS]
    _FULL_DECK_KUHN = [1, 2, 3]

    def __init__(self, deck_size):
        assert deck_size in (3, 6, 52)
        self.cards = Deck.GetFullDeck(deck_size)
        shuffle(self.cards)

    def draw(self, n=1):
        if n == 1:
            return self.cards.pop(0)

        cards = []
        for i in range(n):
            cards.append(self.draw())
        return cards

    def __str__(self):
        return Card.print_pretty_cards(self.cards)

    @staticmethod
    def GetFullDeck(deck_size):
        if deck_size == 6:
            return list(Deck._FULL_DECK_LEDUC)
        elif deck_size == 52:
            return list(Deck._FULL_DECK_HUNL)
        else:
            return list(Deck._FULL_DECK_KUHN)