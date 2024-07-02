FROM debian:bullseye-slim@sha256:34b63f55a4b193ad03c5ddb4b3f8546c797763ed708f0df5309ecb9507d15179

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