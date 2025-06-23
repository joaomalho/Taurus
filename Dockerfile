FROM python:3.11-slim

WORKDIR /code

# Instala dependências do sistema e compila a lib TA-Lib para /usr/local
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    make \
    wget \
    tar \
    build-essential \
    && wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xvzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib && ./configure --prefix=/usr/local && make && make install \
    && rm -rf /var/lib/apt/lists/* ta-lib ta-lib-0.4.0-src.tar.gz

# Garante que o linker encontra a biblioteca compilada
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
RUN echo "/usr/local/lib" > /etc/ld.so.conf.d/ta-lib.conf && ldconfig

# Instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

EXPOSE 8000

CMD ["python", "market-analyzer/manage.py", "runserver", "0.0.0.0:8000"]
