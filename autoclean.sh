#!/bin/bash
[ $1 ] || echo "error, first arg must be file to watch" && exit 1
while [ -e "$1" ] && [ -f "$1" ];
do
    inotifywait -e modify "$1";
    python3 fodtclean.py "$1";
done
