#!/bin/sh

cd /app

export PATH="$(poetry env info -p)/bin:$PATH"

if [ -f /.env ]; then
    . /.env
else
    echo "Couldn't find .env file. Exiting."
    exit 1
fi

if [ "$#" != 0 ]; then
    exec "$@"
else
    wait-for-it -t 0 redis:6379

    if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
        exec watchmedo auto-restart --directory=./ --pattern=*.py -- python sse.py
    else
        exec gunicorn \
                --worker-class aiohttp.GunicornUVLoopWebWorker \
                --forwarded-allow-ips '*' \
                -b 0.0.0.0:8001 \
                --capture-output \
                --error-logfile - \
                --access-logfile - \
            sse:app
    fi
fi
