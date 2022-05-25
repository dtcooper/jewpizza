FROM ubuntu:20.04

ARG LIQUIDSOAP_VERSION=2.0.5 \
    WAIT_FOR_VERSION=2.2.3 \
    DEBUG=0

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        festival \
        festvox-kallpc16k \
        netcat \
        wget \
        # Build deps
        ca-certificates \
        jq \
        # Dev requirements
        $([ "$DEBUG" -a "$DEBUG" != '0' ] && echo \
            inotify-tools \
            netcat-traditional \
            python3-pygments \
            python3-setuptools \
            rlwrap \
        ) \
    && . /etc/lsb-release \
    && DEB_URL="$(wget -qO - "https://api.github.com/repos/savonet/liquidsoap/releases/tags/v${LIQUIDSOAP_VERSION}" \
        | jq -r .assets[].browser_download_url | fgrep "$DISTRIB_CODENAME" | fgrep "$(dpkg --print-architecture)")" \
    && wget -qO /tmp/liquidsoap.deb "$DEB_URL" \
    && apt-get install -y --no-install-recommends /tmp/liquidsoap.deb \
    && wget -qO /usr/local/bin/wait-for "https://raw.githubusercontent.com/eficode/wait-for/v${WAIT_FOR_VERSION}/wait-for" \
    && chmod +x /usr/local/bin/wait-for \
    && if [ -z "$$DEBUG" -o "$$DEBUG" = 0 ]; then \
        apt-get remove -y --purge --autoremove \
            ca-certificates \
            jq \
    ; fi \
    && rm -rf /tmp/liquidsoap.deb /var/lib/apt/lists/*

RUN usermod -d /radio liquidsoap
COPY --chown=liquidsoap reload.liq /radio/script.liq
COPY image/ /

USER liquidsoap
WORKDIR /radio
ENTRYPOINT ["/entrypoint.sh"]
CMD []

HEALTHCHECK --start-period=30s CMD [ "/healthcheck.sh" ]
