#!/bin/sh

cd $(dirname $(greadlink -f $0))
pelican content -o output -s pelicanconf.py
ghp-import output
git push origin master