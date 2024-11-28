FROM debian:bullseye-slim@sha256:60a596681410bd31a48e5975806a24cd78328f3fd6b9ee5bc64dca6d46a51f29

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