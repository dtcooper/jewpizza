#!/bin/sh

cd /radio

if [ -f /.env ]; then
    . /.env
else
    echo "Couldn't find .env file. Exiting."
    exit 1
fi

download_script () {
    URL="http://app:8000/internal/radio/liquidsoap/script/"
    SCRIPT="/radio/script.liq"

    if ! wget "--header=X-Secret-Key: $SECRET_KEY" -qO /radio/script.liq "$URL" ; then
        echo "Error fetching script at $URL"
        exit 1
    fi

    echo "Downloaded script to $SCRIPT"
    if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
        echo '===== script.liq ====='
        pygmentize -l ruby "$SCRIPT" | cat -n
        echo '======================'
    fi
}

if [ "$#" != 0 ]; then
    exec "$@"
else
    wait-for-it -t 0 app:8000
    wait-for-it -t 0 redis:6379

    download_script

    if [ "$DEBUG" -a "$DEBUG" != '0' -a -d /watch ]; then
        LIQUIDSOAP_PID=

        exit_handler () {
            if [ "$LIQUIDSOAP_PID" ]; then
                kill "$LIQUIDSOAP_PID"
                wait
            fi
            exit 0
        }
        trap exit_handler INT TERM

        while true; do
            liquidsoap "$SCRIPT" &
            LIQUIDSOAP_PID="$!"
            inotifywait -qq --includei '\.liq$' -e modify -e move -e create -e delete -e attrib /watch/
            echo 'Detecting change in script. Restarting Liquidsoap.'
            kill "$LIQUIDSOAP_PID"
            wait
            download_script
        done
    else
        exec liquidsoap "$SCRIPT"
    fi
fi
