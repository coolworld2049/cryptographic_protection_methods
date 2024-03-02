#!/usr/bin/env bash

flet pack main.py -v -y \
--name cryptographic_protection_methods \
--hidden-import=ciphers \
--add-data "assets;assets" \
--distpath release

git add release
rm -r build
rm cryptographic_protection_methods.spec