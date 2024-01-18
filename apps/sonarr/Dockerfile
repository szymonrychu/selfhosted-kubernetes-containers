FROM debian:bullseye-slim@sha256:5aab272aa24713622bfac9dba239bc7488d9979b0d82d19a9dffccd99292154d

RUN set -xe;\
    apt-get update;\
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        xz-utils

RUN mkdir "${APP_DIR}/bin" && \
    curl -fsSL "https://download.sonarr.tv/v4/${SBRANCH}/${VERSION}/Sonarr.${SBRANCH}.${VERSION}.linux-musl-x64.tar.gz" | tar xzf - -C "${APP_DIR}/bin" --strip-components=1 && \
    rm -rf "${APP_DIR}/bin/Sonarr.Update" && \
    echo -e "PackageVersion=${PACKAGE_VERSION}\nPackageAuthor=[hotio](https://github.com/hotio)\nUpdateMethod=Docker\nBranch=${SBRANCH}" > "${APP_DIR}/package_info" && \
    chmod -R u=rwX,go=rX "${APP_DIR}" && \
    chmod +x "${APP_DIR}/bin/Sonarr" "${APP_DIR}/bin/ffprobe"

EXPOSE 10300

ENTRYPOINT ["/usr/bin/python3", "-m", "wyoming_faster_whisper" ]