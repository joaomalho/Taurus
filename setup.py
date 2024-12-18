import os
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
import venv
import requests

# Função para carregar as dependências do requirements.txt
def parse_requirements(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    # Remover linhas em branco e comentários
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]

class CustomInstallCommand(install):
    def run(self):

        if not self.is_virtual_env():
            print("Ambiente virtual não detectado. Criando ambiente virtual...")
            self.create_virtualenv()

        install.run(self)

        self.install_yfinance()

        if os.name == "nt":
            self.install_ta_lib_windows()

    def is_virtual_env(self):
        """Verifica se o script está sendo executado em um ambiente virtual"""
        return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

    def create_virtualenv(self):
        """Cria o ambiente virtual"""
        venv_dir = os.path.join(os.getcwd(), 'venv')
        if not os.path.exists(venv_dir):
            print(f"Criando ambiente virtual em: {venv_dir}")
            venv.create(venv_dir, with_pip=True)

        # Usar o pip do ambiente virtual diretamente
        pip_path = os.path.join(venv_dir, 'Scripts', 'pip.exe')

        # Instalar as dependências do requirements.txt no ambiente virtual
        print(f"Instalando as dependências no ambiente virtual usando: {pip_path}")
        subprocess.check_call([pip_path, 'install', '-r', 'requirements.txt'])

    def install_yfinance(self):
        """Instala o yfinance com os parâmetros específicos."""
        print("Instalando yfinance com as opções --upgrade --no-cache-dir...")
        subprocess.check_call("pip install yfinance --upgrade --no-cache-dir", shell=True)

    def install_ta_lib_windows(self):
        """Automatiza a instalação do TA-Lib no Windows."""
        print("Instalando TA-Lib no Windows...")

        # URL do arquivo .whl
        talib_url = "https://github.com/cgohlke/talib-build/releases/download/v0.5.1/ta_lib-0.5.1-cp311-cp311-win_amd64.whl"
        
        # Diretório onde o arquivo será salvo
        library_dir = os.path.join(os.getcwd(), "library")
        
        # Verificar se o diretório 'library' existe, se não, cria
        if not os.path.exists(library_dir):
            os.makedirs(library_dir)

        # Caminho do arquivo para salvar
        file_path = os.path.join(library_dir, "ta_lib-0.5.1-cp311-cp311-win_amd64.whl")

        # Baixar o arquivo
        print(f"Baixando o arquivo de {talib_url}...")
        response = requests.get(talib_url, stream=True)

        # Verifica se o download foi bem-sucedido
        if response.status_code == 200:
            # Salvar o arquivo no diretório
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print(f"Arquivo salvo em {file_path}")
        else:
            print(f"Falha ao baixar o arquivo, status code: {response.status_code}")

        # Usar o pip do ambiente virtual para instalar o .whl
        venv_dir = os.path.join(os.getcwd(), 'venv')
        pip_path = os.path.join(venv_dir, 'Scripts', 'pip.exe')

        # Instalar o arquivo .whl no ambiente virtual
        print(f"Instalando TA-Lib a partir do arquivo baixado usando: {pip_path}")
        subprocess.check_call([pip_path, 'install', file_path])

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
