import os
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.easy_install import easy_install
import venv
import shutil

# Função para carregar as dependências do requirements.txt
def parse_requirements(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    # Remover linhas em branco e comentários
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]

class CustomInstallCommand(install):
    def run(self):
        # Verificar se o ambiente virtual está ativado
        if not self.is_virtual_env():
            print("Ambiente virtual não detectado. Criando ambiente virtual...")
            self.create_virtualenv()

        # Instalar os requisitos Python padrão
        install.run(self)

        # Garantir a instalação do yfinance com as opções específicas
        self.install_yfinance()

        # Checar e instalar dependências adicionais (TA-Lib)
        if os.name == "nt":
            self.install_ta_lib_windows()
        elif os.name == "posix":
            self.install_ta_lib_linux()

    def is_virtual_env(self):
        """Verifica se o script está sendo executado em um ambiente virtual"""
        return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

    def create_virtualenv(self):
        """Cria e ativa o ambiente virtual"""
        venv_dir = os.path.join(os.getcwd(), 'venv')
        if not os.path.exists(venv_dir):
            print(f"Criando ambiente virtual em: {venv_dir}")
            venv.create(venv_dir, with_pip=True)

        # Ativar o ambiente virtual de forma adequada para o sistema operacional
        if os.name == 'nt':
            # No Windows, utilizamos o arquivo `activate.bat`
            activate_script = os.path.join(venv_dir, 'Scripts', 'activate.bat')
        else:
            # No Linux/MacOS, utilizamos o script `activate`
            activate_script = os.path.join(venv_dir, 'bin', 'activate')

        # Executar o script de ativação (somente ativação no código)
        print(f"Ativando o ambiente virtual com: {activate_script}")
        subprocess.call([activate_script], shell=True)

    def install_yfinance(self):
        """Instala o yfinance com os parâmetros específicos."""
        print("Instalando yfinance com as opções --upgrade --no-cache-dir...")
        subprocess.check_call("pip install yfinance --upgrade --no-cache-dir", shell=True)

    def install_ta_lib_windows(self):
        """Automatiza a instalação do TA-Lib no Windows."""
        print("Instalando TA-Lib no Windows...")
        talib_url = "https://sourceforge.net/projects/ta-lib/files/latest/download"
        talib_dir = os.path.join(os.getcwd(), "ta-lib")

        if not os.path.exists(talib_dir):
            os.makedirs(talib_dir)

        # Baixar e descompactar a biblioteca
        subprocess.check_call(f"curl -L {talib_url} --output ta-lib.zip", shell=True)
        subprocess.check_call("tar -xvf ta-lib.zip -C ta-lib --strip-components=1", shell=True)

        # Compilar a biblioteca
        os.chdir(os.path.join(talib_dir, "c", "make", "cdr", "win32", "msvc"))
        subprocess.check_call(
            r'"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" && nmake',
            shell=True
        )
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def install_ta_lib_linux(self):
        """Automatiza a instalação do TA-Lib no Linux."""
        print("Instalando TA-Lib no Linux...")
        subprocess.check_call("sudo apt-get update && sudo apt-get install -y build-essential wget", shell=True)
        talib_url = "https://sourceforge.net/projects/ta-lib/files/latest/download"
        subprocess.check_call(f"wget {talib_url} -O ta-lib.tar.gz", shell=True)
        subprocess.check_call("tar -xvzf ta-lib.tar.gz", shell=True)
        os.chdir("ta-lib")
        subprocess.check_call("./configure --prefix=/usr", shell=True)
        subprocess.check_call("make", shell=True)
        subprocess.check_call("sudo make install", shell=True)
        os.chdir("..")

class CustomUninstallCommand(easy_install):
    """Comando personalizado para desinstalar o pacote e remover o ambiente virtual"""
    
    description = "Desinstala o pacote e remove o ambiente virtual"
    
    def run(self):
        # Remover o ambiente virtual, se existir
        venv_dir = os.path.join(os.getcwd(), 'venv')
        if os.path.exists(venv_dir):
            print(f"Removendo ambiente virtual em: {venv_dir}")
            shutil.rmtree(venv_dir)  # Remove o diretório do ambiente virtual

        # Desinstalar o pacote via pip
        print("Desinstalando o pacote usando pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "taurus"])

        # Chama a desinstalação do pacote do setuptools
        easy_install.run(self)

class UpdateCommand(easy_install):
    """Comando para atualizar todas as dependências do requirements.txt"""
    description = "Atualiza as dependências do requirements.txt para a versão mais recente"
    
    def run(self):
        """Executa a atualização das dependências"""
        print("Atualizando pacotes do requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"])

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
        "install": CustomInstallCommand,
        "uninstall": CustomUninstallCommand,
        "update": UpdateCommand,
    },
)
