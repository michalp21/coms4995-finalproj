#!/bin/bash

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

cd ${SCRIPT_DIR}/acpc_infrastructure
make

cd ${SCRIPT_DIR}/acpc_python_client/agent_lib
make

cd ${SCRIPT_DIR}/test/agent_lib_test_utils
make
