FROM debian:bookworm

# renovate: repository=https://github.com/coder/code-server
ARG CODER_VERSION="4.19.1"

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
        docker \
    ;\
    curl -fLo /tmp/coder.deb "https://github.com/coder/code-server/releases/download/v${CODER_VERSION}/code-server_${CODER_VERSION}_amd64.deb";\
    apt-get install -y /tmp/coder.deb;\
    rm -rf /var/lib/apt/lists/* /tmp/coder.deb;\
    mkdir -p /etc/codeserver.d/

ARG STERN_VERSION="1.22.0"
ARG SOPS_VERSION="1.22.0"
ARG SOPS_VERSION="3.7.3"
ARG HELM_DIFF_VERSION="3.6.0"
ARG HELM_SECRETS_VERSION="3.15.0"
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
    helm plugin install --version "v${HELM_DIFF_VERSION}" https://github.com/databus23/helm-diff;\
    helm plugin install --version "v${HELM_SECRETS_VERSION}" https://github.com/jkroepke/helm-secrets;\
    curl -s https://api.github.com/repos/roboll/helmfile/releases/latest |  jq -r '.assets[] | .browser_download_url' | grep 'linux_amd64' | xargs wget -qO /usr/local/bin/helmfile;\
    chmod a+x /usr/local/bin/helmfile;\
    wget -qO /tmp/terraform.zip "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip";\
    unzip /tmp/terraform.zip;\
    rm /tmp/terraform.zip;\
    mv terraform /usr/local/bin/terraform;\
    rm -rf /tmp/*

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
