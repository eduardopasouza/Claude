import os
import subprocess
import time

# Script otimizado para ingerir vetores gigantes (GPKG de 4.7GB) diretamente no PostGIS via OGR2OGR (GDAL)
DB_HOST = "db"
DB_USER = "agrojus"
DB_PASS = "agrojus"
DB_NAME = "agrojus"

GPKG_PATH = "/app/data/mapbiomas_credito/mapbiomas_credito_rural.gpkg"
TABLE_NAME = "mapbiomas_credito_rural"

def load_gpkg_to_postgis():
    print(f"Iniciando Ingestão Massiva OGR2OGR -> Origem: {GPKG_PATH}")
    
    # Monta a connection string do PostGIS
    pg_conn = f"PG:host={DB_HOST} user={DB_USER} dbname={DB_NAME} password={DB_PASS}"

    # Flag -nln renomeia a tabela no destino
    # Flag -lco GEOMETRY_NAME define a coluna base de geometria
    # Flag -update -append pode ser usado, mas -overwrite limpa e recria
    command = [
        "ogr2ogr",
        "-f", "PostgreSQL",
        pg_conn,
        GPKG_PATH,
        "-nln", TABLE_NAME,
        "-lco", "GEOMETRY_NAME=geom",
        "-lco", "FID=id",
        "-nlt", "PROMOTE_TO_MULTI", # Para não misturar Polygon com MultiPolygon
        "-overwrite",
        "-progress"
    ]

    print("Comando gerado:", " ".join(command).replace(DB_PASS, "*****"))
    
    start_time = time.time()
    try:
        # Popen permite rodar assincronamente e capturar progresso se necessário
        process = subprocess.run(command, check=True)
        print("✅ Sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro executando ogr2ogr: {e}")
    
    print(f"Tempo total: {(time.time() - start_time) / 60:.2f} minutos")

if __name__ == '__main__':
    if os.path.exists(GPKG_PATH):
        load_gpkg_to_postgis()
    else:
        print(f"Erro: Arquivo Geopackage não encontrado em {GPKG_PATH}. Execute a rotina de download primeiro.")
