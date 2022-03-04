FROM savonet/liquidsoap-alpine:v2.0.3

ARG WAIT_FOR_VERSION=2.2.2 \
    DEBUG=0

USER root

RUN apk add --no-cache \
        inotify-tools \
        mimic1 \
        # Dev requirements
        $([ "$DEBUG" -a "$DEBUG" != '0' ] && echo \
            py3-pygments \
            rlwrap \
        )

RUN wget -qO /usr/local/bin/wait-for "https://raw.githubusercontent.com/eficode/wait-for/v${WAIT_FOR_VERSION}/wait-for" \
    && chmod +x /usr/local/bin/wait-for

COPY --chown=liquidsoap reload.liq /var/liquidsoap/script.liq
COPY image/ /

USER liquidsoap
WORKDIR /var/liquidsoap
ENTRYPOINT ["/sbin/tini", "--", "/entrypoint.sh"]
CMD []

HEALTHCHECK --start-period=30s CMD [ "/healthcheck.sh" ]
