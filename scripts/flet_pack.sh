#!/usr/bin/env bash

cd ../src/replacement_method
. ../../scripts/pyproject_to_requirements.sh
echo "algorithm" >> requirements.txt
flet pack app.py -D -y
cd ../../scripts