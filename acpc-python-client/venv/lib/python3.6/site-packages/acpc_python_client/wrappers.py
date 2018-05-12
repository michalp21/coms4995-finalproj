from ctypes import *

MAX_ROUNDS = 4
MAX_PLAYERS = 10
MAX_BOARD_CARDS = 7
MAX_HOLE_CARDS = 3
MAX_NUM_ACTIONS = 64
NUM_ACTION_TYPES = 3

# BettingType definition
(limitBetting, noLimitBetting) = (0, 1)

# ActionType definition
(a_fold, a_call, a_raise, a_invalid) = (0, 1, 2, NUM_ACTION_TYPES)


class ActionWrapper(Structure):
    _fields_ = [
        ('type', c_int),
        ('size', c_int32)]


class GameWrapper(Structure):
    _fields_ = [
        ('stack', c_int32 * MAX_PLAYERS),
        ('blind', c_int32 * MAX_PLAYERS),
        ('raiseSize', c_int32 * MAX_ROUNDS),
        ('bettingType', c_int),
        ('numPlayers', c_uint8),
        ('numRounds', c_uint8),
        ('firstPlayer', c_uint8 * MAX_ROUNDS),
        ('maxRaises', c_uint8 * MAX_ROUNDS),
        ('numSuits', c_uint8),
        ('numRanks', c_uint8),
        ('numHoleCards', c_uint8),
        ('numBoardCards', c_uint8 * MAX_ROUNDS)]


class StateWrapper(Structure):
    _fields_ = [
        ('handId', c_uint32),
        ('maxSpent', c_int32),
        ('minNoLimitRaiseTo', c_int32),
        ('spent', c_int32 * MAX_PLAYERS),
        ('action', ((ActionWrapper * MAX_NUM_ACTIONS) * MAX_ROUNDS)),
        ('actingPlayer', ((c_uint8 * MAX_NUM_ACTIONS) * MAX_ROUNDS)),
        ('numActions', c_uint8 * MAX_ROUNDS),
        ('round', c_uint8),
        ('finished', c_uint8),
        ('playerFolded', c_uint8 * MAX_PLAYERS),
        ('boardCards', c_uint8 * MAX_BOARD_CARDS),
        ('holeCards', (c_uint8 * MAX_HOLE_CARDS) * MAX_PLAYERS)]


class MatchStateWrapper(Structure):
    _fields_ = [
        ('state', StateWrapper),
        ('viewingPlayer', c_uint8)]


class PossibleActionsWrapper(Structure):
    _fields_ = [
        ('foldValid', c_bool),
        ('raiseValid', c_bool),
        ('raiseMin', c_int32),
        ('raiseMax', c_int32)]
