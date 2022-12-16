FROM lscr.io/linuxserver/code-server:4.9.1

USER root

RUN set -ex;\
    apt-get update;\
    apt-get install -y --no-install-recommends \
        wget git vim curl jq gnupg zsh sed unzip

RUN set -ex;\
    adduser abc sudo;\
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN set -ex;\
    wget -qO /usr/local/bin/stern https://github.com/wercker/stern/releases/download/1.11.0/stern_linux_amd64;\
    chmod +x /usr/local/bin/stern;\
    wget -qO /usr/local/bin/sops https://github.com/mozilla/sops/releases/download/v3.7.3/sops-v3.7.3.linux.amd64;\
    chmod a+x /usr/local/bin/sops;\
    wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64;\
    chmod a+x /usr/local/bin/yq;\
    wget -qO /usr/local/bin/kubectl "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl";\
    chmod a+x /usr/local/bin/kubectl;\
    git clone --depth 1 https://github.com/ahmetb/kubectx /opt/kubectx;\
    ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx;\
    ln -s /opt/kubectx/kubens /usr/local/bin/kubens;\
    curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash;\
    helm plugin install --version v3.6.0 https://github.com/databus23/helm-diff;\
    helm plugin install --version v3.15.0 https://github.com/jkroepke/helm-secrets;\
    curl -s https://api.github.com/repos/roboll/helmfile/releases/latest |  jq -r '.assets[] | .browser_download_url' | grep 'linux_amd64' | xargs wget -qO /usr/local/bin/helmfile;\
    chmod a+x /usr/local/bin/helmfile;\
    wget -qO /usr/local/bin/terragrunt https://github.com/gruntwork-io/terragrunt/releases/download/v0.37.4/terragrunt_linux_amd64;\
    chmod a+x /usr/local/bin/terragrunt;\
    wget -qO /tmp/terraform.zip https://releases.hashicorp.com/terraform/1.2.2/terraform_1.2.2_linux_amd64.zip;\
    unzip /tmp/terraform.zip;\
    rm /tmp/terraform.zip;\
    mv terraform /usr/local/bin/terraform;\
    chown -R abc /config

USER abc

RUN set -xe;\
    sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)";\
    mkdir -p /config/.oh-my-zsh/completions;\
    ln -s /opt/kubectx/completion/_kubectx.zsh /config/.oh-my-zsh/completions/_kubectx.zsh;\
    ln -s /opt/kubectx/completion/_kubens.zsh /config/.oh-my-zsh/completions/_kubens.zsh;\
    echo 'source <(helm completion zsh)' >> /config/.zshrc;\
    wget -qO /config/.oh-my-zsh/completions/_helmfile.zsh https://raw.githubusercontent.com/roboll/helmfile/master/autocomplete/helmfile_zsh_autocomplete;\
    echo 'source <(stern --completion=zsh)' >> /config/.zshrc


USER root

# ENTRYPOINT [ "/bin/bash" ]

# CMD [ "-c", "HOME='/config' /app/code-server/bin/code-server --bind-addr=0.0.0.0:8443 --user-data-dir=/config/.config/data --extensions-dir=/config/.config/extensions --disable-telemetry --auth=${AUTH:-none} --proxy-domain=${PROXY_DOMAIN} /config"]




# RUN unset NB_USER