#!/bin/bash

# Run a given command a specified number of times with a specified delay between attempts until it succeeds.

function keep-trying {
    if [[ $# -lt 2 ]]; then
        echo "Error: Not enough arguments."
        echo "Usage: keep-trying COMMAND INTERVAL [MAX_ATTEMPTS]"
        return
    fi

    local idx=0
    local max=""

    if [[ $# -eq 2 ]]; then
        let max=99
    else
        let max=$3
    fi
    echo "Attempting: $1 at an interval of $2 seconds for a max of $max tries."
    while [[ $idx < $max ]]; do
        local cmd="$1"
        type $cmd | grep alias
        if [[ $? -eq 0 ]]; then
            shopt -s expand_aliases
            $cmd = echo "$(cmd)"
            shopt -u expand_aliases
        fi

        $cmd
        local status=$?

        if [[ $status -eq 0 ]]; then
            echo "$1 completed successfully."
            return
        fi
        if [[ $status -eq 127 ]]; then
            return
        fi
        sleep $2
        let idx++
        done
}
