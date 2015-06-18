#!/bin/bash
# requires inotify-tools
[ $1 ] || ( echo "error, first arg must be file to watch" && exit 1 )
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
while [ -e "$1" ] && [ -f "$1" ];
do
    inotifywait -e modify "$1";
    python3 ${DIR}/fodtclean.py "$1";
done
