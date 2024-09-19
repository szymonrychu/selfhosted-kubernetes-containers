FROM debian:bullseye-slim@sha256:b257e5e831aa9949737638f6d323cd563347b2a5571d98b9b15eef0c7cd80b68

# renovate: image=ghcr.io/actions/actions-runner
ARG RUNNER_VERSION="2.319.1"
# renovate: repository=getsops/sops
ARG SOPS_VERSION=v3.9.0
# renovate: repository=hashicorp/terraform
ARG TERRAFORM_VERSION=1.9.6
# renovate: repository=gruntwork-io/terragrunt
ARG TERRAGRUNT_VERSION=v0.67.9
# renovate: repository=databus23/helm-diff
ARG HELM_DIFF_VERSION=v3.9.10
# renovate: repository=jkroepke/helm-secrets
ARG HELM_SECRETS_VERSION=v4.6.1
# renovate: repository=helmfile/helmfile
ARG HELMFILE_VERSION=0.168.0

RUN set -xe;\
    apt-get update; \
    apt-get upgrade -y;\
    apt-get install -y \
        curl \
        wget \
        sudo \
        git \
        jq \
        unzip \
        tar \
        gnupg2 \
        apt-transport-https \
        ca-certificates \
        python3-pip;\
    apt-get clean;\
    rm -rf /var/lib/apt/lists/*;\
    pip3 install ruamel.yaml requests ansible;\
    useradd -m github;\
    usermod -aG sudo github;\
    echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers;\
    wget -qO /usr/local/bin/sops https://github.com/mozilla/sops/releases/download/${SOPS_VERSION}/sops-${SOPS_VERSION}.linux.amd64;\
    chmod a+x /usr/local/bin/sops;\
    wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64;\
    chmod a+x /usr/local/bin/yq;\
    wget -qO /usr/local/bin/kubectl "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl";\
    chmod a+x /usr/local/bin/kubectl;\
    curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash;\
    wget -qO /tmp/helmfile.tar.gz https://github.com/helmfile/helmfile/releases/download/v${HELMFILE_VERSION}/helmfile_${HELMFILE_VERSION}_linux_amd64.tar.gz;\
    tar -xzf /tmp/helmfile.tar.gz -C /tmp/;\
    mv /tmp/helmfile /usr/local/bin/helmfile;\
    wget -qO /usr/local/bin/terragrunt https://github.com/gruntwork-io/terragrunt/releases/download/${TERRAGRUNT_VERSION}/terragrunt_linux_amd64;\
    chmod a+x /usr/local/bin/terragrunt;\
    wget -qO /tmp/terraform.zip https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip;\
    unzip /tmp/terraform.zip;\
    rm /tmp/terraform.zip;\
    mv terraform /usr/local/bin/terraform;\
    rm -rf /tmp/*

USER github
WORKDIR /home/github

COPY --chown=github:github entrypoint.sh ./entrypoint.sh

RUN set -xe;\
    helm plugin install --version ${HELM_DIFF_VERSION} https://github.com/databus23/helm-diff;\
    helm plugin install --version ${HELM_SECRETS_VERSION} https://github.com/jkroepke/helm-secrets;\
    curl -O -L https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz;\
    tar xzf ./actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz;\
    sudo ./bin/installdependencies.sh;\
    sudo chmod u+x ./entrypoint.sh

ENTRYPOINT [ "/bin/bash" ]
CMD ["/home/github/entrypoint.sh"]