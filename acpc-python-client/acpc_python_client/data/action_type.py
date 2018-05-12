from enum import Enum


class ActionType(Enum):
    """Represents type of action."""
    FOLD = 1,
    CALL = 2,
    RAISE = 3,
    INVALID = 4
