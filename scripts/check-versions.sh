#!/usr/bin/env bash

GITHUB_ACTION=

if [ "$1" = 'github-action' ]; then
    GITHUB_ACTION=1
elif [ ! -f /.dockerenv ]; then
    echo 'Must run in docker container'
    exit 1
fi

cd "$(dirname "$0")/.."

grep_quote () {
    sed 's/[^\^]/[&]/g;s/[\^]/\\&/g' <<< "$*"
}

compare () {
    NAME="$1"
    LOCAL="$2"
    UPSTREAM="$3"
    FUZZY="$4"
    OP='='
    UP_TO_DATE=1

    if [ -z "$FUZZY" ]; then
        if [ "$UPSTREAM" != "$LOCAL" ]; then
            OP='!='
            UP_TO_DATE=
        fi
    else
        if echo "$UPSTREAM" | grep -q "^$(grep_quote "$LOCAL")"; then
            OP='^='
        else
            OP='!^='
            UP_TO_DATE=
        fi
    fi

    VERS="$LOCAL (local) $OP $UPSTREAM (remote)"

    if [ -z "$UP_TO_DATE" ]; then
        # Red
        if [ "$GITHUB_ACTION" ]; then
            echo "${NAME} needs updating! ${VERS}"
        else
            echo -e "\x1B[91m${NAME} needs updating! ${VERS}\x1B[0m"
        fi
    elif [ -z "$GITHUB_ACTION" ]; then
        # Green
        echo -e "\x1B[92m${NAME} up to date.\x1B[0m $VERS"
    fi
}

if [ -z "$GITHUB_API_TOKEN" ]; then
    echo -e "\x1B[91mWarning: GITHUB_API_TOKEN not set\x1B[0m"
fi

PYTHON_LOCAL="$(grep '^FROM python' backend/Dockerfile | sed 's/FROM python:\(.*\) as base/\1/')"
PYTHON_UPSTREAM="$(lastversion python/cpython)"
compare Python "$PYTHON_LOCAL" "$PYTHON_UPSTREAM" 1

POSTGRES_LOCAL="$(yq -r .services.db.image docker-compose.yml | sed 's/^library\/postgres:\(.*\)-alpine/\1/')"
POSTGRES_UPSTREAM="$(lastversion postgres/postgres)"
compare PostgreSQL "$POSTGRES_LOCAL" "$POSTGRES_UPSTREAM" 1

REDIS_LOCAL="$(yq -r .services.redis.image docker-compose.yml | sed 's/^library\/redis:\(.*\)-alpine/\1/')"
REDIS_UPSTREAM="$(lastversion redis/redis)"
compare Redis "$REDIS_LOCAL" "$REDIS_UPSTREAM" 1

LIQUIDSOAP_LOCAL="$(grep '^FROM ' radio/Dockerfile | sed 's/^FROM savonet\/liquidsoap:v\([0-9.]*\).*/\1/')"
LIQUIDSOAP_UPSTREAM="$(lastversion savonet/liquidsoap)"
compare Liquidsoap "$LIQUIDSOAP_LOCAL" "$LIQUIDSOAP_UPSTREAM"

DOZZLE_LOCAL="$(yq -r .services.logs.image docker-compose.yml | sed 's/^amir20\/dozzle:v//')"
DOZZLE_UPSTREAM="$(lastversion amir20/dozzle)"
compare Dozzle "$DOZZLE_LOCAL" "$DOZZLE_UPSTREAM"

UMAMI_LOCAL="$(yq -r .services.umami.image docker-compose.yml | sed 's/^ghcr.io\/mikecao\/umami:postgresql-\(.*\)/\1/')"
UMAMI_UPSTREAM="$(curl -s --user "dtcooper:$GITHUB_API_TOKEN" https://api.github.com/users/mikecao/packages/container/umami/versions | jq -r .[].metadata.container.tags | grep -A 1 postgresql-latest | tail -n1 | sed 's/.*postgresql-\([0-9a-f]*\).*/\1/')"
compare Umami "$UMAMI_LOCAL" "$UMAMI_UPSTREAM"

ICECAST_KH_LOCAL="$(fgrep 'ICECAST_KH_VERSION=' icecast/Dockerfile | sed 's/.*ICECAST_KH_VERSION="\([0-9a-zA-Z.-]*\).*/\1/')"
ICECAST_KH_REMOTE="$(curl -s --user "dtcooper:$GITHUB_API_TOKEN" https://api.github.com/repos/karlheyes/icecast-kh/releases/latest | jq -r .tag_name | sed 's/^icecast-//')"
compare icecast-kh "$ICECAST_KH_LOCAL" "$ICECAST_KH_REMOTE"

