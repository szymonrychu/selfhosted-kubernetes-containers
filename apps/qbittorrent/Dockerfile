FROM alpine:3.15@sha256:19b4bcc4f60e99dd5ebdca0cbce22c503bbcff197549d7e19dab4f22254dc864 as qbittorrent-build

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

FROM alpine:3.15@sha256:19b4bcc4f60e99dd5ebdca0cbce22c503bbcff197549d7e19dab4f22254dc864

COPY --from=qbittorrent-build /usr/local/bin/qbittorrent-nox /usr/bin/qbittorrent-nox

# renovate: repository=https://github.com/wdaan/vuetorrent.git
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