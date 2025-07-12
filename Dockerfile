FROM python:3.11-slim

WORKDIR /code

# 1. Instalar dependências de sistema
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
    && rm -rf /var/lib/apt/lists/*

# 2. Instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 3. Instalar TA-Lib C nativo
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xvzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr/local
make
make install
ldconfig
cd ..
rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# 4. Instalat ta-lib (WIP)
# RUN pip install TA-Lib

# 6. Copiar código
COPY . .

EXPOSE 8000

CMD ["python", "market-analyzer/manage.py", "runserver", "0.0.0.0:8000"]
