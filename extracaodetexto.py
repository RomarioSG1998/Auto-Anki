import os
import zipfile
from PIL import Image
import pytesseract
import re

# Configuração do caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Defina o caminho para a pasta de download e para o arquivo ZIP
download_folder = "downloads"
zip_path = r'C:\\Users\\Josiane\\Downloads\\arquivos.zip'  #caminho do seu arquivo ZIP

# Crie a pasta de download se não existir
os.makedirs(download_folder, exist_ok=True)

# Função para extrair arquivos do ZIP
def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Arquivos extraídos para {extract_to}")

# Função para verificar se um arquivo é uma imagem
def is_image(file_path):
    try:
        Image.open(file_path)
        return True
    except IOError:
        return False

# Função para extrair texto de imagens usando OCR
def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        
        # Pré-processamento simples: remoção de caracteres não alfanuméricos
        text_clean = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        return text_clean.strip()  # Remove espaços em branco no início e fim
    except Exception as e:
        print(f"Erro ao processar imagem {image_path}: {e}")
        return ""

# Extraia os arquivos do ZIP
extract_zip(zip_path, download_folder)

# Variável para acumular todos os textos extraídos
all_texts = ""

# Itere sobre os arquivos extraídos e processe as imagens
for root, _, files in os.walk(download_folder):
    for file in files:
        file_path = os.path.join(root, file)
        if is_image(file_path):
            print(f"Processando imagem: {file_path}")
            text = extract_text_from_image(file_path)
            all_texts += text + "\n\n"  # Adiciona o texto extraído à variável, separando por parágrafos

# Imprime ou salva o texto acumulado
print("Texto completo extraído:\n")
print(all_texts)

# Exemplo de salvar o texto em um arquivo
output_file = "output.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(all_texts)

print(f"\nTexto completo salvo em {output_file}")
