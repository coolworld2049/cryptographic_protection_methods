#!/usr/bin/env bash

flet pack main.py -v -y \
--name cryptographic_protection_methods \
--product-name cryptographic_protection_methods \
--company-name coolworld2049
--hidden-import=ciphers \
--add-data "assets;assets" \
-i assets/gravity_falls.png

git add -f dist
rm -r build
rm *.spec