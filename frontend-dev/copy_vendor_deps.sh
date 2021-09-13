#!/bin/sh

# Poor man's way of managing js vendor dependencies with npm

set -e

cd "$(dirname "$0")"

pkg_version() {
    npm list | fgrep "$1@" | sed 's/^.\+@//'
}

ALPINE_SRC="alpinejs/dist/cdn.min.js"
ALPINE_DEST="alpine-$(pkg_version alpinejs).min.js"
ALPINE_LINK="alpine.min.js"
MOMENT_SRC="moment/min/moment.min.js"
MOMENT_DEST="moment-$(pkg_version moment).min.js"
MOMENT_LINK="moment.min.js"
MOMENT_TZ_SRC="moment-timezone/builds/moment-timezone-with-data-1970-2030.min.js"
MOMENT_TZ_DEST="moment-timezone-with-data-1970-2030-$(pkg_version moment-timezone).min.js"
MOMENT_TZ_LINK="moment-timezone.min.js"

PREFIX='../backend/webcore/static/js/vendor'
rm -f $PREFIX/*.min.js

cp -v "node_modules/$ALPINE_SRC" "$PREFIX/$ALPINE_DEST"
cp -v "node_modules/$MOMENT_SRC" "$PREFIX/$MOMENT_DEST"
cp -v "node_modules/$MOMENT_TZ_SRC" "$PREFIX/$MOMENT_TZ_DEST"

cd "$PREFIX"

ln -vs "$ALPINE_DEST" "$ALPINE_LINK"
ln -vs "$MOMENT_DEST" "$MOMENT_LINK"
ln -vs "$MOMENT_TZ_DEST" "$MOMENT_TZ_LINK"
