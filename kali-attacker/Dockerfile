# kali/Dockerfile
ARG BASE_IMAGE=kalilinux/kali-rolling
FROM ${BASE_IMAGE}

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    nmap \
    hydra \
    medusa \
    metasploit-framework \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    python3-numpy && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
7
# path to rockyou.txt : /usr/share/wordlists/rockyou.txt
COPY rockyou-short.txt /usr/share/wordlists/rockyou.txt

# set up python with libraries
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir \
        pandas \

    apt-get update && \
    apt-get install -y --no-install-recommends \
        chromium-driver \
        chromium && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root
CMD ["/bin/bash"]
