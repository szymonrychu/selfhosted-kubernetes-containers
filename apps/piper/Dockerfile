FROM debian:bullseye-slim@sha256:715354035496a48b9c4c8f146a6f751de70449913773038776eb1f3d01c93989

# renovate: repository=https://github.com/rhasspy/piper.git
ARG PIPER_RELEASE='2023.11.14-2'

COPY requirements.txt /tmp/requirements.txt

RUN set -xe;\
    apt-get update;\
    apt-get install -y --no-install-recommends \
        curl \
        python3 \
        python3-pip \
    ;\
    pip3 install --no-cache-dir -U \
        setuptools \
        wheel \
    ;\
    rm -rf /var/lib/apt/lists/*;\
    pip3 install --no-cache-dir -r /tmp/requirements.txt;\
    curl -L -s \
        "https://github.com/rhasspy/piper/releases/download/${PIPER_RELEASE}/piper_linux_x86_64.tar.gz" \
        | tar -zxvf - -C /usr/share

WORKDIR /

EXPOSE 10200

ENTRYPOINT ["/usr/bin/python3", "-m", "wyoming_piper", "--piper", "/usr/share/piper/piper" ]


