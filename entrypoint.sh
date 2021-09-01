#!/bin/sh

if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
    DEBUG=1
    npm install
else
    DEBUG=
fi

if [ "$#" = 0 ]; then
    if [ "$DEBUG" ]; then
        exec npm run runserver
    else
        # XXX
        poetry run ./manage.py runserver
    fi
else
    exec "$@"
fi
