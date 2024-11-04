from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import librosa
import soundfile as sf
import numpy as np
import os

# Caminhos do vídeo e do arquivo final
video_path = r"C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\VIDEOS\teste.mp4"
final_video_path = r"C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\VIDEOS\video_editado.mp4"

def adicionar_ruido_branco(arquivo_audio, output_audio):
    # Carregar o áudio original
    audio_original, sr = librosa.load(arquivo_audio, sr=None)
    
    # Gerar ruído branco de baixa intensidade
    ruido_branco = np.random.normal(0, 0.005, size=audio_original.shape)
    
    # Misturar o ruído branco com o áudio original
    audio_com_ruido = audio_original + ruido_branco
    
    # Garantir que o áudio esteja na faixa [-1, 1]
    audio_com_ruido = np.clip(audio_com_ruido, -1, 1)

    # Salvar o áudio modificado
    sf.write(output_audio, audio_com_ruido, sr)

# Verificar e criar o diretório de saída, se necessário
os.makedirs(os.path.dirname(final_video_path), exist_ok=True)

# Carregar o vídeo
video = VideoFileClip(video_path)

# Extrair o áudio do vídeo e salvar temporariamente
audio_temp_path = "temp_audio.wav"
video.audio.write_audiofile(audio_temp_path)

# Adicionar ruído branco ao áudio
output_audio_path = "audio_com_ruido.wav"
adicionar_ruido_branco(audio_temp_path, output_audio_path)

# Carregar o novo áudio com ruído
new_audio = VideoFileClip(output_audio_path)

# Ajustar tempos de início e fim para cortes
start_time = 0.1  # 100 ms
end_time = video.duration - 0.1  # 100 ms antes do fim

# Criar o vídeo final
final_video = CompositeVideoClip([video.subclip(start_time, end_time)])

# Atribuir o novo áudio ao vídeo final
final_video = final_video.set_audio(new_audio)

# Exportar o vídeo final com o fps do vídeo original
final_video.write_videofile(final_video_path, codec='libx264', fps=video.fps)

# Remover arquivos temporários
os.remove(audio_temp_path)
os.remove(output_audio_path)
