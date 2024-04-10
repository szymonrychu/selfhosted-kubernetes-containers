FROM debian:bullseye-slim@sha256:bc2163bce5496d87b8ca505ee5670fc089c42d32a84a45dc37656871df5686de

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