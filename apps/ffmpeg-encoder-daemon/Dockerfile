FROM debian:bookworm-20230109-slim@sha256:9b8b22f153dc2099e609f56ec3790e5952f89d3e187e42686c0b95ad1f378d01

SHELL ["/bin/sh", "-xec"]

RUN apt-get update;\
    apt-get install -y \
        ffmpeg \
        python3-pip\
        libmagic1\
    ;\
    mkdir /ffmpeg-daemon;\
    mkdir /workdir

WORKDIR /workdir

COPY ./requirements.txt /ffmpeg-daemon/

RUN pip3 install -r /ffmpeg-daemon/requirements.txt;\
    rm /ffmpeg-daemon/requirements.txt

COPY ./src /ffmpeg-daemon/

CMD ["/usr/bin/env", "python3", "/ffmpeg-daemon/cmd.py"]