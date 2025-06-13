import os
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
import requests

# Função para carregar as dependências do requirements.txt
def parse_requirements(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    # Remover linhas em branco e comentários
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        self.install_yfinance()
        if os.name == "nt":
            self.install_ta_lib_windows()

    def install_yfinance(self):
        """Instala o yfinance com as opções específicas no diretório 'libraries'"""
        libraries_path = os.path.join(os.getcwd(), "libraries")
        os.makedirs(libraries_path, exist_ok=True)
        print(f"Instalando yfinance em {libraries_path}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "yfinance", "--upgrade",
            "--no-cache-dir", "--target", libraries_path
        ])

    def install_ta_lib_windows(self):
        """Automatiza a instalação do TA-Lib no Windows."""
        print("Iniciando instalação do TA-Lib no Windows...")

        # URL atualizada do wheel
        talib_url = "https://github.com/cgohlke/talib-build/releases/download/v0.6.3/ta_lib-0.6.3-cp311-cp311-win_amd64.whl"
        talib_whl = os.path.basename(talib_url)

        # Caminho onde o arquivo será salvo
        libraries_path = os.path.join(os.getcwd(), "libraries")
        os.makedirs(libraries_path, exist_ok=True)
        whl_path = os.path.join(libraries_path, talib_whl)

        # Baixar o arquivo se ainda não existir
        if not os.path.isfile(whl_path):
            print(f"Baixando {talib_whl} de {talib_url}...")
            response = requests.get(talib_url, stream=True)
            if response.status_code == 200:
                with open(whl_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                print(f"Download concluído: {whl_path}")
            else:
                print(f"Erro ao baixar {talib_url}: {response.status_code}")
                return False
        else:
            print(f"O arquivo {talib_whl} já existe. Pulando o download.")

        # Instalar o .whl
        try:
            print(f"Instalando {whl_path}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", whl_path])
            print("TA-Lib instalado com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro durante a instalação do TA-Lib: {e}")
            return False

        # Remover o .whl após a instalação (opcional)
        try:
            os.remove(whl_path)
            print(f"Arquivo {whl_path} removido após a instalação.")
        except Exception as e:
            print(f"Erro ao remover o arquivo: {e}")

        return True

# Configuração do setup
requirements = parse_requirements("requirements.txt")

setup(
    name="taurus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        "yfinance": ["yfinance>=0.0.0"],
    },
    cmdclass={
        "install": CustomInstallCommand
    },
)
