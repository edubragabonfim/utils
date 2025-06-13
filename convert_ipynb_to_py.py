import os
import shutil
import nbformat
from nbconvert import PythonExporter

def converter_ipynb_para_py():
    # Lista dos notebooks a serem convertidos
    notebooks = ["d_dimensions.ipynb", "f_facts.ipynb"]
    
    for nome_arquivo in notebooks:
        for root, dirs, files in os.walk("."):
            if nome_arquivo in files and nome_arquivo.endswith(".ipynb"):
                caminho_ipynb = os.path.join(root, nome_arquivo)

                # Lê o notebook
                with open(caminho_ipynb, "r", encoding="utf-8") as f:
                    notebook = nbformat.read(f, as_version=4)

                # Converte para .py
                script, _ = PythonExporter().from_notebook_node(notebook)

                # Garante que a pasta scripts exista
                pasta_destino = os.path.join(".", "scripts")
                os.makedirs(pasta_destino, exist_ok=True)

                # Caminho do novo .py
                nome_py = nome_arquivo.replace(".ipynb", ".py")
                caminho_py = os.path.join(pasta_destino, nome_py)

                with open(caminho_py, "w", encoding="utf-8") as f:
                    f.write(script)

                print(f"✔️ Convertido com sucesso: {caminho_py}")

    # Copia os arquivos para a pasta scripts
    copiar_arquivos_para_scripts()

def copiar_arquivos_para_scripts():
    arquivos_para_copiar = [
        ("methods_database.py", "methods_database.py"),
        ("methods_data_transformation.py", "methods_data_transformation.py"),
        (".env", ".env")
    ]

    pasta_destino = os.path.join(".", "scripts")
    for arquivo_origem, arquivo_destino in arquivos_para_copiar:
        caminho_origem = os.path.join(".", arquivo_origem)
        caminho_destino = os.path.join(pasta_destino, arquivo_destino)
        
        if os.path.exists(caminho_origem):
            shutil.copy2(caminho_origem, caminho_destino)
            print(f"📦 {arquivo_destino} copiado para: {caminho_destino}")
        else:
            print(f"⚠️ Arquivo {arquivo_origem} não encontrado na raiz do projeto.")

# Execução
if __name__ == "__main__":
    converter_ipynb_para_py()