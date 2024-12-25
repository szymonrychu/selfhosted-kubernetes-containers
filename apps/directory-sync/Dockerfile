FROM debian:bullseye-slim@sha256:b0c91cc181796d34c53f7ea106fbcddaf87f3e601cc371af6a24a019a489c980

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