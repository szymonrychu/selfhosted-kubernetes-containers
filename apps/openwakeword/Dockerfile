FROM debian:bullseye-slim@sha256:d3d0d14f49b49a4dd98a436711f5646dc39e1c99203ef223d1b6620061e2c0e5

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