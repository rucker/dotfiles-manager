#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
for test in $DIR/*test.py; do env python3.6 $test; done
