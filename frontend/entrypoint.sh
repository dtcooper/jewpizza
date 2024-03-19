#!/bin/bash

set -e

if [ "$#" = 0 ]; then
    if [ -z "$DEV_MODE" -o "$DEV_MODE" = '0' ]; then
        echo 'Copying static files to /static/frontend'
        rsync -a --delete /app/build/client/ /static/frontend
        SHUTDOWN_TIMEOUT=2 PROTOCOL_HEADER=x-forwarded-proto PORT=8000 exec node build
    else
        npm install
        exec npm run dev -- --port 8000 --host
    fi
else
    echo "Executing: $*"
    exec "$@"
fi
