FROM savonet/liquidsoap:v2.0.2

ARG WAIT_FOR_IT_VERSION=81b1373f \
    DEBUG=0

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        festival \
        festvox-kallpc16k \
        wget \
        # Dev requirements
        $([ "$DEBUG" -a "$DEBUG" != '0' ] && echo \
            inotify-tools \
            netcat-traditional \
            python3-pygments \
            rlwrap \
        ) \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO /usr/local/bin/wait-for-it "https://raw.githubusercontent.com/vishnubob/wait-for-it/${WAIT_FOR_IT_VERSION}/wait-for-it.sh" \
    && chmod +x /usr/local/bin/wait-for-it

RUN usermod -d /radio liquidsoap
COPY --chown=liquidsoap reload.liq /radio/script.liq
COPY image/ /

USER liquidsoap
WORKDIR /radio
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
CMD []

HEALTHCHECK --start-period=30s CMD [ "/healthcheck.sh" ]
