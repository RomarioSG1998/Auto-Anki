from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from PIL import Image
import os
import glob
import numpy as np

# Caminhos para seus diretórios
image_folder = r"C:\Users\Josiane\Desktop\auto-anki\auto-video\imagens"
audio_folder = r"C:\Users\Josiane\Desktop\auto-anki\auto-video\audio"

# Obter todos os arquivos de imagem no diretório
image_files = sorted(glob.glob(os.path.join(image_folder, "*.jpg")))  # você pode mudar "*.jpg" para a extensão apropriada

# Obter o arquivo de áudio (assumindo que há apenas um)
audio_files = glob.glob(os.path.join(audio_folder, "*.mp3"))
if not audio_files:
    raise ValueError("Nenhum arquivo de áudio encontrado na pasta especificada.")
audio_file = audio_files[0]

# Lista para armazenar os clipes de imagem
image_clips = []

# Duração de cada imagem
image_duration = 5  # segundos

# Resolução do vídeo para YouTube
video_width = 1920
video_height = 1080

# Taxa de quadros (fps) para o vídeo
fps = 24

# Redimensionar as imagens usando Pillow antes de criar os clipes de vídeo
for image_path in image_files:
    # Abrir a imagem com Pillow
    img_pil = Image.open(image_path)
    
    # Redimensionar a imagem usando o método bicúbico (ou outro método se preferir)
    img_resized = img_pil.resize((video_width, video_height), resample=Image.BICUBIC)
    
    # Converter a imagem redimensionada para um array numpy
    img_np = np.array(img_resized)
    
    # Converter o array numpy para um ImageClip
    clip = ImageClip(img_np).set_duration(image_duration).set_fps(fps)
    clip = clip.set_position("center")
    
    # Adicionar o clip à lista de clipes de imagem
    image_clips.append(clip)

# Concatenar todos os clipes de imagem em uma sequência
image_sequence = concatenate_videoclips(image_clips, method="compose")

# Carregar o arquivo de áudio
audio = AudioFileClip(audio_file)

# Duração de cada segmento de vídeo
segment_duration = 360  # 6 minutos em segundos

# Número de segmentos necessários
num_segments = int(audio.duration // segment_duration) + 1

# Gerar vídeos para cada segmento do áudio
for i in range(num_segments):
    start_time = i * segment_duration
    end_time = min((i + 1) * segment_duration, audio.duration)
    
    # Criar um subclip do áudio
    audio_segment = audio.subclip(start_time, end_time)
    
    # Repetir a sequência de imagens para corresponder à duração do segmento de áudio
    num_repeats = int(audio_segment.duration // image_sequence.duration) + 1
    repeated_sequence = concatenate_videoclips([image_sequence] * num_repeats, method="compose").subclip(0, audio_segment.duration)
    
    # Definir o áudio para a sequência repetida
    final_video = repeated_sequence.set_audio(audio_segment)
    
    # Exportar o vídeo final
    output_filename = f"final_video_part_{i+1}.mp4"
    final_video.write_videofile(output_filename, codec="libx264", audio_codec="aac", fps=fps)

    print(f"Criação de todas parte completa!")
