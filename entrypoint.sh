#!/bin/sh

if [ -f /.env ]; then
    . /.env
fi

if [ "$#" = 0 ]; then


    if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
        exec poetry run ./manage.py runserver
    else
        poetry run ./manage.py collectstatic --noinput
        wait-for-it -t 0 db:5432
        poetry run ./manage.py migrate

        if [ -z "$GUNICORN_WORKERS" ]; then
            GUNICORN_WORKERS="$(python -c 'import multiprocessing as m; print(max(round(m.cpu_count() * 1.5 + 1), 3))')"
        fi

        exec poetry run gunicorn \
                $GUNICORN_EXTRA_ARGS \
                --forwarded-allow-ips '*' \
                -b 0.0.0.0:8000 \
                -w $GUNICORN_WORKERS \
                --capture-output \
                --access-logfile - \
            jew_pizza.wsgi
    fi
else
    exec $@
fi
