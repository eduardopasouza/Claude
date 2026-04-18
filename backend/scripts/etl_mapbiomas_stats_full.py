import os
import pandas as pd
from sqlalchemy import create_engine
import time

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")

def load_excel_to_db(file_path, sheet_name, table_name, engine):
    print(f"Lendo {file_path} - Sheet: {sheet_name}...")
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Converter nomes de colunas numéricas (anos) para string
        df.columns = [str(c) for c in df.columns]
        
        print(f"Salvando {len(df)} registros na tabela '{table_name}'...")
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"✅ Tabela {table_name} carregada com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao processar {file_path} > {sheet_name}: {e}")

if __name__ == "__main__":
    time.sleep(1)
    engine = create_engine(DATABASE_URL)
    
    # 1. Pastagem
    load_excel_to_db("data/mapbiomas_stats/PASTAGEM_COL9.xlsx", "PASTURE_VIGOR", "mapbiomas_pasture_vigor", engine)
    load_excel_to_db("data/mapbiomas_stats/PASTAGEM_COL9.xlsx", "PASTURE_AGE", "mapbiomas_pasture_age", engine)
    
    # 2. Mineração
    load_excel_to_db("data/mapbiomas_stats/MINERACAO_COL9.xlsx", "CITY_STATE_BIOME", "mapbiomas_mining_stats", engine)
    
    # 3. Cobertura (Total Biomas e Estados Col 10)
    load_excel_to_db("data/mapbiomas_stats/COBERTURA_BIOMAS_ESTADOS_COL10.xlsx", "COVERAGE_10", "mapbiomas_coverage_states", engine)

    print("ETL de Estatísticas Extras do MapBiomas finalizado.")
