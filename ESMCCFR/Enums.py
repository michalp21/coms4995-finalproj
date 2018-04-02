from enum import Enum

class Action(Enum):
	FOLD = 1
	CHECK = 2
	CALL = 3
	BET = 4
	RAISE = 5
	NEWCARD = 6
	NEW3CARDS = 7

class Suit(Enum):
	CLUBS = 1
	DIAMONDS = 2
	HEARTS = 3
	SPADES = 4