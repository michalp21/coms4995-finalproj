# ACPC python client

Python wrapper for [AAAI ACPC][1] poker bot infrastructure. The infrastructure
consists of server, acting as a dealer and clients acting as poker players.
The wrapper is built around original client C code from [ACPC][1].


## ACPC infrastrucure
The complete ACPC poker bot infrastructure is contained in `acpc_infractructure`
directory. All necessary documentation and examples of how the infrastructure
works are contained there. Before trying the wrapper, I strongly recommend taking
the time to grasp how the infrastructure works.


## Prerequisites 
Library was built using Python 3.6. Additionally `gcc` and `make` are needed to
build the native parts. 


## Installation
To use the package clone this repository. After cloning navigate to the root of
the repository and call
```bash
python setup.py install
```

This will install package `acpc_python_client` into your python distribution.


## Sample code
The `random_agent.py` in the root of this repository contains simple random
agent written using the wrapper which can be used for any poker game
supported by ACPC infrastructure. The accompanying file `random_agent.limit.2.sh`
is an example of agent launching script for Heads-Up Limit Hold'em which is passed
to dealer. 


## Agent testing
To test your agent you can either use `play_match.pl` which is documented
in `acpc_infractructure/README`.

If you want to launch the agent yourself you can use `start_dealer_and_player_1.sh`
in `scripts` directory. By executing the script, dealer is launched and 1 random
agent joins the game. Dealer prints out port number for second agent at which your
agent can join. The script is just slightly edited version of `play_match.pl` from
`acpc_infrastructure` directory.


[1]: http://www.computerpokercompetition.org/