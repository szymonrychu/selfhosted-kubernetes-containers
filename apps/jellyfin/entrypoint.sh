#!/bin/bash
mkdir -p \
    /config/{log,data/transcodes,cache} \
    /data \
    /transcode

export \
    JELLYFIN_DATA_DIR="/config/data" \
    JELLYFIN_CONFIG_DIR="/config" \
    JELLYFIN_LOG_DIR="/config/log" \
    JELLYFIN_CACHE_DIR="/config/cache" \
    JELLYFIN_WEB_DIR="/usr/share/jellyfin/web"

/usr/bin/jellyfin --ffmpeg=/usr/lib/jellyfin-ffmpeg/ffmpeg
