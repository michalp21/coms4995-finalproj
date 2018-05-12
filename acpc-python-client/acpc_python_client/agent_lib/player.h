#ifndef PLAYER_H
#define PLAYER_H

#include <inttypes.h>
#include <stdbool.h>

#include "../../acpc_infrastructure/game.h"
#include "../../acpc_infrastructure/net.h"

/*
Tells the client what actions are possible.
Call is always possible.
*/
typedef struct
{
    bool foldValid;
    bool raiseValid;
    int32_t raiseMin, raiseMax;
} PossibleActions;

Game readGameFile(char const *gameFilePath);

State parseState(char const *gameFilePath, char const *stateString);

int playGame(char const *gameFilePath,
             char *dealerHostname,
             char const *dealerPort,
             void (*initObjects)(Game *, MatchState *, PossibleActions *, Action *),
             void (*onGameStartCallback)(),
             void (*onNextTurnCallback)(bool isActingPlayer),
             void (*onGameFinishedCallback)());

#endif /* PLAYER_H */
