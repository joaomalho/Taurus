import os
import sys
import subprocess

def update_dependencies(libraries_path="libraries", requirements_file="requirements.txt"):
    """
    Atualiza todas as dependências listadas no arquivo requirements.txt e instala na pasta libraries.
    """
    print("Iniciando a atualização das dependências...")

    if not os.path.exists(libraries_path):
        print(f"Diretório '{libraries_path}' não encontrado. Criando diretório...")
        os.makedirs(libraries_path)

    if not os.path.exists(requirements_file):
        print(f"Arquivo {requirements_file} não encontrado. Certifique-se de que ele exista.")
        return

    # Atualizar pip e as dependências
    try:
        print("Atualizando o pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

        print(f"Atualizando dependências do {requirements_file} e instalando em {libraries_path}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "-r", requirements_file, "--target", libraries_path
        ])

        print("Todas as dependências foram atualizadas com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro durante a atualização das dependências: {e}")

if __name__ == "__main__":
    libraries_path = "libraries"
    requirements_file = "requirements.txt"
    update_dependencies(libraries_path, requirements_file)
