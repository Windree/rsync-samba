FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y cifs-utils rsync locales && \
    rm -r /var/lib/apt/lists/*
ADD _ /
RUN locale-gen
ENV LC_ALL en_US.UTF-8
ENTRYPOINT ["/init.sh"]
