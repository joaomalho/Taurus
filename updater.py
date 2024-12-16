import os
import subprocess

def update_dependencies(venv_path="taurus_venv", requirements_file="requirements.txt"):
    """
    Atualiza todas as dependências listadas no arquivo requirements.txt.
    """
    print("Iniciando a atualização das dependências...")

    # Verifica se o ambiente virtual existe
    if not os.path.exists(venv_path):
        print(f"Ambiente virtual '{venv_path}' não encontrado. Por favor, crie o ambiente antes de atualizar.")
        return

    # Caminho para o Python dentro do ambiente virtual
    if os.name == 'nt':
        venv_python = os.path.join(venv_path, "Scripts", "python")
    else:
        venv_python = os.path.join(venv_path, "bin", "python")

    # Verificar se o arquivo requirements.txt existe
    if not os.path.exists(requirements_file):
        print(f"Arquivo {requirements_file} não encontrado. Certifique-se de que ele exista.")
        return

    # Atualizar pip e as dependências
    try:
        print("Atualizando o pip...")
        subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip"])

        print(f"Atualizando dependências do {requirements_file}...")
        subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "-r", requirements_file])

        print("Todas as dependências foram atualizadas com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro durante a atualização das dependências: {e}")

if __name__ == "__main__":
    venv_path = "venv"  # Nome do ambiente virtual
    requirements_file = "requirements.txt"  # Nome do arquivo de dependências
    update_dependencies(venv_path, requirements_file)
