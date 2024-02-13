FROM debian:bookworm@sha256:4482958b4461ff7d9fabc24b3a9ab1e9a2c85ece07b2db1840c7cbc01d053e90

# renovate: repository=https://github.com/coder/code-server
ARG CODER_VERSION="4.19.1"
ENV PIP_BREAK_SYSTEM_PACKAGES="1"

RUN set -ex;\
    apt-get update;\
    apt-get install -y --no-install-recommends \
        ca-certificates \
        wget \
        git \
        vim \
        curl \
        jq \
        gnupg \
        zsh \
        sed \
        unzip \
        sudo \
        python3-pip \
        openssh-client \
    ;\
    install -m 0755 -d /etc/apt/keyrings;\
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg;\
    chmod a+r /etc/apt/keyrings/docker.gpg;\
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list;\
    apt-get update;\
    apt-get install -y \
        docker-ce \
        docker-ce-cli \
        containerd.io \
        docker-buildx-plugin \
        docker-compose-plugin \
    ;\
    curl -fLo /tmp/coder.deb "https://github.com/coder/code-server/releases/download/v${CODER_VERSION}/code-server_${CODER_VERSION}_amd64.deb";\
    apt-get install -y /tmp/coder.deb;\
    rm -rf /var/lib/apt/lists/* /tmp/coder.deb;\
    mkdir -p /etc/codeserver.d/

ARG STERN_VERSION="1.22.0"
ARG SOPS_VERSION="1.22.0"
ARG SOPS_VERSION="3.7.3"
ARG TERRAFORM_VERSION="1.2.2"

RUN wget -qO /tmp/stern.tar.gz "https://github.com/stern/stern/releases/download/v${STERN_VERSION}/stern_${STERN_VERSION}_linux_amd64.tar.gz";\
    cd /tmp/;tar -xvzf /tmp/stern.tar.gz; cd -;\
    mv /tmp/stern /usr/local/bin/stern;\
    wget -qO /usr/local/bin/sops "https://github.com/mozilla/sops/releases/download/v${SOPS_VERSION}/sops-v${SOPS_VERSION}.linux.amd64";\
    chmod a+x /usr/local/bin/sops;\
    wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64;\
    chmod a+x /usr/local/bin/yq;\
    wget -qO /usr/local/bin/kubectl "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl";\
    chmod a+x /usr/local/bin/kubectl;\
    git clone --depth 1 https://github.com/ahmetb/kubectx /opt/kubectx;\
    ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx;\
    ln -s /opt/kubectx/kubens /usr/local/bin/kubens;\
    curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash;\
    helm plugin install https://github.com/databus23/helm-diff;\
    helm plugin install https://github.com/jkroepke/helm-secrets;\
    curl -s https://api.github.com/repos/helmfile/helmfile/releases/latest |  jq -r '.assets[] | .browser_download_url' | grep 'linux_amd64' | xargs wget -qO /tmp/helmfile.tar.gz;\
    cd /tmp/;tar -xvzf /tmp/helmfile.tar.gz; cd -;\
    mv /tmp/helmfile /usr/local/bin/helmfile;\
    chmod a+x /usr/local/bin/helmfile;\
    wget -qO /tmp/terraform.zip "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip";\
    unzip /tmp/terraform.zip;\
    rm /tmp/terraform.zip;\
    mv terraform /usr/local/bin/terraform;\
    rm -rf /tmp/*;\
    pip3 install pre-commit


RUN set -xe;\
    sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)";\
    mkdir -p /root/.oh-my-zsh/completions;\
    ln -s /opt/kubectx/completion/_kubectx.zsh /root/.oh-my-zsh/completions/_kubectx.zsh;\
    ln -s /opt/kubectx/completion/_kubens.zsh /root/.oh-my-zsh/completions/_kubens.zsh;\
    echo 'source <(helm completion zsh)' >> /root/.zshrc;\
    wget -qO /root/.oh-my-zsh/completions/_helmfile.zsh https://raw.githubusercontent.com/roboll/helmfile/master/autocomplete/helmfile_zsh_autocomplete;\
    echo 'source <(stern --completion=zsh)' >> /root/.zshrc

COPY entrypoint.sh /entrypoint.sh

CMD [ "/entrypoint.sh" ]
