import os
import requests
import zipfile
import logging
from urllib.parse import urlparse

# Setup Logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')
logger = logging.getLogger('DataFetcher')

# Diretórios Principais
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOWNLOADS_DIR = os.path.join(BASE_DIR, 'data', 'downloads')

DIRECTORIES = {
    'ibama': os.path.join(DOWNLOADS_DIR, 'ibama'),
    'mte': os.path.join(DOWNLOADS_DIR, 'mte'),
    'funai': os.path.join(DOWNLOADS_DIR, 'funai'),
    'mapbiomas': os.path.join(DOWNLOADS_DIR, 'mapbiomas')
}

# Endpoints
ENDPOINTS = [
    {
        'name': 'IBAMA Embargos (SICAFI)',
        'url': 'https://dadosabertos.ibama.gov.br/dados/SICAFI/embargo/Embargo.csv',
        'dir': 'ibama',
        'filename': 'Embargo.csv'
    },
    {
        'name': 'IBAMA Autuações (SICAFI)',
        'url': 'https://dadosabertos.ibama.gov.br/dados/SICAFI/autuacao/Autuacao.csv',
        'dir': 'ibama',
        'filename': 'Autuacao.csv'
    },
    {
        'name': 'MTE Trabalho Escravo (Descompactação Pendente)',
        'url': 'https://codigos.portaldatransparencia.gov.br/api/de-de/download-de-dados/trabalho-escravo/202312',
        'dir': 'mte',
        'filename': 'trabalho_escravo_latest.zip'
    }
]

def make_dirs():
    """Garante que as subpastas estruturais existam."""
    for key, path in DIRECTORIES.items():
        os.makedirs(path, exist_ok=True)
        # Cria README de instrução no MapBiomas
        if key == 'mapbiomas':
            readme = os.path.join(path, '_INSTRUCOES_MAPBIOMAS.txt')
            if not os.path.exists(readme):
                with open(readme, 'w', encoding='utf-8') as f:
                    f.write("=== MAPBIOMAS MANUAL DOWNLOAD FOLDER ===\n")
                    f.write("Por favor, solte todos os TIFs, Geopackages e as Estatísticas CSV (Raster/Vetorial) nesta pasta!\n")
                    f.write("O backend do AgroJus irá escanear estas pastas para ingestão via GeoPandas.\n")
    logger.info("Estrutura de diretórios criada e verificada com sucesso.")

def download_file(url, dest_path, name):
    """Realiza o download massivo com streaming (otimizado para Gigabit)."""
    if os.path.exists(dest_path):
        logger.info(f"O arquivo {name} já existe. Ignorando download para poupar banda.")
        return

    logger.info(f"Iniciando download de {name}...")
    try:
        # User-Agent spoofing se os portais do Gov estiverem bloqueando python-requests cru
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        with requests.get(url, stream=True, headers=headers) as r:
            r.raise_for_status()
            total_length = r.headers.get('content-length')
            
            with open(dest_path, 'wb') as f:
                if total_length is None:
                    # Nenhum content-length, baixa do mesmo jeito
                    f.write(r.content)
                else:
                    downloaded = 0
                    total = int(total_length)
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            downloaded += len(chunk)
                            f.write(chunk)
                            # Progresso silencioso
        logger.info(f"✔ Download Completo: {name} ({os.path.getsize(dest_path) // 1024 // 1024} MB)")
    except Exception as e:
        logger.error(f"Falha ao baixar {name}: {e}")

def run():
    logger.info("=== AgroJus: Iniciando Robô de Intake de Dados Públicos ===")
    make_dirs()
    
    for item in ENDPOINTS:
        out_file = os.path.join(DIRECTORIES[item['dir']], item['filename'])
        download_file(item['url'], out_file, item['name'])
        
    logger.info("Processo concluído. Arquivos estáticos injetados na pasta Download.")

if __name__ == '__main__':
    run()