AUTOHEAL_LOCAL="$(yq -r .services.autoheal.image docker-compose.yml | sed 's/^willfarrell\/autoheal://')"
AUTOHEAL_UPSTREAM="$(lastversion willfarrell/docker-autoheal)"
compare Autoheal "$AUTOHEAL_LOCAL" "$AUTOHEAL_UPSTREAM"

DOCKER_NGINX_CERTBOT_LOCAL="$(grep '^FROM jonasal/nginx-certbot' nginx/Dockerfile | sed 's/FROM jonasal\/nginx-certbot:\(.*\)-alpine AS base/\1/')"
DOCKER_NGINX_CERTBOT_UPSTREAM="$(lastversion JonasAlfredsson/docker-nginx-certbot)"
compare docker-nginx-certbot "$DOCKER_NGINX_CERTBOT_LOCAL" "$DOCKER_NGINX_CERTBOT_UPSTREAM" 1

POETRY_LOCAL="$(fgrep 'POETRY_VERSION=' backend/Dockerfile | sed 's/.*POETRY_VERSION=\([0-9.]*\).*/\1/')"
POETRY_UPSTREAM="$(lastversion python-poetry/poetry)"
compare Poetry "$POETRY_LOCAL" "$POETRY_UPSTREAM"

JINJA2_CLI_LOCAL="$(fgrep 'JINJA2_CLI_VERSION=' nginx/Dockerfile | sed 's/.*JINJA2_CLI_VERSION=\([0-9.]*\).*/\1/')"
JINJA2_CLI_UPSTREAM="$(lastversion mattrobenolt/jinja2-cli)"
compare jinja2-cli "$JINJA2_CLI_LOCAL" "$JINJA2_CLI_UPSTREAM"

NGINX_BROTLI_LOCAL="$(fgrep 'NGX_BROTLI_VERSION=' nginx/Dockerfile | sed 's/.*NGX_BROTLI_VERSION=\([0-9a-zA-Z]*\).*/\1/')"
NGINX_BROTLI_DEFAULT_BRANCH="$(curl -s --user "dtcooper:$GITHUB_API_TOKEN" https://api.github.com/repos/google/ngx_brotli | jq -r .default_branch)"
NGINX_BROTLI_UPSTREAM="$(curl -s --user "dtcooper:$GITHUB_API_TOKEN" "https://api.github.com/repos/google/ngx_brotli/commits/$NGINX_BROTLI_DEFAULT_BRANCH" | jq -r .sha)"
compare nginx-brotli "$NGINX_BROTLI_LOCAL" "$NGINX_BROTLI_UPSTREAM" 1

NCHAN_LOCAL="$(fgrep 'NCHAN_VERSION=' nginx/Dockerfile | sed 's/.*NCHAN_VERSION=\([0-9.]*\).*/\1/')"
NCHAN_UPSTREAM="$(lastversion slact/nchan)"
compare nchan "$NCHAN_LOCAL" "$NCHAN_UPSTREAM"

AUDIOWAVEFORM_LOCAL="$(fgrep 'AUDIOWAVEFORM_VERSION=' backend/Dockerfile | sed 's/.*AUDIOWAVEFORM_VERSION=\([0-9.]*\).*/\1/')"
AUDIOWAVEFORM_UPSTREAM="$(lastversion bbc/audiowaveform)"
compare audiowaveform "$AUDIOWAVEFORM_LOCAL" "$AUDIOWAVEFORM_UPSTREAM"

WAIT_FOR_IT_LOCAL="$(fgrep 'WAIT_FOR_IT_VERSION=' backend/Dockerfile | sed 's/.*WAIT_FOR_IT_VERSION=\([0-9a-z]*\).*/\1/')"
WAIT_FOR_IT_DEFAULT_BRANCH="$(curl -s --user "dtcooper:$GITHUB_API_TOKEN" https://api.github.com/repos/vishnubob/wait-for-it | jq -r .default_branch)"
WAIT_FOR_IT_UPSTREAM="$(curl -s --user "dtcooper:$GITHUB_API_TOKEN" "https://api.github.com/repos/vishnubob/wait-for-it/commits/$WAIT_FOR_IT_DEFAULT_BRANCH" | jq -r .sha)"
compare 'wait-for-it' "$WAIT_FOR_IT_LOCAL" "$WAIT_FOR_IT_UPSTREAM" 1

ICONIFY_LOCAL="$(fgrep iconify backend/webcore/jinja2/webcore/base_full.html | sed 's/.*iconify\/\([0-9.]*\)\/.*/\1/')"
ICONIFY_UPSTREAM="$(npm --silent view @iconify/iconify version)"
compare 'iconify' "$ICONIFY_LOCAL" "$ICONIFY_UPSTREAM"
