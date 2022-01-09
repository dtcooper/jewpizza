#!/bin/sh

cd /app/backend

# Use the poetry's virtualenv
export PATH="$(poetry env info -p)/bin:$PATH"

# Source .env file
if [ -f /.env ]; then
    . /.env
else
    echo "Couldn't find .env file. Exiting."
    exit 1
fi

if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
    DEBUG=1
    if [ ! -f ../docker-compose.override.yml ]; then
        echo "WARNING: docker-compose.override.yml NOT found. You'll need to symlink so DEBUG can to work properly."
    fi
else
    DEBUG=
fi

if [ "$RUN_HUEY" ]; then
    export __RUN_HUEY=1
fi

if [ -z "$SECRET_KEY" ]; then
    echo "SECRET_KEY not set. Exiting."
    exit 1
fi

init_db () {
    if [ "$(./manage.py shell -c 'from django.contrib.auth.models import User; print("" if User.objects.exists() else "1")')" = 1 ]; then
        DJANGO_SUPERUSER_PASSWORD=cooper ./manage.py createsuperuser --noinput --username dave --email 'david@jew.pizza'
    fi

    ./manage.py loaddata shows/showdates.json shows/episodes.json
}

init_umami () {
    if [ -z "$(./manage.py constance get UMAMI_WEBSITE_ID)" ]; then
        echo "No UMAMI_WEBSITE_ID with DEBUG = True. Setting..."
        wait-for-it -t 0 umami:3000
        WEBSITE_ID="$(cat <<'END' | python
import requests

token = requests.post(
'http://umami:3000/api/auth/login',
json={'username': 'dave', 'password': 'cooper'}).json()['token']
uuid = requests.post(
'http://umami:3000/api/website',
json={'domain': 'localhost', 'name': 'jew.pizza local dev', 'enable_share_url': False},
headers={'Cookie': f'umami.auth={token}'}).json()['website_uuid']
print(uuid)
END
)"
        wait-for-it -t 0 redis:6379
        ./manage.py constance set UMAMI_WEBSITE_ID "$WEBSITE_ID"
    fi
}

if [ "$#" != 0 ]; then
    if [ "$DEBUG" ] ; then
        # Make psql work easily
        export PGHOST=db
        export PGUSER=postgres
        export PGPASSWORD=postgres
    fi

    exec "$@"

elif [ "$RUN_HUEY" ]; then
    if [ -z "$HUEY_WORKERS" ]; then
        HUEY_WORKERS="$(python -c 'import multiprocessing as m; print(max(m.cpu_count() * 3, 6))')"
    fi

    wait-for-it -t 0 db:5432 &
    wait-for-it -t 0 redis:6379 &
    wait

    CMD="./manage.py run_huey --workers $HUEY_WORKERS --flush-locks"
    if [ "$DEBUG" ]; then
        exec watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- $CMD
    else
        exec $CMD
    fi

else
    wait-for-it -t 0 db:5432 -- ./manage.py migrate &

    if [ "$DEBUG" -a ! -d '../frontend/node_modules' ]; then
        # In case /app is mounted in Docker, needed to re-install the /app/frontend/node_modules folder
        npm --prefix=../frontend install &
    fi

    if [ -z "$DEBUG" ]; then
        ./manage.py collectstatic --noinput &
    fi

    wait-for-it -t 0 redis:6379 &

    # Wait on DB migrated, static collected, and redis up. Ready to start afterwards.
    wait

    # We can initialize the DB (fixtures) async
    init_db &

    if [ "$DEBUG" ]; then
        init_umami &
        exec ./manage.py runserver
    else
        if [ -z "$GUNICORN_WORKERS" ]; then
            # Number of workers =  min(<cores * 1.5 rounded up> + 1, 3)
            GUNICORN_WORKERS="$(python -c 'import multiprocessing as m; print(max(round(m.cpu_count() * 1.5 + 1), 3))')"
        fi

        exec gunicorn \
                $GUNICORN_EXTRA_ARGS \
                --forwarded-allow-ips '*' \
                -b 0.0.0.0:8000 \
                -w $GUNICORN_WORKERS \
                --capture-output \
                --error-logfile - \
                --access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
                --access-logfile - \
            jew_pizza.wsgi
    fi
fi
