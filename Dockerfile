FROM ubuntu:16.04

ARG uid=1000
ARG indy_stream=master

ARG indy_plenum_ver=1.1.143
ARG indy_anoncreds_ver=1.0.32
ARG indy_node_ver=1.1.159
ARG python3_indy_crypto_ver=0.1.6
ARG indy_crypto_ver=0.1.6

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV SHELL="/bin/bash"

# Install environment
RUN apt-get update -y && apt-get install -y \
    git \
    wget \
    python3.5 \
    python3-pip \
    python-setuptools \
    python3-nacl \
    apt-transport-https \
    ca-certificates \
    build-essential \
    pkg-config \
    cmake \
    libssl-dev \
    libsqlite3-dev \
    libsodium-dev \
    curl

RUN pip3 install -U \
    pip \
    setuptools

# Add indy user
RUN useradd -ms /bin/bash -u $uid indy

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 68DB5E88
RUN echo "deb https://repo.sovrin.org/deb xenial $indy_stream" >> /etc/apt/sources.list

RUN apt-get update -y && apt-get install -y \
    indy-plenum=${indy_plenum_ver} \
    indy-anoncreds=${indy_anoncreds_ver} \
    indy-node=${indy_node_ver} \
    python3-indy-crypto=${python3_indy_crypto_ver} \
    libindy-crypto=${indy_crypto_ver} \
    vim

USER indy
WORKDIR /home/indy

# Install rust toolchain
RUN curl -o rustup https://sh.rustup.rs
RUN chmod +x rustup
RUN ./rustup -y

# Build libindy
RUN git clone https://github.com/bcgov/indy-sdk.git
WORKDIR /home/indy/indy-sdk/libindy
RUN /home/indy/.cargo/bin/cargo build

# Move libindy to lib path
USER root
RUN mv target/debug/libindy.so /usr/lib

USER indy
WORKDIR /home/indy

# Add our startup scripts
ADD --chown=indy:indy ./scripts /home/indy/scripts

# Add our python scripts
ADD --chown=indy:indy ./connector /home/indy/von-connector