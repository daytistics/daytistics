# Basisimage verwenden
FROM ubuntu:24.04

# Umgebungsvariablen, um Eingabeaufforderungen zu vermeiden
ENV DEBIAN_FRONTEND=noninteractive

# Aktualisierung und Installation der grundlegenden Pakete
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    python3 \
    python3-pip \
    docker.io \
    docker-compose-plugin \
    software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Node.js installieren (über nvm für Flexibilität)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# UV installieren
RUN pip install uv

# Docker Compose Alias hinzufügen (optional)
RUN ln -s /usr/libexec/docker/cli-plugins/docker-compose /usr/local/bin/docker-compose

# Standardarbeitsverzeichnis setzen
WORKDIR /app

# Python und Node Versionen überprüfen (zum Debuggen)
RUN python3 --version && node --version && npm --version

# Docker Daemon starten (falls im Container nötig)
CMD ["bash"]
