FROM ubuntu:24.04

USER root

SHELL ["/bin/bash", "-c"]

#################################################
# DOCKERIFLE ARGs
#################################################
ARG PYTHON_VERSION=3.14.0
ARG PYTHON_MAJOR=3

ARG TERRAFORM_VERSION="1.13.3"

#################################################
# UBUNTU PACKAGE REPOSITORIES
#################################################
RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y \
  apt-utils \
  curl \
  lsb-release \
  software-properties-common \
  sudo

### Microsoft
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
  curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | tee /etc/apt/sources.list.d/microsoft-prod.list

# ### Python
# RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -cs)-proposed main" | tee -a /etc/apt/sources.list && \
#   echo "# deb-src http://archive.ubuntu.com/ubuntu/ $(lsb_release -cs)-proposed main" | tee -a /etc/apt/sources.list

#################################################
# OS SYSTEM PACKAGES/LIBRARIES
#################################################
RUN apt-get update -y && apt-get upgrade -y && \
DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y --no-install-recommends \
    apache2-utils \
    apt-transport-https \
    ca-certificates \
    curl \
    dnsmasq \
    dnsutils \
    dos2unix \
    git \
    gnupg \
    gzip \
    hostname \
    jq \
    libatomic1 \
    libcurl4-openssl-dev \
    openssl \
    shellcheck \
    tar \
    tree \
    unzip \
    uuid-runtime \
    vim \
    wget \
    zip

#################################################
# PYTHON
#################################################
# RUN cp /etc/apt/sources.list /etc/apt/sources.list~ && \
#   sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list && \
#   DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y \
#     gdebi-core && \
#   apt-get update -y && \
#   DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get build-dep python3 -y && \
#   DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y \
#     libffi-dev \
#     libgdbm-dev \
#     libsqlite3-dev \
#     libssl-dev \
#     zlib1g-dev \
#     libbz2-dev && \
#   sed -Ei 's/deb-src /# deb-src /' /etc/apt/sources.list

RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y \
    gdebi-core \
    build-essential \
    libffi-dev \
    libgdbm-dev \
    libsqlite3-dev \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libncursesw5-dev \
    libgdbm-compat-dev \
    liblzma-dev \
    tk-dev \
    uuid-dev

RUN curl -O https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xvzf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make -j16 && \
    make install && \
    ln -sfn /usr/local/bin/python3 /usr/local/bin/python && \
    ln -sfn /usr/local/bin/pip3 /usr/local/bin/pip && \
    cd / && rm -rf Python-${PYTHON_VERSION}.tgz Python-${PYTHON_VERSION}

#################################################
# AZURE CLI
#################################################
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

#################################################
# TERRAFORM
#################################################
RUN curl -sL "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" -o terraform.zip && \
    unzip -d /usr/local/bin/ terraform.zip && \
    chmod +x /usr/local/bin/terraform && \
    rm -rf terraform.zip && \
    apt-get install -f