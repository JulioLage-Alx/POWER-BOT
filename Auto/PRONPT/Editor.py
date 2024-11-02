from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Carregar o vídeo
video_path = r"C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\POWER-BOT\VIDEOS\2024-03-29_03-20-00_UTC.mp4"
video = VideoFileClip(video_path)

# Criar o texto
text = TextClip("VIDEO EDITADO", fontsize=70, color='white', bg_color='black', size=video.size)

# Definir a duração do texto e a transparência
text = text.set_duration(5)  # Duração em segundos
text = text.set_opacity(0.2)  # Definir a transparência (0.0 a 1.0)
text = text.set_position('center').set_start(video.duration / 2)  # Colocar no meio do vídeo

# Cortar o vídeo (2 milésimos antes do início ou 3 milésimos após)
start_time = 0.002  # 2 milésimos
end_time = video.duration + 0.003  # 3 milésimos após o final

# Criar o vídeo final
final_video = CompositeVideoClip([video.subclip(start_time, end_time), text])

# Exportar o vídeo final
final_video_path = r"C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\POWER-BOT\Auto\PRONPT\PASTA.mp4"

# Certifique-se de que o fps esteja definido
final_video.write_videofile(final_video_path, codec='libx264', fps=24)