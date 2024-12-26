import os

# Caminho do arquivo original
caminho_arquivo_original = r'C:\Users\Josiane\Desktop\texto_original.txt'

# Verificar se o arquivo existe
if os.path.exists(caminho_arquivo_original):
    print("O arquivo existe.")
else:
    print("O arquivo não foi encontrado. Verifique o caminho.")
