FROM bitnami/wordpress:6.7.1-debian-12-r1@sha256:b59631572ece2f7ae63729087ad3e107fa31b509b213a9e7d70db044e436aab6

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