FROM kalilinux/kali-rolling

# Install system dependencies
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
    wget \
    curl && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Setup virtual environment
RUN python3 -m venv /opt/venv

# Install Python packages
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir \
        numpy \
        gym==0.26.2

# Copy your project files
COPY rockyou-short.txt /usr/share/wordlists/rockyou.txt
COPY main.py /root/main.py
COPY attack_functions.py /root/attack_functions.py
COPY cyberattackenv.py /root/cyberattackenv.py
COPY q_table.npy /root/q_table.npy

ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /root

# Default command
CMD ["/bin/bash"]
