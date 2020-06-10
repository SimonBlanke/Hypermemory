#!/bin/bash

# Run Tests
pytest \
    --cov=hyperactive/
    -p no:warnings \
    tests/ \
    --durations=10 \
    -rfEX
