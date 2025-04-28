# Dockerfile.defender
FROM ubuntu:22.04

# Suricata + Python sciences des données
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        suricata iptables python3-pip && \
    pip3 install --no-cache-dir scikit-learn joblib pandas numpy && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copie (optionnelle) de ton script de défense IA
# COPY agent_defender/ /opt/agent
WORKDIR /var/log/suricata

# Suricata se lance en démon (-D) et l’IA peut être appelée par entrypoint
CMD ["suricata", "-D", "-i", "eth0"]