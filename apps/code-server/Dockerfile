FROM debian:bookworm@sha256:321341744acb788e251ebd374aecc1a42d60ce65da7bd4ee9207ff6be6686a62

# renovate: repository=coder/code-server
ARG CODER_VERSION="4.96.4"
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
        rsync \
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

# renovate: repository=getsops/sops
ARG SOPS_VERSION=v3.9.4
# renovate: repository=hashicorp/terraform
ARG TERRAFORM_VERSION=1.10.5
# renovate: repository=gruntwork-io/terragrunt
ARG TERRAGRUNT_VERSION=v0.72.5
# renovate: repository=databus23/helm-diff
ARG HELM_DIFF_VERSION=v3.9.14
# renovate: repository=jkroepke/helm-secrets
ARG HELM_SECRETS_VERSION=v4.6.2
# renovate: repository=helmfile/helmfile
ARG HELMFILE_VERSION=0.170.1
# renovate: repository=stern/stern
ARG STERN_VERSION=1.32.0

RUN set -ex;\
    wget -qO /tmp/stern.tar.gz "https://github.com/stern/stern/releases/download/v${STERN_VERSION}/stern_${STERN_VERSION}_linux_amd64.tar.gz";\
    cd /tmp/;tar -xvzf /tmp/stern.tar.gz; cd -;\
    mv /tmp/stern /usr/local/bin/stern;\
    wget -qO /usr/local/bin/sops https://github.com/mozilla/sops/releases/download/${SOPS_VERSION}/sops-${SOPS_VERSION}.linux.amd64;\
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
    wget -qO /tmp/helmfile.tar.gz https://github.com/helmfile/helmfile/releases/download/v${HELMFILE_VERSION}/helmfile_${HELMFILE_VERSION}_linux_amd64.tar.gz;\
    tar -xzf /tmp/helmfile.tar.gz -C /tmp/;\
    mv /tmp/helmfile /usr/local/bin/helmfile;\
    chmod a+x /usr/local/bin/helmfile;\
    wget -qO /usr/local/bin/terragrunt https://github.com/gruntwork-io/terragrunt/releases/download/${TERRAGRUNT_VERSION}/terragrunt_linux_amd64;\
    chmod a+x /usr/local/bin/terragrunt;\
    wget -qO /tmp/terraform.zip https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip;\
    unzip /tmp/terraform.zip;\
    rm /tmp/terraform.zip;\
    mv terraform /usr/local/bin/terraform;\
    rm -rf /tmp/*;\
    pip3 install pre-commit

ARG GROUP_NAME="user" \
    USER_NAME="user" \
    USER_UID="1000" \
    USER_GID="1000"

RUN set -ex;\
    groupadd --gid "${USER_GID}" "${GROUP_NAME}";\
    useradd --create-home --home-dir "/home/${USER_NAME}" --uid "${USER_UID}" --shell /usr/bin/zsh --gid "${USER_GID}" "${USER_NAME}";\
    sed -i -e 's/%sudo	ALL=(ALL:ALL) ALL/%sudo	ALL=(ALL:ALL) NOPASSWD:ALL/g' /etc/sudoers

USER $USER_NAME

RUN set -ex;\
    sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)";\
    mkdir -p "/home/${USER_NAME}/.oh-my-zsh/completions";\
    ln -s /opt/kubectx/completion/_kubectx.zsh "/home/${USER_NAME}/.oh-my-zsh/completions/_kubectx.zsh";\
    ln -s /opt/kubectx/completion/_kubens.zsh "/home/${USER_NAME}/.oh-my-zsh/completions/_kubens.zsh";\
    echo 'source <(helm completion zsh)' >> "/home/${USER_NAME}/.zshrc";\
    echo 'source <(stern --completion=zsh)' >> "/home/${USER_NAME}/.zshrc"

USER root

COPY entrypoint.sh /entrypoint.sh

CMD [ "/entrypoint.sh" ]
