FROM mcr.microsoft.com/dotnet/sdk:8.0-jammy-amd64@sha256:998629df5d88b4db5b79512a5345f59857d46bba275a37dd62129a877c517708 as build

ARG SERVER_VERSION="96e8cc2e3fd4f181d38f3cc27b5ccb0c2dca3eec"
SHELL ["/bin/bash", "-exo", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update --allow-insecure-repositories;\
    apt-get install --yes --no-install-recommends \
      openssl \
      mariadb-server \
      git;\
    apt-get clean;\
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/lib/librum-server/src/;\
    git clone https://github.com/Librum-Reader/Librum-Server.git librum-server;\
    cd librum-server;\
    git checkout "${SERVER_VERSION}";\
    dotnet restore;\
    cd src/Presentation;\
    dotnet publish  -c Release -o build  --no-restore --verbosity m;\
    cd ../..;\
    install -d /etc/librum-server/;\
    install -m660 self-hosting/librum-server.conf /etc/librum-server/;\
    mkdir -p /var/lib/librum-server/srv;\
    cp -r src/Presentation/build/* /var/lib/librum-server/srv;\
    chmod --recursive 660 /var/lib/librum-server;\
    chmod 770 /var/lib/librum-server;\
    chmod 770 /var/lib/librum-server/srv;\
    install self-hosting/run.sh -m770 /var/lib/librum-server/srv

COPY entrypoint.sh /entrypoint.sh
COPY appsettings.json /var/lib/librum-server/srv/appsettings.json

ENTRYPOINT [ "/bin/bash" ]
CMD ["/entrypoint.sh"]