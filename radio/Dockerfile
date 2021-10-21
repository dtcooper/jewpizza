FROM savonet/liquidsoap:v2.0.0

ENV SCRIPT_NAME=radio

ARG WAIT_FOR_IT_VERSION=81b1373f

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO /usr/local/bin/wait-for-it "https://raw.githubusercontent.com/vishnubob/wait-for-it/${WAIT_FOR_IT_VERSION}/wait-for-it.sh" \
    && chmod +x /usr/local/bin/wait-for-it

RUN mkdir /radio && chown liquidsoap:liquidsoap /radio

COPY entrypoint.sh failsafe.mp3 jingle.mp3 /

USER liquidsoap
WORKDIR /radio
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
CMD []
