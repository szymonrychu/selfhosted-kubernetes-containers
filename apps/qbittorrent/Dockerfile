FROM alpine:3.15 as qbittorrent-build

# renovate: repository=https://github.com/qbittorrent/qBittorrent.git
ARG QBITTORRENT_VERSION=release-4.6.1

# Install dependencies
RUN set -ex;\
    apk add --no-cache \
        git \
        qt6-qttools-dev \
        g++ \
        libtorrent-rasterbar-dev \
        cmake \
        libexecinfo-dev \
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

FROM alpine:3.15

COPY --from=qbittorrent-build /usr/local/bin/qbittorrent-nox /usr/bin/qbittorrent-nox

RUN set -ex;\
    mkdir -p /config /downloads;\
    apk add --no-cache \
        qt6-qtbase \
        libtorrent-rasterbar

COPY entrypoint.sh /entrypoint.sh

EXPOSE 6881 6881/udp 8080

USER qbittorrent

env HOME="/config" \
    XDG_CONFIG_HOME="/config" \
    XDG_DATA_HOME="/config"

CMD ["/entrypoint.sh"]