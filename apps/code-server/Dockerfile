FROM codercom/code-server:4.19.0@sha256:d485b27ce0eeb32bc09beb512825eb5ad2d5ad09202e64e0bd4ca27b1555062f

USER root

RUN set -ex;\
    apt-get update;\
    apt-get install -y --no-install-recommends \
        wget git vim curl jq gnupg zsh sed unzip

RUN set -ex;\
    wget -qO /tmp/stern.tar.gz https://github.com/stern/stern/releases/download/v1.22.0/stern_1.22.0_linux_amd64.tar.gz;\
    cd /tmp/;tar -xvzf /tmp/stern.tar.gz; cd -;\
    mv /tmp/stern /usr/local/bin/stern;\
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
    rm -rf /tmp/*;\
    chown -R coder /home/coder

USER coder

RUN set -xe;\
    sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)";\
    mkdir -p /home/coder/.oh-my-zsh/completions;\
    ln -s /opt/kubectx/completion/_kubectx.zsh /home/coder/.oh-my-zsh/completions/_kubectx.zsh;\
    ln -s /opt/kubectx/completion/_kubens.zsh /home/coder/.oh-my-zsh/completions/_kubens.zsh;\
    echo 'source <(helm completion zsh)' >> /home/coder/.zshrc;\
    wget -qO /home/coder/.oh-my-zsh/completions/_helmfile.zsh https://raw.githubusercontent.com/roboll/helmfile/master/autocomplete/helmfile_zsh_autocomplete;\
    echo 'source <(stern --completion=zsh)' >> /home/coder/.zshrc

