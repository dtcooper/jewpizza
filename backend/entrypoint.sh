#!/bin/bash

set -e

if [ "$#" = 0 ]; then
    wait-for-it --timeout 0 --service db:5432 --service redis:6379

    ./manage.py migrate

    if [ -z "$DEV_MOD" -o "$DEV_MODE" = '0' ]; then
        ./manage.py collectstatic --noinput
    fi

    exec uvicorn --host 0.0.0.0 --port 8000 --reload jewpizza.asgi:application
else
    echo "Executing: $*"
    exec "$@"
fi
