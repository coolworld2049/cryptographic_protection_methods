#!/usr/bin/env bash

NAME=Ivanov_N_P__BSBO-06-20
flet pack main.py -v -y \
--name cryptographic_protection_methods-"$NAME" \
--product-name cryptographic_protection_methods-"$NAME" \
--company-name coolworld2049 \
--hidden-import=ciphers \
--add-data "assets;assets" \
--icon assets/gravity_falls.png \
--copyright "$NAME" \
--distpath output

set +e

git add -f output
rm -r build
rm *.spec generated*

set -e