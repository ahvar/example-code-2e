#!/bin/bash

# run this script to set PYTHONPATH of the python interpreter in your virtual environment

# Get the root directory
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Construct PYTHONPATH dynamically based on the project root
export PYTHONPATH="$PROJECT_ROOT:$PROJECT_ROOT/nineteen_concurrency:$PROJECT_ROOT/nineteen_concurrency/av:$PROJECT_ROOT/nineteen_concurrency/primes/:$PROJECT_ROOT/nineteen_concurrency/primes/av"

echo "PYTHONPATH set to: $PYTHONPATH"