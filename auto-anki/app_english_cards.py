import requests
from PIL import Image
import pyautogui
import pyperclip
from io import BytesIO
import os
from time import sleep
import uuid

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

# 1- Clica em cadastro
pyautogui.click(611, 115, duration=1)

# 4- Extrair cada produto
with open('anki.txt', 'r') as arquivo:
    # Ignorar a primeira linha (cabeçalhos)
    next(arquivo)
    for linha in arquivo:
        # Depuração: exibir a linha lida
        print(f"Lendo linha: {linha.strip()}")
        
        # Verificar e dividir a linha
        try:
            pergunta, resposta, imagem_url = linha.strip().split(',')
        except ValueError as e:
            print(f"Erro ao processar linha: {e}")
            continue  # Pular a linha em caso de erro

        # Depuração: exibir os valores extraídos
        print(f"Pergunta: {pergunta}, Resposta: {resposta}, Imagem: {imagem_url}")

        # Baixar a imagem
        try:
            image = download_image(imagem_url)
            image = convert_image_to_jpg(image)
            unique_filename = generate_unique_filename()
            image_path = os.path.join(os.getcwd(), unique_filename)
            save_image(image, image_path)

            # Para fins de teste, retornamos o caminho do arquivo local
            new_image_url = upload_image(image_path)

            # Depuração: exibir o caminho da imagem convertida
            print(f"Imagem convertida salva em: {new_image_url}")
        except Exception as e:
            print(f"Erro ao processar a imagem: {e}")
            continue

        # Executar ações de pyautogui
        pyautogui.click(611, 115, duration=2)
        pyautogui.click(973, 228, duration=5)
        pyautogui.write(pergunta)
        
        # clicar na imagem com o botao esuqerdo
        pyautogui.click(197,426, duration=2)
        pyautogui.click(197,426, duration=2, button='right')
        pyautogui.click(282,586, duration=2)



        pyautogui.click(1058, 308, duration=2)
        pyautogui.write(resposta + ' ')  # Adicionando um espaço entre a resposta e a imagem
        pyautogui.hotkey('ctrl', 'v')  # Simular Ctrl+V para colar o link da imagem


        pyautogui.click(977, 516, duration=2)
        pyautogui.click(1171, 523, duration=2)

        pyautogui.click(197,426, duration=2, button='right')
        pyautogui.click(270,661, duration=2)

      
       
        
        sleep(2)

# Clicar em algum lugar após o loop para finalizar o processo
pyautogui.click(993, 65, duration=2)
