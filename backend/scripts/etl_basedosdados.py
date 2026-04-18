import basedosdados as bd
import os

# Você precisa fornecer um Billing Project do Google Cloud para rodar as queries (Mesmo de graça, o GCP exige o projeto de cobrança configurado)
BILLING_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "agrojus-data-2026")

def search_agro_datasets():
    print(f"Iniciando Mapeamento via Google BigQuery no Base dos Dados...")
    print(f"Project ID logado: {BILLING_PROJECT_ID}")
    
    # Query na super-tabela do IBGE (Produção Agrícola Municipal - PAM)
    query = """
    SELECT 
        sigla_uf,
        id_municipio,
        produto,
        ano,
        area_plantada,
        valor_producao
    FROM `basedosdados.br_ibge_pam.municipio_lavoura_permanente`
    WHERE ano = (SELECT MAX(ano) FROM `basedosdados.br_ibge_pam.municipio_lavoura_permanente`)
    LIMIT 10
    """
    
    try:
        print("\nExecutando query no Data Lake da Receita/IBGE...")
        # A API bd.read_sql puxa tudo para um DataFrame do pandas automaticamente!
        df = bd.read_sql(query, billing_project_id=BILLING_PROJECT_ID)
        
        print("\n=== Amostra de Produção Agrícola por Município (PAM/IBGE) ===")
        print(df.head())
        print("Integração BigQuery / BaseDosDados concluída estruturalmente.")
        
    except Exception as e:
        print(f"\n⚠️ O BigQuery requer autenticação (Arquivo JSON do Cloud SDK ou Application Default Credentials).")
        print(f"Detalhe do erro: {e}")
        print("A superstrutura para o Motor SQL da Base dos Dados está pavimentada.")

if __name__ == '__main__':
    search_agro_datasets()
