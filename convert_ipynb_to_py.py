import sys
import pathlib
import nbformat
from nbconvert import PythonExporter

def converter_ipynb_para_py(nome_sem_extensao):
    ipynb_path = pathlib.Path(f"{nome_sem_extensao}.ipynb")

    if not ipynb_path.exists():
        print(f"❌ Arquivo {ipynb_path.name} não encontrado na pasta atual.")
        sys.exit(1)

    with ipynb_path.open("r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    script, _ = PythonExporter().from_notebook_node(notebook)
    py_path = ipynb_path.with_suffix(".py")

    with py_path.open("w", encoding="utf-8") as f_out:
        f_out.write(script)

    print(f"✔️ {ipynb_path.name} convertido para {py_path.name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗Uso: python converter.py <nome_do_arquivo_sem_extensao>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    converter_ipynb_para_py(nome_arquivo)
