FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
ARG BUILD_PACKAGES=wget apt-transport-https software-properties-common
RUN apt update && \
    apt upgrade -y && \
    apt install -y cifs-utils rsync locales $BUILD_PACKAGES && \
    . /etc/os-release && \
    wget -q https://packages.microsoft.com/config/ubuntu/$VERSION_ID/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb && \
    apt update && \
    apt install -y powershell && \
    apt purge -y --auto-remove $BUILD_PACKAGES && \
    rm -r /var/lib/apt/lists/*
ADD _ /
RUN locale-gen
ENV LC_ALL en_US.UTF-8
ENTRYPOINT ["/init.sh"]
