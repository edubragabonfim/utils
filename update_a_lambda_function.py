import os
import shutil
import zipfile
import boto3
import sys
import subprocess
from pathlib import Path

# Caminhos base dos seus projetos
CAMINHOS = {
    1: r"C:\Code\Python\LucIAna_Features",
    2: r"C:\Code",
}

def zip_folder(source_folder, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                abs_path = os.path.join(root, file)
                arcname = os.path.relpath(abs_path, start=source_folder)
                zipf.write(abs_path, arcname)

def atualizar_lambda(lambda_name, subfolder_name, index, bucket_name):
    base_path = CAMINHOS.get(index)
    if not base_path:
        print(f"❌ Caminho não encontrado para o índice {index}.")
        sys.exit(1)

    source_path = Path(base_path) / subfolder_name
    requirements_path = source_path / "requirements.txt"
    if not source_path.exists():
        print(f"❌ A pasta '{source_path}' não foi encontrada.")
        sys.exit(1)

    print(f"📦 Preparando pacote da pasta: {source_path}")

    tmp_dir = Path("tmp")
    package_dir = tmp_dir / "package"
    package_dir.mkdir(parents=True, exist_ok=True)

    s3_key_prefix = f"monteiro_{subfolder_name}"
    s3_key = f"{s3_key_prefix}/lambda_package.zip"

    try:
        # 1. Instalar dependências
        if requirements_path.exists():
            print("📦 Instalando dependências do requirements.txt...")
            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                str(requirements_path),
                "-t",
                str(package_dir)
            ])
        else:
            print("⚠️ Nenhum requirements.txt encontrado, seguindo sem dependências...")

        # 2. Copiar arquivos do código
        for item in source_path.iterdir():
            if item.name == "requirements.txt":
                continue
            destino = package_dir / item.name
            if item.is_file():
                shutil.copy(item, destino)
            elif item.is_dir():
                shutil.copytree(item, destino, dirs_exist_ok=True)

        # 3. Zipar o pacote
        zip_path = tmp_dir / "package.zip"
        zip_folder(package_dir, zip_path)

        # 4. Upload para o S3
        print(f"☁️ Fazendo upload para S3: s3://{bucket_name}/{s3_key}")
        s3_client = boto3.client("s3")
        s3_client.upload_file(str(zip_path), bucket_name, s3_key)

        # 5. Atualizar Lambda usando S3
        print("🚀 Atualizando função Lambda via S3...")
        lambda_client = boto3.client('lambda')
        response = lambda_client.update_function_code(
            FunctionName=lambda_name,
            S3Bucket=bucket_name,
            S3Key=s3_key
        )
        print("✔️ Lambda atualizada com sucesso!")
        print(f"🕓 Última modificação: {response.get('LastModified')}")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        print("🧹 Limpeza concluída.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python update_a_lambda_function.py <nome_lambda> <nome_pasta_codigo> <numero_caminho> <nome_bucket>")
        sys.exit(1)

    nome_lambda = sys.argv[1]
    pasta_codigo = sys.argv[2]
    numero_caminho = int(sys.argv[3])
    nome_bucket = sys.argv[4]

    atualizar_lambda(nome_lambda, pasta_codigo, numero_caminho, nome_bucket)
