#!/bin/sh

cd /var/liquidsoap

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

SCRIPT="/var/liquidsoap/script.liq"

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

kill_children() {
    kill $(jobs -p) 2> /dev/null
}

if [ "$#" != 0 ]; then
    exec "$@"
else
    wait_for_service app:8000
    wait_for_service redis:6379

    sed -i "s/^SECRET_KEY.*/SECRET_KEY = '$SECRET_KEY'  # from entrypoint.sh/" "$SCRIPT"
    sed -i "s/^DEBUG.*/DEBUG = $([ "$DEBUG" ] && echo 'true' || echo 'false')  # from entrypoint.sh/" "$SCRIPT"
    echo "Replaced SECRET_KEY and DEBUG in $SCRIPT"

    if [ "$DEBUG" -a -d /watch ]; then
        trap kill_children SIGINT
        trap kill_children SIGTERM
        trap kill_children EXIT
        run_liquidsoap_loop_debug &
        run_restart_loop_debug &
        wait
    else
        exec liquidsoap -f "$SCRIPT"
    fi
fi
