import os

def juntar_descricoes(pasta_origem, arquivo_saida):
    with open(arquivo_saida, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(pasta_origem):
            if filename.endswith('.txt'):  # Verifica se o arquivo é um .txt
                caminho_arquivo = os.path.join(pasta_origem, filename)
                with open(caminho_arquivo, 'r', encoding='utf-8') as infile:
                    # Lê o conteúdo do arquivo e remove quebras de linha desnecessárias
                    conteudo = infile.read().strip().replace('\n', ' ')
                    outfile.write(conteudo + '\n')  # Adiciona uma nova linha após cada descrição

juntar_descricoes(r"C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\POWER-BOT\VIDEOS",r"C:\Users\julio\OneDrive\Documentos\BOOT-TIKTPK\BOOT-TIKTPK\POWER-BOT\Auto\DESCRIÇAO\descricao.txt")