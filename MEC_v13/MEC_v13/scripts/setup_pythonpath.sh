#!/bin/bash

# Setup PYTHONPATH for MEC_v13 project

export PYTHONPATH=$(pwd)/MEC_v13:$PYTHONPATH
echo "PYTHONPATH set to: $PYTHONPATH"
