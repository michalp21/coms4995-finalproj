#include "test_utils.h"


void fillTestAction(Action * action) {
  action->type = a_call;
  action->size = 32;
}

void fillTestGame(Game * game) {
  for (int i = 0; i < MAX_PLAYERS; ++i) {
    game->stack[i] = 21 + i;
  }
  for (int i = 0; i < MAX_PLAYERS; ++i) {
    game->blind[i] = 89 + i;
  }
  for (int i = 0; i < MAX_ROUNDS; ++i) {
    game->raiseSize[i] = 13 + i;
  }
  game->bettingType = noLimitBetting;
  game->numPlayers = 7;
  game->numRounds = 2;
  for (int i = 0; i < MAX_ROUNDS; ++i) {
    game->firstPlayer[i] = 42 + i;
  }
  for (int i = 0; i < MAX_ROUNDS; ++i) {
    game->maxRaises[i] = 18 + i;
  }
  game->numSuits = 2;
  game->numRanks = 25;
  game->numHoleCards = 2;
  for (int i = 0; i < MAX_ROUNDS; ++i) {
    game->numBoardCards[i] = i + 1;
  }
}

enum ActionType indexToActionType(int index) {
  if (index == 0) {
    return a_fold;
  } else if (index == 1) {
    return a_call;
  } else if (index == 2) {
    return a_raise;
  } else {
    return a_invalid;
  }
}

void fillTestState(MatchState * matchState) {
  matchState->viewingPlayer = 1;
  State * state = &matchState->state;
  state->handId = 12;
  state->maxSpent = 8;
  state->minNoLimitRaiseTo = 22;
  for (int i = 0; i < MAX_PLAYERS; ++i) {
    state->spent[i] = 18 + i;
  }
  for (int i = 0; i < MAX_ROUNDS; ++i) {
    for (int j = 0; j < MAX_NUM_ACTIONS; ++j) {
      state->action[i][j].type =
        indexToActionType((i * MAX_ROUNDS + j) % NUM_ACTION_TYPES);
      state->action[i][j].size = 1 + i * MAX_ROUNDS + j;
    }
  }
  for (int i = 0; i < MAX_ROUNDS; ++i) {
    for (int j = 0; j < MAX_NUM_ACTIONS; ++j) {
      state->actingPlayer[i][j] = 3 + i * MAX_ROUNDS + j;
    }
  }
  for (int i = 0; i < MAX_ROUNDS; ++i) {
    state->numActions[i] = 7 + i;
  }
  state->round = 1;
  state->finished = 11;
  for (int i = 0; i < MAX_PLAYERS; ++i) {
    state->playerFolded[i] = 33 + i;
  }
  for (int i = 0; i < MAX_BOARD_CARDS; ++i) {
    state->boardCards[i] = 82 + i;
  }
  for (int i = 0; i < MAX_PLAYERS; ++i) {
    for (int j = 0; j < MAX_HOLE_CARDS; ++j) {
      state->holeCards[i][j] = 2 + i * MAX_PLAYERS + j;
    }
  }
}

void fillTestMatchState(MatchState * matchState) {
  matchState->state.handId = 3;
  matchState->state.round = 4;
  matchState->viewingPlayer = 5;
}

void fillTestPossibleActions1(PossibleActions * possibleActions) {
  possibleActions->foldValid = true;
  possibleActions->raiseValid = true;
  possibleActions->raiseMin = 5;
  possibleActions->raiseMax = 8;
}

void fillTestPossibleActions2(PossibleActions * possibleActions) {
  possibleActions->foldValid = false;
  possibleActions->raiseValid = true;
  possibleActions->raiseMin = 34;
  possibleActions->raiseMax = -6;
}

void fillTestPossibleActions3(PossibleActions * possibleActions) {
  possibleActions->foldValid = true;
  possibleActions->raiseValid = false;
  possibleActions->raiseMin = -154;
  possibleActions->raiseMax = 1;
}
