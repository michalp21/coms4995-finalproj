#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <getopt.h>

#include "player.h"

Game readGameFile(char const *gameFilePath) {
  Game *game;
  FILE *file;

  file = fopen(gameFilePath, "r");
  if (file == NULL)
  {

    fprintf(stderr, "ERROR: could not open game %s\n", gameFilePath);
    exit(EXIT_FAILURE);
  }
  game = readGame(file);
  if (game == NULL)
  {

    fprintf(stderr, "ERROR: could not read game %s\n", gameFilePath);
    exit(EXIT_FAILURE);
  }
  fclose(file);

  return *game;
}

State parseState(char const *gameFilePath, const char *stateString) {
  Game game = readGameFile(gameFilePath);
  State state;
  readState(stateString, &game, &state);
  return state;
}

int playGame(char const *gameFilePath, char *dealerHostname,
             char const *dealerPort,
             void (*initObjects)(Game *, MatchState *, PossibleActions *, Action *),
             void (*onGameStartCallback)(),
             void (*onNextTurnCallback)(bool isActingPlayer),
             void (*onGameFinishedCallback)())
{
  int sock, len, r;
  uint16_t port;
  Game *game;
  MatchState state;
  Action action;
  PossibleActions possibleActions;
  FILE *file, *toServer, *fromServer;
  char line[MAX_LINE_LEN];

  /* we make some assumptions about the actions - check them here */
  assert(NUM_ACTION_TYPES == 3);

  /* get the game */
  file = fopen(gameFilePath, "r");
  if (file == NULL)
  {

    fprintf(stderr, "ERROR: could not open game %s\n", gameFilePath);
    exit(EXIT_FAILURE);
  }
  game = readGame(file);
  if (game == NULL)
  {

    fprintf(stderr, "ERROR: could not read game %s\n", gameFilePath);
    exit(EXIT_FAILURE);
  }
  fclose(file);

  initObjects(game, &state, &possibleActions, &action);

  /* connect to the dealer */
  if (sscanf(dealerPort, "%" SCNu16, &port) < 1)
  {

    fprintf(stderr, "ERROR: invalid port %s\n", dealerPort);
    exit(EXIT_FAILURE);
  }
  sock = connectTo(dealerHostname, port);
  if (sock < 0)
  {

    exit(EXIT_FAILURE);
  }
  toServer = fdopen(sock, "w");
  fromServer = fdopen(sock, "r");
  if (toServer == NULL || fromServer == NULL)
  {

    fprintf(stderr, "ERROR: could not get socket streams\n");
    exit(EXIT_FAILURE);
  }

  /* send version string to dealer */
  if (fprintf(toServer, "VERSION:%" PRIu32 ".%" PRIu32 ".%" PRIu32 "\n",
              VERSION_MAJOR, VERSION_MINOR, VERSION_REVISION) != 14)
  {

    fprintf(stderr, "ERROR: could not get send version to server\n");
    exit(EXIT_FAILURE);
  }
  fflush(toServer);

  bool gameFinished = true;

  /* play the game! */
  while (fgets(line, MAX_LINE_LEN, fromServer))
  {

    /* ignore comments */
    if (line[0] == '#' || line[0] == ';')
    {
      continue;
    }

    len = readMatchState(line, game, &state);
    if (len < 0)
    {

      fprintf(stderr, "ERROR: could not read state %s", line);
      exit(EXIT_FAILURE);
    }

    if (stateFinished(&state.state))
    {
      onGameFinishedCallback();
      gameFinished = true;
      continue;
    }

    if (gameFinished)
    {
      onGameStartCallback();
      gameFinished = false;
    }

    if (currentPlayer(game, &state.state) != state.viewingPlayer)
    {
      onNextTurnCallback(false);
      /* no action is required by server */
      continue;
    }

    /* add a colon (guaranteed to fit because we read a new-line in fgets) */
    line[len] = ':';
    ++len;

    /* check if fold is valid */
    action.type = a_fold;
    action.size = 0;
    possibleActions.foldValid = isValidAction(game, &state.state, 0, &action);

    /* check if raise is valid and by how much */
    possibleActions.raiseValid = raiseIsValid(game, &state.state,
                                              &(possibleActions.raiseMin), &(possibleActions.raiseMax));

    /* call the python callback, it will set the action to the chose action */
    onNextTurnCallback(true);

    /* do the action! */
    assert(isValidAction(game, &state.state, 0, &action));
    r = printAction(game, &action, MAX_LINE_LEN - len - 2,
                    &line[len]);
    if (r < 0)
    {

      fprintf(stderr, "ERROR: line too long after printing action\n");
      exit(EXIT_FAILURE);
    }
    len += r;
    line[len] = '\r';
    ++len;
    line[len] = '\n';
    ++len;

    if (fwrite(line, 1, len, toServer) != len)
    {

      fprintf(stderr, "ERROR: could not get send response to server\n");
      exit(EXIT_FAILURE);
    }
    fflush(toServer);
  }

  return EXIT_SUCCESS;
}
