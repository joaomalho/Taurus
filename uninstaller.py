import os
import shutil

def remove_directory(directory):
    """Remove um diretório e todos os seus conteúdos."""
    if os.path.exists(directory):
        print(f"Removendo o diretório: {directory}")
        shutil.rmtree(directory)
    else:
        print(f"O diretório {directory} não existe ou já foi removido.")

def remove_file(file_path):
    """Remove um arquivo específico."""
    if os.path.exists(file_path):
        print(f"Removendo o arquivo: {file_path}")
        os.remove(file_path)
    else:
        print(f"O arquivo {file_path} não existe ou já foi removido.")

def uninstall_environment(venv_path="venv"):
    """Remove o ambiente virtual e os arquivos temporários associados."""
    print("Iniciando o processo de desinstalação...")

    # Remover o ambiente virtual
    remove_directory(venv_path)

    # Remover arquivos temporários relacionados ao TA-Lib
    remove_directory("ta-lib")  # Diretório de compilação do TA-Lib
    remove_file("ta-lib.zip")  # Arquivo ZIP do TA-Lib (Windows)
    remove_file("ta-lib.tar.gz")  # Arquivo TAR.GZ do TA-Lib (Linux)

    print("Desinstalação concluída. Todos os arquivos relacionados foram removidos.")

if __name__ == "__main__":
    uninstall_environment()
