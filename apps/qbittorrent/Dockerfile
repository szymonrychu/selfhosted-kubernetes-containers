FROM alpine:3.20@sha256:0a4eaa0eecf5f8c050e5bba433f58c052be7587ee8af3e8b3910ef9ab5fbe9f5 as qbittorrent-build

# renovate: repository=qbittorrent/qBittorrent.git
ARG QBITTORRENT_VERSION=release-4.6.1

# Install dependencies
RUN set -ex;\
    apk add --no-cache \
        git \
        qt6-qttools-dev \
        g++ \
        libtorrent-rasterbar-dev \
        cmake \
        boost-dev \
        ninja;\
    cd /tmp;\
    git clone --recurse-submodules https://github.com/qbittorrent/qBittorrent.git --branch "${QBITTORRENT_VERSION}" --depth 1;\
    cd ./qBittorrent;\
    cmake -Wno-dev -G Ninja -B build-nox \
        -D CMAKE_BUILD_TYPE="release" \
        -D STACKTRACE=OFF \
        -D QT6=ON \
        -D GUI=OFF;\
    cmake --build build-nox -j$(nproc);\
    cmake --install build-nox

FROM alpine:3.20@sha256:0a4eaa0eecf5f8c050e5bba433f58c052be7587ee8af3e8b3910ef9ab5fbe9f5

COPY --from=qbittorrent-build /usr/local/bin/qbittorrent-nox /usr/bin/qbittorrent-nox

# renovate: repository=wdaan/vuetorrent.git
ARG VUETORRENT_VERSION=2.2.0

RUN set -ex;\
    mkdir -p /config/qBittorrent /downloads;\
    apk add --no-cache \
        qt6-qtbase \
        libtorrent-rasterbar \
        curl;\
    curl -fsSL "https://github.com/wdaan/vuetorrent/releases/download/v${VUETORRENT_VERSION}/vuetorrent.zip" > "/tmp/vuetorrent.zip";\
    unzip "/tmp/vuetorrent.zip" -d /themes;\
    rm "/tmp/vuetorrent.zip";\
    chmod -R u=rwX,go=rX /themes/vuetorrent

COPY qBittorrent.conf /config/qBittorrent/qBittorrent.conf

env HOME="/config" \
    XDG_CONFIG_HOME="/config" \
    XDG_DATA_HOME="/config"

CMD ["qbittorrent-nox", "--webui-port=8080"]