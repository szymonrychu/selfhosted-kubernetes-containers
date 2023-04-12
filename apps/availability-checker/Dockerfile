FROM debian:bullseye-slim@sha256:9404b05bd09b57c76eccc0c5505b3c88b5feccac808d9b193a4fbac87bb44745

COPY script/requirements.txt /tmp/requirements.txt

RUN set -xe;\
    apt-get update;\
    apt-get install -y \
        python3-pip;\
    apt-get clean;\
    rm -rf /var/lib/apt/lists/*;\
    mkdir /checker;\
    pip3 install -r /tmp/requirements.txt

WORKDIR /checker

COPY script/cmd.py /checker/cmd.py

ENTRYPOINT ["/checker/cmd.py"]


    