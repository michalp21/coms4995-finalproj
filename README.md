# coms4995-finalproj

Final Project for COMS4995.

Our goal was to replicate Libratus from a 2017 article published in Science titled *Superhuman AI for heads-up no-limit poker: Libratus beats top professionals*, and supplementary materials.

Instead of building a poker bot for a full-sized HUNL Poker game, we scaled down to a Leduc game with 105 chips in the stack and 10-chip big and small blinds. With this we could also test against a Leduc implementation of DeepStack, a rival Poker AI from 2016, on GitHub.

NOTE: This is a work in progress.

## Walkthrough

This walkthrough assumes a Unix environment and Python 3.6.

### Dealer

Poker games are conducted through a server following the [ACPC Protocol](http://www.computerpokercompetition.org/downloads/documents/protocols/protocol.pdf).  Essentially, the **dealer** acts as the server, to which two **players** connect to play a **game**. After cloning this repo, clone [DeepStack-Leduc](https://github.com/lifrordi/DeepStack-Leduc.git) which bundles together DeepStack and an ACPC server. (Alternatively, an ACPC server without DeepStack can be found [here](https://github.com/ethansbrown/acpc/tree/master/project_acpc_server)). Run `make` in the ACPC server directory. Also clone [acpc-python-client](https://github.com/JakubPetriska/acpc-python-client), a python-wrapper for the client, and run `python setup.py install`.

First we must run the dealer. Use appropriate parameters. Run just `./dealer` to see full usage.

```
./dealer <matchName> <gameDefFile> <#Hands> <rngSeed> <p1name> <p2name> -p 20000,20001
```
The dealer will wait until two players connect.

Note: The dealer and the two players must be playing the same game, as defined in the gameDefFile (and for Libratus, in various additional files). When connecting players, ensure that they agree on the game definition.

### Libratus

To play Libratus, first see the following files:
- coms4995-finalproj/ESMCCFR-LEDUC/Libratus.py - In the constructor, set the parameters for the game in self.state_controller in the constructor (stack size, blinds, blueprint file). These must match the parameters in the gameDef file.
- DeepStack-Leduc/ACPCServer/leduc.game - (gameDef) Set the parameters according to the ACPC Game Definitions. A summary of each parameter can be found in the "ACPC Game Definitions" section below.
- strategy-leduc-105-10-10.csv - This file is the blueprint: a map of infosets to strategy objects. The current game must use the same gameDef as the one the blueprint was trained on. Information on generating a new blueprint can be found in the "Training Libratus" section below.

(TODO: config file)

To connect Libratus to the ACPC server as a player, navigate to coms4995-finalproj/ESMCCFR-LEDUC and run the following command in a separate process. Replace parameters as appropriate.

```
python libratus.py <gameDefFile> localhost 20001
```

### DeepStack

To play DeepStack, see the prerequisites section of their GitHub. In summary, install [Lua](https://www.lua.org/), [Torch](http://torch.ch/), and [luasocket](http://w3.impa.br/~diego/software/luasocket/). 

All parameters, including the game definition can be set in DeepStack-Leduc/Source/Settings/arguments.lua. Be sure we are connecting to localhost on port 20000.

To connect DeepStack to the ACPC server as a player, navigate to DeepStack-Leduc/Source and run the following command in a separate process:

```
th Player/deepstack.lua
```

### Random Players and Other Bots

We can also connect other bots to the dealer. We provide the following ACPC-compatible bots:
- allin_net.py - Always raises/calls to the maximum amount possible.
- example_player.c - Selects a random valid action.

We implemented allin_net.py, while example_player.c came with the ACPC server bundled with DeepStack.

Run either `python allin_net.py <gameDefFile> <server> <port>` or `./example_player <gameDefFile> <server> <port>`.

### Output and Statistics

Each player and the dealer has its own output. The dealer follows the format specified in the ACPC protocol specification. Libratus prints out the infoset, the corresponding strategy, and the available betting actions. DeepStack prints the game state and strategy.

Since the dealer output contains information on both players, we provide a script to generate simple match statistics from the output in GameStatistics.py. Run like so:
```
python GameStatistics.py <dealer_output_file>
```
Output from several test runs on Leduc with a stack of 105 and blinds of 10 chips can be shown in dealer_output directory, as well as a chart containing parsed game statistics from the same runs.

## Training Libratus

A large portion of Libratus is trained offline, using an algorithm called External Sampling Monte Carlo Counterfactual Regret Minimization (ESMCCFR) with regret pruning. To run your own ESMCCFR, navigate to coms4995-finalproj/ESMCCFR-LEDUC and run `python ESMCCFR.py`. Parameters such as iterations, game definitions, output file, etc can all be found in the file (TODO: options).

The outputted strategy will be loaded and used when Libratus plays against another player.

## Training DeepStack

A more detailed runthrough of model training for DeepStack can be found on the Tutorial found on their website. First edit Source/Settings/arguments.lua and edit the parameters as appropriate. We define game definition, # cfr iterations, data and model paths, neural network architecture, and more all in this file.

The process boils down to the following commands:

```
th DataGeneration/main_data_generation.lua
th Training/main_train.lua
th Tree/Tests/test_tree_strategy_filling.lua
```

First random game data is generated. The model trains using these data in the second command. Finally, we can calculate the exploitability with the third command.

After training, once `params.value_net_name` is set in arguments.lua, the model will be used when DeepStack is run as a player.

## ACPC Game Definitions 

(Taken from the ACPC repo).

The dealer takes game definition files to determine which game of poker it
plays.  Please see the included game definitions for some examples.  The code
for handling game definitions is found in game.c and game.h.

Game definitions can have the following fields (case is ignored):

- **gamedef** - the starting tag for a game definition 
- **end gamedef** - ending tag for a game definition
- **stack** - the stack size for each player at the start of each hand (for no-limit)
- **blind** - the size of the blinds for each player (relative to the dealer)
- **raisesize** - the size of raises on each round (for limit games)
- **limit** - specifies a limit game
- **nolimit** - specifies a no-limit game
- **numplayers** - number of players in the game
- **numrounds** - number of betting rounds per hand of the game
- **firstplayer** - the player that acts first (relative to the dealer) on each round
- **maxraises** - the maximum number of raises on each round
- **numsuits** - the number of different suits in the deck
- **numranks** - the number of different ranks in the deck
- **numholecards** - the number of private cards to deal to each player
- **numboardcards** - the number of cards revealed on each round

## Further credit/attributions

We would like to thank the research teams behind DeepStack and Libratus for their excellent and groundbreaking research, as well as their thorough documentation. Also for lack of a better place to put this, we used [Deuces](https://github.com/worldveil/deuces) for hand evaluation.
