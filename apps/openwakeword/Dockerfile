FROM debian:bullseye-slim@sha256:e831d9a884d63734fe3dd9c491ed9a5a3d4c6a6d32c5b14f2067357c49b0b7e1

COPY requirements.txt /tmp/requirements.txt

RUN set -xe;\
    apt-get update;\
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        libopenblas0 \
    ;\
    pip3 install --no-cache-dir -U \
        setuptools \
        wheel \
    ;\
    pip3 install --no-cache-dir -r /tmp/requirements.txt --extra-index-url https://www.piwheels.org/simple;\
    rm -rf /var/lib/apt/lists/*

EXPOSE 10400

ENTRYPOINT ["/usr/bin/python3", "-m", "wyoming_openwakeword" ]