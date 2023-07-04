FROM debian:bullseye-slim@sha256:c73af22108a0c8d6aaeeb5a3162618df20aa9bc9f21805594228bb4df0d5ccda
ARG RUNNER_VERSION="2.300.0"

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
    wget -qO /usr/local/bin/sops https://github.com/mozilla/sops/releases/download/v3.7.3/sops-v3.7.3.linux.amd64;\
    chmod a+x /usr/local/bin/sops;\
    wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64;\
    chmod a+x /usr/local/bin/yq;\
    wget -qO /usr/local/bin/kubectl "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl";\
    chmod a+x /usr/local/bin/kubectl;\
    curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash;\
    curl -s https://api.github.com/repos/roboll/helmfile/releases/latest |  jq -r '.assets[] | .browser_download_url' | grep 'linux_amd64' | xargs wget -qO /usr/local/bin/helmfile;\
    chmod a+x /usr/local/bin/helmfile;\
    wget -qO /usr/local/bin/terragrunt https://github.com/gruntwork-io/terragrunt/releases/download/v0.37.4/terragrunt_linux_amd64;\
    chmod a+x /usr/local/bin/terragrunt;\
    wget -qO /tmp/terraform.zip https://releases.hashicorp.com/terraform/1.2.2/terraform_1.2.2_linux_amd64.zip;\
    unzip /tmp/terraform.zip;\
    rm /tmp/terraform.zip;\
    mv terraform /usr/local/bin/terraform

USER github
WORKDIR /home/github

COPY --chown=github:github entrypoint.sh ./entrypoint.sh

RUN set -xe;\
    helm plugin install --version v3.6.0 https://github.com/databus23/helm-diff;\
    helm plugin install --version v3.15.0 https://github.com/jkroepke/helm-secrets;\
    curl -O -L https://github.com/actions/runner/releases/download/v$RUNNER_VERSION/actions-runner-linux-x64-$RUNNER_VERSION.tar.gz;\
    tar xzf ./actions-runner-linux-x64-$RUNNER_VERSION.tar.gz;\
    sudo ./bin/installdependencies.sh;\
    sudo chmod u+x ./entrypoint.sh

ENTRYPOINT [ "/bin/bash" ]
CMD ["/home/github/entrypoint.sh"]