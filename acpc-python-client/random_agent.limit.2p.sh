#!/bin/bash

ACPC_UTILS_DIR=./acpc_infrastructure_utils
ACPC_DIR=./acpc_infrastructure

python ../example_agent.py ./holdem.limit.2p.reverse_blinds.game $1 $2
