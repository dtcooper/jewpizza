FROM node:21.7.1-alpine3.19

RUN apk add --no-cache rsync

COPY package.json package-lock.json /app/
WORKDIR /app
RUN npm install

COPY src /app/src
COPY static /app/static
COPY entrypoint.sh *.config.js /app/
RUN npm run build

ENTRYPOINT ["/app/entrypoint.sh"]
CMD []
