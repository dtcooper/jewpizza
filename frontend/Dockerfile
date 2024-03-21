FROM node:21.7.1

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        rsync \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]
CMD []
