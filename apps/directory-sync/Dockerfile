FROM debian:bullseye-slim@sha256:610b4c7ad241e66f6e2f9791e3abdf0cc107a69238ab21bf9b4695d51fd6366a

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