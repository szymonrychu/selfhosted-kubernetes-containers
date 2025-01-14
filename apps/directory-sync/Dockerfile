FROM debian:bullseye-slim@sha256:6344a6747740d465bff88e833e43ef881a8c4dd51950dba5b30664c93f74cbef

RUN set -xe;\
  apt-get update; \
  apt-get upgrade -y;\
  apt-get install -y \
    inotify-tools \
    rsync \
    bash \
  ;\
  apt-get clean;\
  rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh ./entrypoint.sh

ENTRYPOINT [ "/bin/bash" ]
CMD ["/entrypoint.sh"]