import os
import gdown
import zipfile
import subprocess
import time

DATA_DIR = "data/mapbiomas_credito"
GDRIVE_ID = "1tO0-qYUAQKRHJWrbYxO7VsUmwHLEn-TS"
ZIP_PATH = os.path.join(DATA_DIR, "mapbiomas_credito_rural.zip")

def download_and_extract():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 1. Download
    if not os.path.exists(ZIP_PATH):
        print("Iniciando download do Banco de Dados do MapBiomas Crédito Rural...")
        print(f"ID GDrive: {GDRIVE_ID}")
        gdown.download(id=GDRIVE_ID, output=ZIP_PATH, quiet=False)
    else:
        print("✅ Arquivo ZIP já baixado.")

    # 2. Extract
    print("Extraindo arquivos...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(DATA_DIR)
        print("✅ Extração concluída.")

    # 3. List files
    extracted_files = os.listdir(DATA_DIR)
    print("Conteúdo extraído:", extracted_files)

if __name__ == "__main__":
    download_and_extract()
