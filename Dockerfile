FROM python:3.11-slim

# Instalar pacotes do sistema necessários para TA-Lib e outras dependências
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    gcc \
    make \
    libtool \
    autoconf \
    pkg-config \
    libffi-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    netcat \
    libcurl4-openssl-dev \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar TA-Lib (C library)
WORKDIR /tmp
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib && ./configure --prefix=/usr && make && make install \
    && ldconfig \
    && rm -rf /tmp/*

# Preparar a pasta do projeto
WORKDIR /code

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do projeto
COPY . .

EXPOSE 8000
