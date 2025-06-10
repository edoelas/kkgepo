#!/bin/bash

uv pip compile pyproject.toml > requirements.txt
pex -r requirements.txt -o kk.pex --exe main.py
export KKGEPO_ALIASES="$PWD/aliases.yaml"
rm requirements.txt
# Run the application
./kk.pex gepo
