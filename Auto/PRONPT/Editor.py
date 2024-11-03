from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, CompositeAudioClip
from pydub import AudioSegment
import numpy as np
import os

# Caminhos do vídeo e do arquivo final
video_path = r"C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\VIDEOS\teste.mp4"
final_video_path = r"C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\VIDEOS"

def mod_som(video):
    # Extrair o áudio original
    audio_original = video.audio.to_soundarray(fps=44100)
    # Gerar ruído branco de baixa intensidade
    ruido_branco = (np.random.normal(0, 0.005, size=audio_original.shape)).astype(np.float32)
    # Misturar o ruído branco com o áudio original
    audio_com_ruido = audio_original + ruido_branco

    # Criar um novo áudio a partir do array
    audio_segment = AudioSegment(
        audio_com_ruido.tobytes(), 
        frame_rate=44100, 
        sample_width=audio_com_ruido.dtype.itemsize, 
        channels=1
    )
    
    # Exportar o áudio modificado
    audio_segment.export("temp_audio.wav", format="wav")
    
    # Carregar o áudio modificado
    audio_final = AudioSegment.from_wav("temp_audio.wav")
    
    # Adicionar o áudio modificado ao vídeo
    video = video.set_audio(audio_final)
    
    return video

# Verificar e criar o diretório de saída, se necessário
os.makedirs(os.path.dirname(final_video_path), exist_ok=True)

# Carregar o vídeo
video = VideoFileClip(video_path)

# Criar o texto
text = TextClip("VIDEO EDITADO", fontsize=1, color='white', bg_color='black', size=video.size)
text = text.set_duration(5).set_opacity(0.2)
text = text.set_position('center').set_start(video.duration / 2)  # Texto no meio do vídeo

# Ajustar tempos de início e fim para cortes
start_time = 0.1  # 100 ms
end_time = video.duration - 0.1  # 100 ms antes do fim

# Criar o vídeo final
video = mod_som(video)  # Modificar o áudio
final_video = CompositeVideoClip([video.subclip(start_time, end_time), text])

# Exportar o vídeo final com o fps do vídeo original
final_video.write_videofile(final_video_path, codec='libx264', fps=video.fps)
