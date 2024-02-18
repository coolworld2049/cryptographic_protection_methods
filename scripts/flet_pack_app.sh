#!/usr/bin/env bash

cd ../src/replacement_method
. ../../scripts/pyproject_to_requirements.sh
flet pack app.py -n trithemius_cipher -y
cd ../../scripts