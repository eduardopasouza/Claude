import sys
from ckanapi import RemoteCKAN
import json

def explore_dadosgovbr():
    print("Iniciando conexão com API CKAN do Portal de Dados Abertos (dados.gov.br)...")
    try:
        # A API CKAN 3 original funciona bem na raiz
        dados_gov = RemoteCKAN('https://dados.gov.br/api/action')
    except Exception as e:
        # dados.gov.br costuma alternar os endpoints, fallback para http puro:
        print(f"Fallback. Erro inicial: {e}")
        import httpx
        url = "https://dados.gov.br/api/3/action/package_search"
        queries = ["agricultura", "silvicultura", "pecuaria", "cadastro ambiental rural", "outorga"]
        
        results_agg = {}
        with httpx.Client(verify=False) as client:
            for q in queries:
                print(f"Buscando termo: '{q}'...")
                r = client.get(url, params={"q": q, "rows": 15})
                if r.status_code == 200:
                    data = r.json()
                    count = data.get('result', {}).get('count', 0)
                    packages = data.get('result', {}).get('results', [])
                    
                    results_agg[q] = {
                        "total_found": count,
                        "samples": [pkg.get('title') for pkg in packages[:5]]
                    }
                    
        print("\n--- RESUMO DA MINERAÇÃO DADOS.GOV.BR ---")
        print(json.dumps(results_agg, indent=2, ensure_ascii=False))
        return

if __name__ == '__main__':
    explore_dadosgovbr()
