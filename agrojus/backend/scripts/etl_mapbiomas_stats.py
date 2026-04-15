import os
import pandas as pd
from sqlalchemy import create_engine
import time

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")

def load_excel_to_db(file_path, sheet_name, table_name, engine):
    print(f"Lendo {file_path} - Sheet: {sheet_name}...")
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Converter nomes de colunas numéricas (anos) para string para evitar problemas no banco
        df.columns = [str(c) for c in df.columns]
        
        print(f"Colunas: {df.columns.tolist()[:10]}...")
        print(f"Salvando {len(df)} registros na tabela '{table_name}'...")
        
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"✅ Tabela {table_name} carregada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")

if __name__ == "__main__":
    time.sleep(2)  # Wait for DB to be ready if in docker compose
    engine = create_engine(DATABASE_URL)
    
    # 1. Agricultura (Irrigação)
    load_excel_to_db(
        "data/mapbiomas_stats/AGRICULTURA_COL9.xlsx", 
        "CITY_STATE_BIOME_IRRIGATION", 
        "mapbiomas_irrigation_stats", 
        engine
    )

    # 1.1 Agricultura (Ciclos)
    load_excel_to_db(
        "data/mapbiomas_stats/AGRICULTURA_COL9.xlsx", 
        "CITY_STATE_BIOME_NUMBER_CYCLES", 
        "mapbiomas_agriculture_cycles", 
        engine
    )
    
    # NOTE: To load coverage and pasture, we would check their sheet names.
    # We will log completion.
    print("ETL de Estatísticas MapBiomas finalizado.")
