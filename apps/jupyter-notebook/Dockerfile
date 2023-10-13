FROM ubuntu:jammy@sha256:2b7412e6465c3c7fc5bb21d3e6f1917c167358449fecac8176c6e496e5c1f05f
ARG NB_USER="jupyter_notebook"
ARG NB_UID="1000"
ARG NB_GID="1000"
ARG PYTHON_VERSION=3.11

SHELL ["/bin/bash", "-exo", "pipefail", "-c"]

USER root

ENV DEBIAN_FRONTEND=noninteractive \
    CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    JUPYTER_PORT=8888

ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

RUN ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime;\
    apt-get update --yes;\
    apt-get install --yes --no-install-recommends \
        tzdata \
        python3-pip \
        dirmngr \
        gnupg2 \
        bzip2 \
        ca-certificates \
        locales \
        pandoc \
        sudo \
        tini \
        fonts-liberation \
        run-one \
        wget;\
    apt-get clean;\
    rm -rf /var/lib/apt/lists/*;\
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen;\
    locale-gen;\
    sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc;\
    echo 'eval "$(command conda shell.bash hook 2> /dev/null)"' >> /etc/skel/.bashrc;\
    echo "auth requisite pam_deny.so" >> /etc/pam.d/su;\
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers;\
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers;\
    useradd --no-log-init --create-home --shell /bin/bash --uid "${NB_UID}" --no-user-group "${NB_USER}";\
    mkdir -p "${CONDA_DIR}";\
    chown "${NB_USER}:${NB_GID}" "${CONDA_DIR}";\
    chmod g+w /etc/passwd;\
    mkdir /usr/local/bin/start-notebook.d;\
    mkdir /usr/local/bin/before-notebook.d

COPY run-hooks.sh start.sh start-notebook.sh start-singleuser.sh /usr/local/bin/
COPY jupyter_server_config.py docker_healthcheck.py /etc/jupyter/

RUN chmod a+x /usr/local/bin/run-hooks.sh \
        /usr/local/bin/start.sh \
        /usr/local/bin/start-notebook.sh \
        /usr/local/bin/start-singleuser.sh

USER ${NB_UID}

RUN mkdir "/home/${NB_USER}/work"

COPY --chown="${NB_UID}:${NB_GID}" initial-condarc "${CONDA_DIR}/.condarc"

RUN cd /tmp ;\
    arch=$(uname -m) ;\
    if [ "${arch}" = "x86_64" ]; then \
        # Should be simpler, see <https://github.com/mamba-org/mamba/issues/1437>
        arch="64"; \
    fi ;\
    wget --progress=dot:giga -O /tmp/micromamba.tar.bz2 \
        "https://micromamba.snakepit.net/api/micromamba/linux-${arch}/latest" ;\
    tar -xvjf /tmp/micromamba.tar.bz2 --strip-components=1 bin/micromamba ;\
    rm /tmp/micromamba.tar.bz2 ;\
    PYTHON_SPECIFIER="python=${PYTHON_VERSION}" ;\
    if [[ "${PYTHON_VERSION}" == "default" ]]; then PYTHON_SPECIFIER="python"; fi ;\
    # Install the packages
    ./micromamba install \
        --root-prefix="${CONDA_DIR}" \
        --prefix="${CONDA_DIR}" \
        --yes \
        "${PYTHON_SPECIFIER}" \
        'mamba' \
        'jupyter_core' ;\
    rm micromamba ;\
    # Pin major.minor version of python
    mamba list python | grep '^python ' | tr -s ' ' | cut -d ' ' -f 1,2 >> "${CONDA_DIR}/conda-meta/pinned" ;\
    mamba install --yes \
        'jupyterlab' \
        'notebook' \
        'jupyterhub' \
        'nbclassic' ;\
    jupyter server --generate-config ;\
    mamba clean --all -f -y ;\
    jupyter lab clean ;\
    rm -rf "/home/${NB_USER}/.cache/yarn";\
    mamba clean --all -f -y
    

EXPOSE $JUPYTER_PORT

HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
    CMD /etc/jupyter/docker_healthcheck.py || exit 1

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-notebook.sh"]

ENV ROS_DISTRO noetic

USER root

RUN pip3 install jupyter_contrib_nbextensions;\
    jupyter contrib nbextension install;\
    jupyter nbextension enable varInspector/main;\
    echo "deb http://packages.ros.org/ros/ubuntu focal main" > /etc/apt/sources.list.d/ros1-latest.list;\
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654;\
    apt-get update --yes;\
    apt-get install --yes \
        ros-noetic-ros-core=1.5.0-1* \
        git \
        curl \
        vim;\
    apt-get clean;\
    rm -rf /var/lib/apt/lists/*;\
    pip3 install jupyter bqplot pyyaml ipywidgets;\
    jupyter nbextension enable --py --sys-prefix ipywidgets;\
    pip3 install jupyros;\
    jupyter nbextension enable --py --sys-prefix jupyros;\
    jupyter labextension install jupyter-ros

USER ${NB_UID}
WORKDIR "${HOME}"