# Importações
from moviepy.editor import VideoFileClip, CompositeVideoClip, AudioFileClip
import librosa
import numpy as np
from pydub import AudioSegment
import os
import wave
import tempfile

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
    novo_audio = novo_audio.set_frame_rate(audio.frame_rate)
    novo_audio.export(output_path, format="wav")

# Ajustar volume em partes
def ajustar_volume_partes(audio_path, output_path, momentos, ganho):
    audio = AudioSegment.from_wav(audio_path)
    for inicio, fim in momentos:
        trecho = audio[inicio * 1000:fim * 1000]
        trecho = trecho + ganho
        audio = audio[:inicio * 1000] + trecho + audio[fim * 1000:]
    audio.export(output_path, format="wav")

# Função principal de edição
def editar(video_path, final_video_path, fator_velocidade=1.02, momentos_volume=[(1, 3)], ganho_volume=5):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Caminhos temporários
        audio_temp_path = os.path.join(temp_dir, "temp_audio.wav")
        output_audio_path = os.path.join(temp_dir, "audio_com_ruido.wav")
        output_audio_velocidade_path = os.path.join(temp_dir, "audio_velocidade.wav")

        # Carregar vídeo
        video = VideoFileClip(video_path)

        # Extrair áudio e salvar temporariamente
        video.audio.write_audiofile(audio_temp_path)

        # Adicionar ruído branco
        adicionar_ruido_branco(audio_temp_path, output_audio_path)

        # Alterar a velocidade do áudio
        alterar_velocidade(output_audio_path, output_audio_velocidade_path, fator=fator_velocidade)

        # Ajustar volume em partes específicas
        ajustar_volume_partes(output_audio_velocidade_path, output_audio_path, momentos_volume, ganho_volume)

        # Carregar o novo áudio com ruído e velocidade alterada
        new_audio = AudioFileClip(output_audio_path)

        # Cortar o vídeo e atribuir o novo áudio
        start_time = 0.1  # 100 ms
        end_time = video.duration - 0.1  # 100 ms antes do fim
        final_video = CompositeVideoClip([video.subclip(start_time, end_time)]).set_audio(new_audio)

        # Exportar o vídeo final
        final_video.write_videofile(final_video_path, codec='libx264', fps=video.fps)

        # Fechar recursos de vídeo
        video.close()
        final_video.close()
