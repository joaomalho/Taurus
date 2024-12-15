import os
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
import venv

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
        
        # Ativar o ambiente virtual
        if os.name == 'nt':
            activate_script = os.path.join(venv_dir, 'Scripts', 'activate_this.py')
        else:
            activate_script = os.path.join(venv_dir, 'bin', 'activate_this.py')
        
        exec(open(activate_script).read(), {'__file__': activate_script})

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

# Carregar dependências do requirements.txt
requirements = parse_requirements("requirements.txt")

setup(
    name="taurus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,  # Usa o requirements.txt
    extras_require={
        "yfinance": ["yfinance>=0.0.0"],
    },
    cmdclass={
        "install": CustomInstallCommand,
    },
)
