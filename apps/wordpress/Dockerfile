FROM bitnami/wordpress:6.7.1-debian-12-r9@sha256:bc4a6d440af280a373cafadfa96090595dab4a747c801f330e4c34eccb2e0da5

# renovate: repository=kevinoid/postgresql-for-wordpress
ARG POSTGRESQL_FOR_WORDPRESS_VERSION="v3.4.1"

USER root

RUN set -xe;\
    apt-get update;\
    apt-get install -y --no-install-recommends \
        git;\
    git clone https://github.com/kevinoid/postgresql-for-wordpress.git /tmp/postgresql-for-wordpress;\
    cd /tmp/postgresql-for-wordpress;\
    git fetch --tags;\
    git checkout "${POSTGRESQL_FOR_WORDPRESS_VERSION}";\
    cd /tmp;\
    mv /tmp/postgresql-for-wordpress/pg4wp /opt/bitnami/wordpress/wp-content/;\
    rm -rf /tmp/postgresql-for-wordpres;\
    cp /opt/bitnami/wordpress/wp-content/pg4wp/db.php /opt/bitnami/wordpress/wp-content/db.php;\
    apt-get remove -y --purge \
        git;\
    rm -rf \
        /tmp/* \
        /var/lib/apt/lists/* \
        /var/tmp/*

USER 1001