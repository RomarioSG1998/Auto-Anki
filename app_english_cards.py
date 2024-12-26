import requests
from PIL import Image
import pyautogui
import pyperclip
from io import BytesIO
import os
from time import sleep
import uuid
import win32clipboard
from win32con import CF_DIB
import io

# Variável global para armazenar a imagem
current_image = None

def download_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

def convert_image_to_jpg(image):
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    return image

def save_image(image, path):
    image.save(path, format="JPEG")

# Função para gerar um nome de arquivo único
def generate_unique_filename():
    return f"image_{uuid.uuid4().hex}.jpg"

# Função fictícia de upload que apenas retorna o caminho local para a imagem convertida
def upload_image(image_path):
    return image_path

def image_to_clipboard(image):
    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(CF_DIB, data)
    win32clipboard.CloseClipboard()

# 1- Clica em cadastro
pyautogui.click(611, 115, duration=1)

# 4- Extrair cada produto
with open('anki.txt', 'r', encoding='utf-8') as arquivo:
    # Ignorar a primeira linha (cabeçalhos)
    next(arquivo)
    for linha in arquivo:
        # Finalizar se encontrar "pare aqui"
        if "pare aqui" in linha:
            print("Encontrado 'pare aqui'. Finalizando o script.")
            break
        
        # Depuração: exibir a linha lida
        print(f"Lendo linha: {linha.strip()}")
        
        # Verificar e dividir a linha usando '||'
        try:
            partes = linha.strip().split(' || ')
            if len(partes) != 3:
                raise ValueError("Número incorreto de partes na linha")
            
            pergunta, resposta, imagem_url = partes
        except ValueError as e:
            print(f"Erro ao processar linha: {e}")
            continue  # Pular a linha em caso de erro

        # Depuração: exibir os valores extraídos
        print(f"Pergunta: {pergunta}, Resposta: {resposta}, Imagem: {imagem_url}")

        # Baixar a imagem
        try:
            current_image = download_image(imagem_url)
            current_image = convert_image_to_jpg(current_image)
            unique_filename = generate_unique_filename()
            image_path = os.path.join(os.getcwd(), unique_filename)
            save_image(current_image, image_path)

            # Para fins de teste, retornamos o caminho do arquivo local
            new_image_url = upload_image(image_path)

            # Depuração: exibir o caminho da imagem convertida
            print(f"Imagem convertida salva em: {new_image_url}")
        except Exception as e:
            print(f"Erro ao processar a imagem: {e}")
            current_image = None  # Definir como None em caso de erro

        # Executar ações de pyautogui
        pyautogui.click(611, 115, duration=2)
        pyautogui.click(973, 228, duration=5)
        pyperclip.copy(pergunta + ' ')  # Copiar a pergunta para a área de transferência
        pyautogui.hotkey('ctrl', 'v')  # Simular Ctrl+V para colar a pergunta

        pyautogui.click(1058, 318, duration=2)
        pyperclip.copy(resposta + ' ')  # Copiar a resposta para a área de transferência
        pyautogui.hotkey('ctrl', 'v')  # Simular Ctrl+V para colar a resposta

        # Colar a imagem após colar a resposta
        if current_image:
            image_to_clipboard(current_image)  # Copiar a imagem para a área de transferência
            pyautogui.hotkey('ctrl', 'v')  # Simular Ctrl+V para colar a imagem

        pyautogui.click(977, 516, duration=4)
        pyautogui.click(1171, 523, duration=2)

        pyautogui.click(197, 426, duration=2, button='right')
        pyautogui.click(270, 661, duration=2)
        
        sleep(2)

# Clicar em algum lugar após o loop para finalizar o processo
pyautogui.click(993, 65, duration=2)
 