import httpx
import json

def test_mapbiomas_alerta():
    url = "https://plataforma.alerta.mapbiomas.org/api/v2/graphql"
    query = """
    query {
      alerts(limit: 5) {
        alertCode
        areaHa
        detectedAt
        municipality
        state
        biome
      }
    }
    """
    print("Testando conexão com MapBiomas Alerta GraphQL...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = httpx.post(url, json={"query": query}, headers=headers, timeout=30.0)
        print(f"Status da resposta: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print("Erros na query:")
                print(json.dumps(data["errors"], indent=2))
            else:
                print("Sucesso! Alertas retornados:")
                print(json.dumps(data["data"]["alerts"], indent=2, ensure_ascii=False))
        else:
            print("Erro ao acessar API:")
            print(response.text)
    except Exception as e:
        print(f"Falha na requisição: {e}")

if __name__ == "__main__":
    test_mapbiomas_alerta()
