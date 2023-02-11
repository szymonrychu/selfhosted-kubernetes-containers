FROM debian:bookworm-20230109-slim

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