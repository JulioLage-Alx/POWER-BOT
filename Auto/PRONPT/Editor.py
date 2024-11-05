# Importações
from moviepy.editor import VideoFileClip, CompositeVideoClip, AudioFileClip
import librosa
import numpy as np
from pydub import AudioSegment
import os
import wave

# Caminhos do vídeo e do arquivo final
video_path = r"C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\VIDEOS\video.mp4"
final_video_path = r"C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\VIDEOS\video_editado.mp4"

# Função para escrever WAV
def write_wav(filename, data, samplerate):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        int_data = np.int16(data * 32767)
        wf.writeframes(int_data.tobytes())

# Adicionar ruído branco
def adicionar_ruido_branco(arquivo_audio, output_audio):
    audio_original, sr = librosa.load(arquivo_audio, sr=None)
    ruido_branco = np.random.normal(0, 0.005, size=audio_original.shape)
    audio_com_ruido = audio_original + ruido_branco
    audio_com_ruido = np.clip(audio_com_ruido, -1, 1)
    write_wav(output_audio, audio_com_ruido, sr)

# Alterar velocidade
def alterar_velocidade(audio_path, output_path, fator=1.02):
    audio = AudioSegment.from_wav(audio_path)
    novo_audio = audio._spawn(audio.raw_data, overrides={'frame_rate': int(audio.frame_rate * fator)})
    novo_audio.export(output_path, format="wav")

# Ajustar volume em partes
def ajustar_volume_partes(audio_path, output_path, momentos, ganho):
    audio = AudioSegment.from_wav(audio_path)
    for inicio, fim in momentos:
        trecho = audio[inicio * 1000:fim * 1000]
        trecho = trecho + ganho
        audio = audio[:inicio * 1000] + trecho + audio[fim * 1000:]
    audio.export(output_path, format="wav")

# Criar diretório se não existir
os.makedirs(os.path.dirname(final_video_path), exist_ok=True)

# Carregar vídeo
video = VideoFileClip(video_path)

# Extrair áudio e salvar temporariamente
audio_temp_path = "temp_audio.wav"
video.audio.write_audiofile(audio_temp_path)

# Adicionar ruído branco
output_audio_path = "audio_com_ruido.wav"
adicionar_ruido_branco(audio_temp_path, output_audio_path)

# Alterar a velocidade do áudio
output_audio_velocidade_path = "audio_velocidade.wav"
alterar_velocidade(output_audio_path, output_audio_velocidade_path, fator=1.02)

# Ajustar volume em partes específicas (exemplo: aumentar o volume entre 1 e 3 segundos)
momentos_volume = [(1, 3)]  # Ajustar volume entre 1 e 3 segundos
ganho_volume = 5  # Aumentar o volume em 5 dB
ajustar_volume_partes(output_audio_velocidade_path, output_audio_path, momentos_volume, ganho_volume)

# Carregar o novo áudio com ruído e velocidade alterada
new_audio = AudioFileClip(output_audio_path)

# Cortar o vídeo e atribuir o novo áudio
start_time = 0.1  # 100 ms
end_time = video.duration - 0.1  # 100 ms antes do fim
final_video = CompositeVideoClip([video.subclip(start_time, end_time)])
final_video = final_video.set_audio(new_audio)

# Exportar o vídeo final
final_video.write_videofile(final_video_path, codec='libx264', fps=video.fps)

# Remover arquivos temporários
os.remove(audio_temp_path)
os.remove(output_audio_path)
os.remove(output_audio_velocidade_path)
