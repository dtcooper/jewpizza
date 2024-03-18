#!/bin/bash

set -e

ME="$(basename "$0")"

entrypoint_log() {
    if [ -z "${NGINX_ENTRYPOINT_QUIET_LOGS:-}" ]; then
        echo "$@"
    fi
}

auto_jinja2() {
  local template_dir="${NGINX_JINJA2_TEMPLATE_DIR:-/etc/nginx/templates}"
  local suffix="${NGINX_JINJA2_TEMPLATE_SUFFIX:-.j2}"
  local output_dir="${NGINX_JINJA2_OUTPUT_DIR:-/etc/nginx/conf.d}"

  local template relative_path output_path subdir
  if [ ! -w "$output_dir" ]; then
    entrypoint_log "$ME: ERROR: $template_dir exists, but $output_dir is not writable"
    return 0
  fi

  find "$template_dir" -follow -type f -name "*$suffix" -print | while read -r template; do
    relative_path="${template#"$template_dir/"}"
    output_path="$output_dir/${relative_path%"$suffix"}"
    subdir=$(dirname "$relative_path")
    mkdir -p "$output_dir/$subdir"
    entrypoint_log "$ME: jinja2 template $template rendered as $output_path"
    jinja2 --strict "$template" > "$output_path"
    nginxfmt --indent 2 "$output_path"

    if [ "$DEV_MODE" -a "$DEV_MODE" != '0' ]; then
        echo "======= rendered config: $output_path ======="
        cat "$output_path"
        echo '============================================='
    fi
  done
}

auto_jinja2
