import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def extract_program_cs_to_pdf(solution_path, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    y_position = height - 40  # Posição inicial do texto

    for root, _, files in os.walk(solution_path):
        for file in files:
            if file == "Program.cs":  # Filtra apenas Program.cs
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as cs_file:
                        content = cs_file.readlines()

                    c.setFont("Courier", 10)  # Define a fonte para texto de código
                    c.drawString(30, y_position, f"### Arquivo: {file_path} ###")
                    y_position -= 20

                    for line in content:
                        if y_position < 40:  # Criar nova página se necessário
                            c.showPage()
                            c.setFont("Courier", 10)
                            y_position = height - 40
                        c.drawString(30, y_position, line.strip())
                        y_position -= 12  # Ajusta espaçamento entre linhas
                    
                    # Adiciona uma linha separadora
                    y_position -= 10
                    c.drawString(30, y_position, "-" * 77)
                    y_position -= 20
                except Exception as e:
                    print(f"Erro ao ler {file_path}: {e}")

    c.save()  # Salva o PDF


actual_folder = 'Lista1'
file_name = f'output_{actual_folder}.pdf'

# Defina o caminho da solução e do arquivo de saída
solution_directory = r"C:/Code/C#/repos/" + actual_folder  # Atualize com o caminho real
output_pdf = os.path.join("C:/Code/C#/python_outputs", file_name)

# Executa a extração
extract_program_cs_to_pdf(solution_directory, output_pdf)

print(f"Todos os arquivos .cs foram extraídos para {output_pdf}")
