#!/usr/bin/env bash

if command -v poetry &> /dev/null; then
  poetry export --without-hashes --format=requirements.txt > requirements.txt
else
    echo "Poetry is not installed. Please install it from https://python-poetry.org/docs/."
fi