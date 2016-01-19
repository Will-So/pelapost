#!/bin/sh

cd $(dirname $(greadlink -f $0))
pelican content -o output -s pelicanconf.py
ghp-import output
git push origin gh-pages:master
# git push git@github.com:Will-So/Will-So.github.io.git gh-pages:master