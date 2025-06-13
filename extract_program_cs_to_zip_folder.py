import os
import shutil
import zipfile

lista_atv = '3'

def copiar_renomear_por_pasta(solution_path, nome_destino):
    destino = os.path.join("C:/Code/C#/python_outputs", nome_destino)

    # Cria a pasta destino
    if not os.path.exists(destino):
        os.makedirs(destino)

    for root, dirs, files in os.walk(solution_path):
        for dir_name in dirs:
            pasta_exercicio = os.path.join(root, dir_name)
            arquivo_origem = os.path.join(pasta_exercicio, "Program.cs")

            if os.path.exists(arquivo_origem):
                novo_nome = f"{dir_name}.cs"  # Nome baseado na pasta
                destino_arquivo = os.path.join(destino, novo_nome)

                try:
                    shutil.copyfile(arquivo_origem, destino_arquivo)
                    print(f"{arquivo_origem} copiado como {destino_arquivo}")
                except Exception as e:
                    print(f"Erro ao copiar {arquivo_origem}: {e}")
        break  # Evita descer recursivamente nas subpastas dos exercícios

    return destino

def compactar_pasta_em_zip(caminho_pasta):
    caminho_zip = f"{caminho_pasta}.zip"
    with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(caminho_pasta):
            for file in files:
                caminho_completo = os.path.join(root, file)
                caminho_relativo = os.path.relpath(caminho_completo, caminho_pasta)
                zipf.write(caminho_completo, caminho_relativo)
    print(f"Pasta compactada em: {caminho_zip}")

# Nome da sua pasta final (ex: seu nome)
nome_usuario = f"Eduardo_Bonfim_Lista{lista_atv}"  # Substitua pelo seu nome
pasta_lista = rf"C:/Code/C#/repos/Lista{lista_atv}"  # Caminho da lista

# Executa
pasta_saida = copiar_renomear_por_pasta(pasta_lista, nome_usuario)
compactar_pasta_em_zip(pasta_saida)
