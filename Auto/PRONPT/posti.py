import os
import logging
import time
import subprocess
from random import shuffle, choice
import emoji

def iniciar_vm(nome_vm):
    try:
        subprocess.run(['quickemu', '--vm', nome_vm], check=True)
        print(f"VM {nome_vm} iniciada com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao iniciar a VM {nome_vm}: {e}")

def posta(conta):
    # Configuração do log
    logging.basicConfig(level=logging.INFO, filename='upload_log.txt', filemode='a', 
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Caminhos dos arquivos e pastas
    pasta_videos = r'C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\POWER-BOT\VIDEOS'
    descricao_path = r'C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\POWER-BOT\Auto\DESCRIÇAO\descricao.txt'
    linha_contador_path = r'C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\POWER-BOT\Auto\CONTADOR\LINHA_CONTADOR.TXT'
    
    TEMPO_ESPERA = 30  # Ajuste do tempo para evitar bloqueio de requisições
    MAX_TENTATIVAS = 3  # Número máximo de tentativas para upload de cada vídeo

    # Garante que o diretório do contador exista
    os.makedirs(os.path.dirname(linha_contador_path), exist_ok=True)

    # Carrega descrições do arquivo
    def carregar_descricoes(caminho):
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as descri:
                return [linha.strip() for linha in descri.readlines() if linha.strip()]
        return []

    # Obter vídeos e descrições
    videos = [f for f in os.listdir(pasta_videos) if f.endswith('.mp4')]
    descricoes = carregar_descricoes(descricao_path)

    # Embaralha a lista de vídeos
    shuffle(videos)

    for video in videos[:10]:  # Processa até 10 vídeos por execução
        video_path = os.path.join(pasta_videos, video)
        logging.info(f"Fazendo upload de: {video_path}")
        print(f"Fazendo upload de: {video_path}")

        # Inicia a VM para este upload
       # nome_vm = 'sua_vm'  # Defina o nome da sua VM aqui
       # iniciar_vm(nome_vm)

        # Ignora vídeos vazios ou muito pequenos
        video_size = os.path.getsize(video_path)
        if video_size == 0 or video_size < 1024:
            logging.warning(f"O vídeo {video} está vazio ou muito pequeno e será ignorado.")
            continue

        # Seleciona uma descrição
        if descricoes:
            descricao = descricoes.pop(0)  # Pega a primeira descrição e remove da lista
        else:
            descricoes_padrao = [
                "Link in bio\n #Product #Find #Gift #GreatFind",
                "Check the link in bio!\n #NewArrival #Promotion",
                "Don't miss this amazing offer! Link in bio!\n #Discount #Unmissable"
            ]
            descricao = choice(descricoes_padrao)
        
        # Adiciona emojis à descrição
        descricao = emoji.emojize(descricao)
        logging.info(f"Iniciando upload do vídeo: {video_path} com descrição: {descricao}")

        # Tentativas de upload com pausa entre falhas
        for tentativa in range(1, MAX_TENTATIVAS + 1):
            try:
                subprocess.run([
                    'python', 
                    r'C:\Users\julio\OneDrive\Documentos\GitHub\TiktokAutoUploader\cli.py', 
                    'upload', 
                    '-u', 
                    conta, 
                    '-v', 
                    video_path,
                    '-t', 
                    descricao
                ], check=True, encoding='utf-8')

                logging.info(f"Upload concluído para: {video}")
                print(f"Upload concluído para: {video}")

                # Exclui o vídeo após upload bem-sucedido
                os.remove(video_path)
                logging.info(f"Vídeo excluído: {video_path}")
                print(f"Vídeo excluído: {video_path}")
                break  # Sai do loop de tentativas se o upload for bem-sucedido

            except subprocess.CalledProcessError as e:
                logging.error(f"Erro ao fazer upload de {video} (tentativa {tentativa}): {e}")
                print(f"Erro ao fazer upload de {video} (tentativa {tentativa}): {e}")
                if tentativa < MAX_TENTATIVAS:
                    logging.info(f"Aguardando {TEMPO_ESPERA} segundos antes de nova tentativa.")
                    time.sleep(TEMPO_ESPERA)
                else:
                    logging.error(f"Máximo de tentativas atingido para {video}. Pulando para o próximo vídeo.")
        
        # Atualiza o contador
        try:
            with open(linha_contador_path, 'r+') as file:
                try:
                    contador = int(file.read().strip())
                except ValueError:
                    contador = 0  # Caso não haja número válido, inicializa como 0
                file.seek(0)
                file.write(str(contador + 1))
                file.truncate()
        except FileNotFoundError:
            with open(linha_contador_path, 'w') as file:
                file.write('1')

        # Aguarda antes do próximo upload
        time.sleep(TEMPO_ESPERA)

if __name__ == "__main__":
    posta('contaone')
