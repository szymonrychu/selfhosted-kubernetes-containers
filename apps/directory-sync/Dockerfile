FROM debian:bullseye-slim@sha256:3f9e53602537cc817d96f0ebb131a39bdb16fa8b422137659a9a597e7e3853c1

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