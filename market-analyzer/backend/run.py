import os
import subprocess
import sys

# Função para verificar se o ambiente virtual está ativo
def is_virtual_env():
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

# Função para executar o setup.py automaticamente se o ambiente virtual não estiver presente
def run_setup_if_needed():
    if not is_virtual_env():
        print("Ambiente virtual não detectado. Executando setup.py...")
        subprocess.check_call([sys.executable, 'setup.py', 'install'])

def main():
    # Verifica se o ambiente virtual está ativo ou se precisa ser criado
    run_setup_if_needed()

    # Agora que o ambiente virtual está ativo, seu código pode ser executado
    print("Ambiente virtual está ativo, iniciando a aplicação...")
    # Adicione aqui a execução do seu código principal
    subprocess.check_call([sys.executable, 'your_main_script.py'])

if __name__ == "__main__":
    main()
