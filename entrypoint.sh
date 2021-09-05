#!/bin/sh

cd /app/jew_pizza

# Source .env file
if [ -f /.env ]; then
    . /.env
else
    echo "Couldn't find .env file. Exiting."
    exit 1
fi

# Check if secret key is set
if [ -z "$SECRET_KEY" ]; then
    echo 'Generating secret key in .env file'
    NEW_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(40))')"

    if grep -q '^SECRET_KEY=' /.env; then
        # sed in place doesn't work on docker file mounts, so copy
        sed "s/^SECRET_KEY=.*/SECRET_KEY='$NEW_SECRET_KEY'/" /.env > /tmp/new.env
        cat /tmp/new.env > /.env
        rm /tmp/new.env
    else
        echo "\nSECRET_KEY='$NEW_SECRET_KEY'" >> /.env
    fi

    . /.env
fi


if [ "$__RUN_MANAGE" ]; then
    poetry run ./manage.py $@
elif [ "$#" != 0 ]; then
    exec $@
else
    migrate() {
        wait-for-it -t 0 db:5432
        poetry run ./manage.py migrate
    }

    if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
        migrate
        exec poetry run ./manage.py runserver
    else
        poetry run ./manage.py collectstatic --noinput
        migrate

        if [ -z "$GUNICORN_WORKERS" ]; then
            # Number of workers =  min(<cores * 1.5 rounded up> + 1, 3)
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
fi
