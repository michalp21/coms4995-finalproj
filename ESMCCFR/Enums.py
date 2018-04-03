from enum import Enum

class Action(Enum):
	FOLD = 0
	CHECK = 1
	CALL = 2
	BET = 3
	RAISE = 4
	NEWCARD = 5
	NEW3CARDS = 6

class Suit(Enum):
	CLUBS = 1
	DIAMONDS = 2
	HEARTS = 3
	SPADES = 4