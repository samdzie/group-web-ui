#!/bin/bash

# Run Mountebank in the background for upstream service stubs
config=$(dirname $0)/mb-config.json
mb start --nologfile --configfile $config > /dev/null &

# Run tests
pytest

# Tear down Mountebank
mb stop
