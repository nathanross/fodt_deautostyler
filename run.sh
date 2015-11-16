#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

isFile() {
    [ $1 ] && [ -e "$1" ] && [ -f "$1" ]
    return $?
}

error() {
    echo "$1"
    exit 1
}

main() {
    isFile "$1" || error "error, first arg must be file to clean"
    [ $2 ] || error "error, second arg must be wait or once"
    if [ ! -e ${DIR}/env ]; then
        pyvenv-3.4 ${DIR}/env
        source ${DIR}/env/bin/activate
        pip install -r ${DIR}/requirements.txt
    fi
    if [[ $2 == "wait" ]]; then
        while [ -e "$1" ] && [ -f "$1" ];
        do
            inotifywait -e modify "$1";
            python3 ${DIR}/fodtclean.py "$1";
        done
    else
        python3 ${DIR}/fodtclean.py "$1";
    fi
}
main $@
