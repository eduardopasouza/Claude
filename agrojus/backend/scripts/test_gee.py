import ee
import sys

def test_earth_engine():
    print("Iniciando teste de conexão à API do Google Earth Engine...")
    
    try:
        # A inicialização básica busca credenciais no env
        ee.Initialize()
        print("✅ Sucesso! Google Earth Engine inicializado com as credenciais locais.")
        
        # Tenta carregar o raster da Cobertura MapBiomas
        print("Tentando carregar metadados da Coleção 10.1 do MapBiomas no GEE...")
        mapbiomas_col_10 = ee.Image("projects/mapbiomas-public/assets/brazil/lulc/collection10_1/mapbiomas_brazil_collection10_1_coverage_v1")
        bands = mapbiomas_col_10.bandNames().getInfo()
        print(f"✅ Bandas carregadas com sucesso! Anos disponíveis: {len(bands)}")
        print(f"Primeiros anos da série histórica: {bands[:5]}")
        
    except Exception as e:
        print("❌ Falha na inicialização do Earth Engine.")
        print("Erro relatado:", e)
        print("\nPara resolver no AgroJus (Docker):")
        print("Você precisa gerar uma Service Account no Google Cloud com a API GEE habilitada.")
        print("Salve o JSON em 'backend/credentials/gee_key.json' e defina a variável:")
        print("export GOOGLE_APPLICATION_CREDENTIALS=\"/app/credentials/gee_key.json\"")
        print("Ou rode interativamente: docker exec -it agrojus-backend-1 earthengine authenticate --auth_mode=notebook")

if __name__ == "__main__":
    test_earth_engine()
