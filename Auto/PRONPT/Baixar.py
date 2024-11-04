import undetected_chromedriver as uc
from sslproxies import ProxyManager
import instaloader
import Descricoes as dc
import limp as lp
import os
import time
import requests

# Configurações do projeto
pasta = r'VIDEOS'
arquivo_saida = r'C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\POWER-BOT\Auto\DESCRIÇAO\descricao.txt'
caminho_perfis = r'C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\POWER-BOT\Auto\PERFIS\usuarios.txt'
TEMPO_ESPERA_POST = 30
TEMPO_ESPERA_PERFIL = 120
MAX_TENTATIVAS = 5
MIN_VIEW = 259865

# Inicializar o gerenciador de proxies
manager = ProxyManager()

def get_new_proxy():
    proxy = manager.get_new_proxy()
    print(f"Novo proxy obtido: {proxy}")
    return {'http': proxy, 'https': proxy}

def verificar_perfil_com_chromedriver(nome_perfil):
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    url_perfil = f'https://www.instagram.com/{nome_perfil}/'
    driver.get(url_perfil)
    time.sleep(5)
    source = driver.page_source
    driver.quit()
    return "Profile not found" not in source

def baixar_apenas_videos_perfil(nome_perfil, pasta_destino,min_views):
    os.makedirs(pasta_destino, exist_ok=True)
    loader = instaloader.Instaloader()
    video_salvos = []
    profile = None

    for tentativa in range(MAX_TENTATIVAS):
        if verificar_perfil_com_chromedriver(nome_perfil):
            try:
                profile = instaloader.Profile.from_username(loader.context, nome_perfil)
                break
            except instaloader.exceptions.ProfileNotExistsException:
                print(f"Perfil {nome_perfil} não encontrado.")
                return []
            except instaloader.exceptions.ConnectionException:
                print("Falha de conexão. Tentando novamente.")
                continue
    else:
        print("Falha ao conectar ao perfil após várias tentativas.")
        return []

    time.sleep(TEMPO_ESPERA_PERFIL)

    for post in profile.get_posts():
        if post.is_video and post.video_view_count >= min_views:
            for tentativa in range(MAX_TENTATIVAS):
                try:
                    print(f"Baixando vídeo do perfil {nome_perfil}: {post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}.mp4")
                    loader.download_post(post, target=pasta_destino)
                    video_salvos.append(post)
                    time.sleep(TEMPO_ESPERA_POST)
                    break
                except instaloader.exceptions.QueryReturnedBadRequestException as e:
                    if "401 Unauthorized" in str(e):
                        print("Erro 401 Unauthorized. Tentando novo proxy...")
                        continue
                    print(f"Erro ao baixar o vídeo: {e}")
                    break
                except Exception as e:
                    print(f"Erro desconhecido ao baixar o vídeo: {e}")
                    break

    return video_salvos if video_salvos else "Nenhum vídeo foi salvo."

def baixa():
    with open(caminho_perfis, 'r', encoding='utf-8') as perfis_file:
        perfis = [linha.strip() for linha in perfis_file.readlines()]

    todos_videos = []
    for perfil in perfis:
        print(f"Processando perfil: {perfil}")
        videos = baixar_apenas_videos_perfil(perfil, pasta,MIN_VIEW)
        if isinstance(videos, list):
            todos_videos.extend(videos)

        print("Esperando para o próximo perfil...")
        time.sleep(TEMPO_ESPERA_PERFIL)

    print("Todos os vídeos baixados:", todos_videos)
    dc.juntar_descricoes(pasta, arquivo_saida)
    print(f"Descrições salvas em: {arquivo_saida}")
    lp.remove_non_mp4_files(pasta)

if __name__ == "__main__":
    baixa()
