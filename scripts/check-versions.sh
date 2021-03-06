#!/bin/sh

GITHUB_ACTION=

if [ "$1" = 'github-action' ]; then
    GITHUB_ACTION=1
elif [ ! -f /.dockerenv ]; then
    echo 'Must run in docker container'
    exit 1
fi

cd "$(dirname "$0")/.."

grep_quote () {
    echo "$*" | sed 's/[^\^]/[&]/g;s/[\^]/\\&/g'
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

PYTHON_LOCAL="$(grep '^FROM python' backend/Dockerfile | sed 's/FROM python:\([0-9.]*\)-alpine[0-9.]* AS base/\1/')"
PYTHON_UPSTREAM="$(lastversion python/cpython)"
compare Python "$PYTHON_LOCAL" "$PYTHON_UPSTREAM" 1

POSTGRES_LOCAL="$(yq -r .services.db.image docker-compose.yml | sed 's/^library\/postgres:\(.*\)-alpine/\1/')"
POSTGRES_UPSTREAM="$(lastversion postgres/postgres)"
compare PostgreSQL "$POSTGRES_LOCAL" "$POSTGRES_UPSTREAM" 1

REDIS_LOCAL="$(yq -r .services.redis.image docker-compose.yml | sed 's/^library\/redis:\(.*\)-alpine/\1/')"
REDIS_UPSTREAM="$(lastversion redis/redis)"
compare Redis "$REDIS_LOCAL" "$REDIS_UPSTREAM" 1

LIQUIDSOAP_LOCAL="$(fgrep 'LIQUIDSOAP_VERSION=' radio/Dockerfile | sed 's/.*LIQUIDSOAP_VERSION=\([0-9.]*\).*/\1/')"
LIQUIDSOAP_UPSTREAM="$(lastversion savonet/liquidsoap)"
compare Liquidsoap "$LIQUIDSOAP_LOCAL" "$LIQUIDSOAP_UPSTREAM"

DOZZLE_LOCAL="$(yq -r .services.logs.image docker-compose.yml | sed 's/^amir20\/dozzle:v//')"
DOZZLE_UPSTREAM="$(lastversion amir20/dozzle)"
compare Dozzle "$DOZZLE_LOCAL" "$DOZZLE_UPSTREAM"

UMAMI_LOCAL="$(yq -r .services.umami.image docker-compose.yml | sed 's/^ghcr.io\/mikecao\/umami:postgresql-v\(.*\)/\1/')"
UMAMI_UPSTREAM="$(lastversion mikecao/umami)"
compare Umami "$UMAMI_LOCAL" "$UMAMI_UPSTREAM"

ICECAST_KH_LOCAL="$(fgrep 'ICECAST_KH_VERSION=' icecast/Dockerfile | sed 's/.*ICECAST_KH_VERSION="\([0-9a-zA-Z.-]*\).*/\1/')"
ICECAST_KH_REMOTE="$(wget --header "Authorization: token ${GITHUB_API_TOKEN}" -qO - "https://api.github.com/repos/karlheyes/icecast-kh/releases/latest" | jq -r .tag_name | sed 's/^icecast-//')"
compare icecast-kh "$ICECAST_KH_LOCAL" "$ICECAST_KH_REMOTE"

AUTOHEAL_LOCAL="$(yq -r .services.autoheal.image docker-compose.yml | sed 's/^willfarrell\/autoheal://')"
AUTOHEAL_UPSTREAM="$(lastversion willfarrell/docker-autoheal)"
compare Autoheal "$AUTOHEAL_LOCAL" "$AUTOHEAL_UPSTREAM"

DOCKER_NGINX_CERTBOT_LOCAL="$(grep '^FROM jonasal/nginx-certbot' nginx/Dockerfile | sed 's/FROM jonasal\/nginx-certbot:\(.*\)-nginx.*/\1/')"
DOCKER_NGINX_CERTBOT_UPSTREAM="$(lastversion JonasAlfredsson/docker-nginx-certbot)"
compare docker-nginx-certbot "$DOCKER_NGINX_CERTBOT_LOCAL" "$DOCKER_NGINX_CERTBOT_UPSTREAM"

POETRY_LOCAL="$(fgrep 'POETRY_VERSION=' backend/Dockerfile | head -n 1 | sed 's/.*POETRY_VERSION=\([0-9.]*\).*/\1/')"
POETRY_UPSTREAM="$(lastversion python-poetry/poetry)"
compare Poetry "$POETRY_LOCAL" "$POETRY_UPSTREAM"

JINJA2_CLI_LOCAL="$(fgrep 'JINJA2_CLI_VERSION=' nginx/Dockerfile | sed 's/.*JINJA2_CLI_VERSION=\([0-9.]*\).*/\1/')"
JINJA2_CLI_UPSTREAM="$(lastversion mattrobenolt/jinja2-cli)"
compare jinja2-cli "$JINJA2_CLI_LOCAL" "$JINJA2_CLI_UPSTREAM"

NGINX_BROTLI_LOCAL="$(fgrep 'NGX_BROTLI_VERSION=' nginx/Dockerfile | sed 's/.*NGX_BROTLI_VERSION=\([0-9a-zA-Z]*\).*/\1/')"
NGINX_BROTLI_DEFAULT_BRANCH="$(wget --header "Authorization: token ${GITHUB_API_TOKEN}" -qO - "https://api.github.com/repos/google/ngx_brotli" | jq -r .default_branch)"
NGINX_BROTLI_UPSTREAM="$(wget --header "Authorization: token ${GITHUB_API_TOKEN}" -qO - "https://api.github.com/repos/google/ngx_brotli/commits/$NGINX_BROTLI_DEFAULT_BRANCH" | jq -r .sha)"
compare nginx-brotli "$NGINX_BROTLI_LOCAL" "$NGINX_BROTLI_UPSTREAM" 1

NCHAN_LOCAL="$(fgrep 'NCHAN_VERSION=' nginx/Dockerfile | sed 's/.*NCHAN_VERSION=\([0-9.]*\).*/\1/')"
NCHAN_UPSTREAM="$(lastversion slact/nchan)"
compare nchan "$NCHAN_LOCAL" "$NCHAN_UPSTREAM"

NGINX_DEVEL_KIT_LOCAL="$(fgrep 'NGX_DEVEL_KIT_VERSION=' nginx/Dockerfile | sed 's/.*NGX_DEVEL_KIT_VERSION=\([rc0-9.]*\).*/\1/')"
NGINX_DEVEL_KIT_UPSTREAM="$(lastversion --pre vision5/ngx_devel_kit)"
compare 'devel kit nginx module' "$NGINX_DEVEL_KIT_LOCAL" "$NGINX_DEVEL_KIT_UPSTREAM"

NGINX_HEADERS_MORE_LOCAL="$(fgrep 'NGX_HEADERS_MORE_VERSION=' nginx/Dockerfile | sed 's/.*NGX_HEADERS_MORE_VERSION=\([rc0-9.]*\).*/\1/')"
NGINX_HEADERS_MORE_UPSTREAM="$(lastversion --pre openresty/headers-more-nginx-module)"
compare 'headers-more nginx module' "$NGINX_HEADERS_MORE_LOCAL" "$NGINX_HEADERS_MORE_UPSTREAM"

LUA_RESTY_CORE_LOCAL="$(fgrep 'NGX_LUA_RESTY_CORE_VERSION=' nginx/Dockerfile | sed 's/.*NGX_LUA_RESTY_CORE_VERSION=\([rc0-9.]*\).*/\1/')"
LUA_RESTY_CORE_UPSTREAM="$(lastversion --pre openresty/lua-resty-core)"
compare 'resty-core lua module' "$LUA_RESTY_CORE_LOCAL" "$LUA_RESTY_CORE_UPSTREAM"

LUA_RESTY_LRUCACHE_LOCAL="$(fgrep 'NGX_LUA_RESTY_LRUCACHE_VERSION=' nginx/Dockerfile | sed 's/.*NGX_LUA_RESTY_LRUCACHE_VERSION=\([rc0-9.]*\).*/\1/')"
LUA_RESTY_LRUCACHE_UPSTREAM="$(lastversion --pre openresty/lua-resty-lrucache)"
compare 'resty-lrucache lua module' "$LUA_RESTY_LRUCACHE_LOCAL" "$LUA_RESTY_LRUCACHE_UPSTREAM"

LUA_RESTY_REDIS_LOCAL="$(fgrep 'NGX_LUA_RESTY_REDIS_VERSION=' nginx/Dockerfile | sed 's/.*NGX_LUA_RESTY_REDIS_VERSION=\([rc0-9.]*\).*/\1/')"
LUA_RESTY_REDIS_UPSTREAM="$(lastversion --pre openresty/lua-resty-redis)"
compare 'resty-redis lua module' "$LUA_RESTY_REDIS_LOCAL" "$LUA_RESTY_REDIS_UPSTREAM"

NGINX_LUA_LOCAL="$(fgrep 'NGX_LUA_VERSION=' nginx/Dockerfile | sed 's/.*NGX_LUA_VERSION=\([rc0-9.]*\).*/\1/')"
NGINX_LUA_UPSTREAM="$(lastversion --pre openresty/lua-nginx-module)"
compare 'lua nginx module' "$NGINX_LUA_LOCAL" "$NGINX_LUA_UPSTREAM"

AUDIOWAVEFORM_LOCAL="$(fgrep 'AUDIOWAVEFORM_VERSION=' backend/Dockerfile | sed 's/.*AUDIOWAVEFORM_VERSION=\([0-9.]*\).*/\1/')"
AUDIOWAVEFORM_UPSTREAM="$(lastversion bbc/audiowaveform)"
compare audiowaveform "$AUDIOWAVEFORM_LOCAL" "$AUDIOWAVEFORM_UPSTREAM"

WAIT_FOR_LOCAL="$(fgrep 'WAIT_FOR_VERSION=' backend/Dockerfile | sed 's/.*WAIT_FOR_VERSION=\([0-9.]*\).*/\1/')"
WAIT_FOR_UPSTREAM="$(lastversion eficode/wait-for)"
compare wait-for "$WAIT_FOR_LOCAL" "$WAIT_FOR_UPSTREAM"

ICONIFY_LOCAL="$(fgrep iconify backend/webcore/jinja2/webcore/base_full.html | sed 's/.*iconify\/\([0-9.]*\)\/.*/\1/')"
ICONIFY_UPSTREAM="$(npm --silent view @iconify/iconify version)"
compare Iconify "$ICONIFY_LOCAL" "$ICONIFY_UPSTREAM"
