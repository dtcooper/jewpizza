#!/bin/bash

cd /radio

if [ -f /.env ]; then
    . /.env
else
    echo "Couldn't find .env file. Exiting."
    exit 1
fi

if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
    DEBUG=1
else
    DEBUG=
fi

SCRIPT="/radio/script.liq"

run_liquidsoap_loop_debug () {
    while true; do
        liquidsoap -f "$SCRIPT"
    done
}

run_restart_loop_debug () {
    while true; do
        # Auto-reload on changes to backend/radio/jinja2/radio/*.liq (mounted as /watch)
        inotifywait -qq -e modify -e move -e create -e delete -e attrib /watch/
        echo "DEBUG: Reloading script based on file modification"
        wget -qO /dev/null --header="X-Secret-Key: $SECRET_KEY" http://localhost:8000/reload
    done
}

wait_for_service() {
    echo "Waiting for ${1}..."
    wait-for -t 0 "$1"
}

if [ "$#" != 0 ]; then
    exec "$@"
else
    echo "Waiting for app:8000..."
    wait-for -t 0 app:8000

    sed -i "s/^SECRET_KEY.*/SECRET_KEY = '$SECRET_KEY'  # from entrypoint.sh/" "$SCRIPT"
    sed -i "s/^DEBUG.*/DEBUG = $([ "$DEBUG" ] && echo 'true' || echo 'false')  # from entrypoint.sh/" "$SCRIPT"
    echo "Replaced SECRET_KEY and DEBUG in $SCRIPT"

    if [ "$DEBUG" -a -d /watch ]; then
        trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT  # /bin/bash needed to kill children (not /bin/sh)
        run_liquidsoap_loop_debug &
        run_restart_loop_debug &
        wait
    else
        exec liquidsoap -f "$SCRIPT"
    fi
fi
