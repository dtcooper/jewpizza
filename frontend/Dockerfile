FROM node:21.7.1

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        rsync \
    && rm -rf /var/lib/apt/lists/*

COPY package.json package-lock.json /app/
WORKDIR /app
RUN npm install

COPY src /app/src
COPY static /app/static
COPY entrypoint.sh *.config.js /app/
RUN npm run build

ENTRYPOINT ["/app/entrypoint.sh"]
CMD []
