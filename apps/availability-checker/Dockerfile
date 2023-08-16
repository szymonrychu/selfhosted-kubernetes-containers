FROM debian:bullseye-slim@sha256:59a751b3f0aaa097b42ebc19a0c429e80cf4d6b861fbe1453b9948aa5fa41200

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


    