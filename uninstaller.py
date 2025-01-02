import os
import shutil
import subprocess

def remove_directory(directory):
    """Remove um diretório e todos os seus conteúdos."""
    if os.path.exists(directory):
        print(f"Removendo o diretório: {directory}")
        shutil.rmtree(directory)
    else:
        print(f"O diretório {directory} não existe ou já foi removido.")

def uninstall_requirements(requirements_file="requirements.txt", libraries_path="libraries"):
    """Desinstala todas as bibliotecas listadas no requirements.txt e remove o diretório libraries."""
    if not os.path.exists(requirements_file):
        print(f"Arquivo {requirements_file} não encontrado. Não há bibliotecas para desinstalar.")
        return

    # Ler os pacotes do arquivo requirements.txt
    with open(requirements_file, "r") as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    # Desinstalar cada pacote
    for package in packages:
        try:
            print(f"Desinstalando o pacote: {package}")
            subprocess.check_call([os.sys.executable, "-m", "pip", "uninstall", "-y", package])
        except subprocess.CalledProcessError as e:
            print(f"Erro ao desinstalar o pacote {package}: {e}")

    remove_directory(libraries_path)
    print("Desinstalação concluída. Todas as bibliotecas, o diretório libraries e arquivos associados foram removidos.")

if __name__ == "__main__":
    uninstall_requirements()
