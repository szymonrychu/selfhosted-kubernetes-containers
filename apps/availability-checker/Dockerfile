FROM debian:bullseye-slim@sha256:ed0ed67ed2620b48b94649605db557c3aee537893a749de4b9083934cbf6d5c6

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


    