#!/bin/sh

cd /radio

if [ -f /.env ]; then
    . /.env
else
    echo "Couldn't find .env file. Exiting."
    exit 1
fi

if [ "$#" != 0 ]; then
    exec "$@"
else
    wait-for-it -t 0 app:8000
    wait-for-it -t 0 redis:6379

    SCRIPT="/radio/script.liq"
    sed -i "s/^SECRET_KEY.*/SECRET_KEY = '$SECRET_KEY'  # from entrypoint.sh/" "$SCRIPT"
    sed -i "s/^DEBUG.*/DEBUG = $([ "$DEBUG" -a "$DEBUG" != '0' ] && echo 'true' || echo 'false')  # from entrypoint.sh/" "$SCRIPT"
    echo "Replaced SECRET_KEY and DEBUG in $SCRIPT"

    if [ "$DEBUG" -a "$DEBUG" != '0' -a -d /watch ]; then
        # Auto-reload on changes to backend/radio/jinja2/radio/*.liq (mounted as /watch)
        LIQUIDSOAP_PID=

        exit_handler () {
            if [ "$LIQUIDSOAP_PID" ]; then
                kill "$LIQUIDSOAP_PID"
                wait
            fi
            exit 0
        }
        trap exit_handler INT TERM

        liquidsoap -f "$SCRIPT" &
        LIQUIDSOAP_PID="$!"

        while true; do
            inotifywait -qq -e modify -e move -e create -e delete -e attrib /watch/
            echo "DEBUG: Reloading script based on file modification"
            wget -qO /dev/null --header="X-Secret-Key: $SECRET_KEY" http://localhost:8000/reload
        done
    else
        exec liquidsoap -f "$SCRIPT"
    fi
fi
