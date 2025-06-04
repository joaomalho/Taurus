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
        self.install_requirements_to_libraries()
        install.run(self)
        self.install_yfinance()
        if os.name == "nt":
            self.install_ta_lib_windows()

    def install_yfinance(self):
        """Instala o yfinance com os parâmetros específicos no diretório libraries"""
        libraries_path = os.path.join(os.getcwd(), "libraries")
        print(f"Instalando yfinance com as opções --upgrade --no-cache-dir em {libraries_path}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "yfinance", "--upgrade",
            "--no-cache-dir", "--target", libraries_path
        ])

    def install_ta_lib_windows(self):
        """Automatiza a instalação do TA-Lib no Windows."""
        print("Iniciando instalação do TA-Lib no Windows...")

        # URL do arquivo .whl (atualize conforme necessário)
        talib_url = "https://github.com/cgohlke/talib-build/releases/download/v0.5.1/TA_Lib-0.5.1-cp311-cp311-win_amd64.whl"
        talib_whl = talib_url.split("/")[-1]  # Nome do arquivo

        # Caminho local para salvar o arquivo .whl
        local_path = os.path.join(os.getcwd(), "libraries")

        # Fazer o download do arquivo .whl
        if not os.path.exists(local_path):
            print(f"Baixando {talib_whl} de {talib_url}...")
            response = requests.get(talib_url, stream=True)
            if response.status_code == 200:
                with open(local_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                print(f"Download concluído: {local_path}")
            else:
                print(f"Erro ao baixar {talib_url}: {response.status_code}")
                return False
        else:
            print(f"O arquivo {talib_whl} já existe. Pulando o download.")

        # Instalar o arquivo .whl com pip
        print(f"Instalando {talib_whl}...")
        try:
            subprocess.check_call(["pip", "install", local_path])
            print("TA-Lib instalado com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro durante a instalação: {e}")
            return False

        # Remover o arquivo .whl após a instalação (opcional)
        if os.path.exists(local_path):
            os.remove(local_path)
            print(f"Arquivo {local_path} removido após a instalação.")
        return True

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
