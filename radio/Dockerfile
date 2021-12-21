FROM savonet/liquidsoap:v2.0.1

ENV SCRIPT_NAME=radio

ARG WAIT_FOR_IT_VERSION=81b1373f \
    DEBUG=0

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        festival \
        festvox-kallpc16k \
        redis-tools \
        wget \
        # Dev requirements
        $(if [ "$DEBUG" -a "$DEBUG" != '0' ]; then echo \
            inotify-tools \
            netcat-traditional \
            python3-pygments \
            rlwrap \
        ; fi) \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO /usr/local/bin/wait-for-it "https://raw.githubusercontent.com/vishnubob/wait-for-it/${WAIT_FOR_IT_VERSION}/wait-for-it.sh" \
    && chmod +x /usr/local/bin/wait-for-it

RUN mkdir /radio && chown liquidsoap:liquidsoap /radio && usermod -d /radio liquidsoap

COPY entrypoint.sh failsafe.mp3 jingle.mp3 /

USER liquidsoap
WORKDIR /radio
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
CMD []
