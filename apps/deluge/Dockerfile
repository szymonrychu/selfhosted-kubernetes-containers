FROM debian:bookworm-20230109-slim

SHELL ["/bin/sh", "-xec"]

COPY openssl.cnf /tmp

RUN apt-get update;\
    apt-get install -yq \
        openssl \
        gnupg \
        bash \
        supervisor;\
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8EED8FB4A8E6DA6DFDF0192BC5E6A5ED249AD24C;\
    echo "deb http://ppa.launchpad.net/deluge-team/stable/ubuntu focal main" >> /etc/apt/sources.list.d/deluge.list;\
    echo "deb-src http://ppa.launchpad.net/deluge-team/stable/ubuntu focal main" >> /etc/apt/sources.list.d/deluge.list;\
    apt-get update;\
    apt-get install -yq \
        deluged \
        deluge-console \
        deluge-web;\
    cat /tmp/openssl.cnf /etc/ssl/openssl.cnf > /tmp/openssl.cnf;\
    cp /tmp/openssl.cnf /etc/ssl/openssl.cnf;\
    rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD [ "/usr/bin/supervisord", "--configuration=/etc/supervisor/conf.d/supervisord.conf" ]
