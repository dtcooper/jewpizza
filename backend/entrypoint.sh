#!/bin/bash

set -e

if [ "$#" = 0 ]; then
    echo test
else
    echo "Executing: $*"
    exec "$@"
fi
