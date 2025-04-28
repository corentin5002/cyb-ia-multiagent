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

# path to rockyou.txt : /usr/share/wordlists/rockyou.txt
COPY rockyou-short.txt /usr/share/wordlists/rockyou.txt
WORKDIR /root
CMD ["/bin/bash"]
