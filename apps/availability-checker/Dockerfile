FROM debian:bullseye-slim@sha256:d5dd14ffead88f6e0cdc4d9b5e8ce7b748e5e0ee9294aa0e566f39f2e85bc55e

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


    