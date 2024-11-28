FROM alpine:3.20.3@sha256:1e42bbe2508154c9126d48c2b8a75420c3544343bf86fd041fb7527e017a4b4a

# renovate: nkelemen18/koreui
ARG KOREUI_VERSION="22.0.0"
# renovate: aerogear/keycloak-metrics-spi
ARG METRICS_SPI_VERSION="7.0.0"

RUN set -ex;\
    mkdir -p /keycloak-providers/;\
    wget -qO /keycloak-providers/koreui.jar "https://github.com/nkelemen18/koreui/releases/download/${KOREUI_VERSION}/koreui-${KOREUI_VERSION}.jar";\
    wget -qO /keycloak-providers/metrics-spi.jar "https://github.com/aerogear/keycloak-metrics-spi/releases/download/${METRICS_SPI_VERSION}/keycloak-metrics-spi-${METRICS_SPI_VERSION}.jar"

