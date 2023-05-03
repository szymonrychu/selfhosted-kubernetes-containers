FROM debian:bullseye-slim@sha256:f4da3f9b18fc242b739807a0fb3e77747f644f2fb3f67f4403fafce2286b431a

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


    