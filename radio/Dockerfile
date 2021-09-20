FROM ubuntu:20.04

ARG LIQUIDSOAP_VERSION="2.0.0-rc1"

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        festival \
        festvox-kallpc16k \
        ffmpeg \
        wget \
    && rm -rf /var/lib/apt/lists/*

RUN ARCH="$(dpkg --print-architecture)" \
    DEB_NAME="liquidsoap-v${LIQUIDSOAP_VERSION}_$(echo "$LIQUIDSOAP_VERSION" | sed 's/-/./')-ubuntu-focal-1_${ARCH}.deb" \
    && wget -qO /tmp/liquidsoap.deb "https://github.com/savonet/liquidsoap/releases/download/v${LIQUIDSOAP_VERSION}/${DEB_NAME}" \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        /tmp/liquidsoap.deb \
    && rm -rf /var/lib/apt/lists/* /tmp/*.deb

COPY radio.liq /etc/radio.liq

USER liquidsoap
CMD ["liquidsoap", "/etc/radio.liq"]
