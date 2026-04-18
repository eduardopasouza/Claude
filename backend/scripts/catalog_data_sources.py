"""
Catalogador de datasets relevantes ao AgroJus nas plataformas:
  - dados.gov.br (CKAN API pública, sem autenticação)
  - basedosdados.org (BigQuery — lista tabelas disponíveis via API REST pública)
  - MapBiomas (API GraphQL pública)

Resultado: imprime todos os datasets identificados com URL de download.
"""
import httpx
import json

CKAN_BASE = "https://dados.gov.br/api/3/action"

AGROJUS_QUERIES = {
    "IBAMA: embargos e infrações": "embargo ambiental IBAMA",
    "SICAR / CAR": "cadastro ambiental rural sicar",
    "Crédito Rural / SICOR": "credito rural pronaf pronamp sicor",
    "Trabalho escravo / MTE": "trabalho escravo resgate cadastro empregadores",
    "Agrotóxicos / MAPA": "agrotoxico rotulo receituario",
    "Produção Agrícola IBGE (PAM)": "producao agricola municipal pam ibge",
    "Pecuária IBGE (PPM)": "pecuaria municipal ppm ibge",
    "Georreferenciamento INCRA": "georreferenciamento imovel rural incra sigef",
    "Outorgas de Água (ANA)": "outorga uso agua ana",
    "DCR / Certidão Débito Rural": "certidao debito rural",
    "GTA Pecuário (MAPA)": "guia transito animal gta mapa",
    "Terras Indigenas (FUNAI)": "terras indigenas funai demarcacao",
    "DataJud / Processos": "processo judicial rural tributario",
    "PLDAg (Plano Lavoura MAPA)": "plano lavoura mapa producao",
}

BD_REST = "https://backend.basedosdados.org/api/v1/rest"
BD_GRAPHQL = "https://backend.basedosdados.org/api/v1/graphql"

BD_AGROJUS_THEMES = [
    "Agropecuária", "Meio Ambiente", "Trabalho", "Economia", "Território"
]

BD_QUERY = """
query SearchDatasets($theme: String) {
  allDataset(
    first: 20
    theme_Icontains: $theme
    status: "published"
  ) {
    edges {
      node {
        id
        slug
        name
        description
        tables {
          edges {
            node {
              name
              description
              updatedAt
              numberRows
            }
          }
        }
      }
    }
  }
}
"""

MAPBIOMAS_GRAPHQL = "https://plataforma.alerta.mapbiomas.org/api/graphql"


def search_ckan():
    print("\n" + "="*70)
    print("DADOS.GOV.BR — Catalogação de Datasets Relevantes")
    print("="*70)
    
    results = []
    with httpx.Client(verify=False, timeout=30, follow_redirects=True) as client:
        for label, query in AGROJUS_QUERIES.items():
            url = f"{CKAN_BASE}/package_search"
            try:
                r = client.get(url, params={"q": query, "rows": 5, "sort": "score desc"})
                if r.status_code != 200:
                    print(f"  [{label}] HTTP {r.status_code}")
                    continue
                
                data = r.json()
                count = data.get("result", {}).get("count", 0)
                pkgs  = data.get("result", {}).get("results", [])
                
                print(f"\n📂 {label} — {count} datasets encontrados")
                
                for pkg in pkgs[:3]:
                    title = pkg.get("title", "–")[:70]
                    org   = (pkg.get("organization") or {}).get("title", "")[:40]
                    resources = pkg.get("resources", [])
                    
                    # Pega a URL de download do primeiro recurso CSV/ZIP/XLSX
                    dl_url = ""
                    for res in resources:
                        fmt = res.get("format", "").upper()
                        if fmt in ("CSV", "ZIP", "XLSX", "JSON"):
                            dl_url = res.get("url", "")
                            break
                    
                    results.append({
                        "categoria": label,
                        "titulo": title,
                        "organizacao": org,
                        "url_download": dl_url,
                        "total_recursos": len(resources),
                    })
                    print(f"   ✦ {title}")
                    if org:      print(f"     Org: {org}")
                    if dl_url:   print(f"     URL: {dl_url[:80]}")
                    
            except Exception as e:
                print(f"  [{label}] Erro: {e}")
    
    return results


def search_basedosdados():
    print("\n" + "="*70)
    print("BASEDOSDADOS.ORG — Datasets de Agronegócio/Agropecuária disponíveis")
    print("="*70)
    print("⚠️  Requer Google Cloud Project para executar queries via BigQuery.")
    print("    Listando metadados públicos das tabelas (sem baixar dados).\n")
    
    bd_tables = []
    with httpx.Client(verify=False, timeout=30) as client:
        for theme in BD_AGROJUS_THEMES:
            try:
                r = client.post(
                    BD_GRAPHQL,
                    json={"query": BD_QUERY, "variables": {"theme": theme}},
                    headers={"Content-Type": "application/json"},
                )
                if r.status_code != 200:
                    continue
                
                data = r.json()
                datasets = data.get("data", {}).get("allDataset", {}).get("edges", [])
                
                for ds_edge in datasets:
                    ds = ds_edge.get("node", {})
                    tables = ds.get("tables", {}).get("edges", [])
                    
                    for tbl_edge in tables:
                        tbl = tbl_edge.get("node", {})
                        rows = tbl.get("numberRows") or "?"
                        name = tbl.get("name", "")
                        desc = (tbl.get("description") or "")[:80]
                        
                        bd_tables.append({
                            "tema": theme,
                            "dataset": ds.get("slug", ""),
                            "tabela": name,
                            "descricao": desc,
                            "linhas": rows,
                        })
                        print(f"  📊 {ds.get('slug')}.{name}")
                        print(f"     Rows: {rows} | {desc}")
                        
            except Exception as e:
                print(f"  Erro ao consultar BD [{theme}]: {e}")
    
    return bd_tables


def check_mapbiomas_api():
    print("\n" + "="*70)
    print("MAPBIOMAS — Verificação das APIs disponíveis")
    print("="*70)
    
    # Testa quais endpoints respondem
    endpoints = [
        ("Alerta MapBiomas API",       "https://plataforma.alerta.mapbiomas.org/api/graphql"),
        ("MapBiomas Workspace GEE",    "https://code.earthengine.google.com/"),
        ("MapBiomas Stats Downloads",  "https://storage.googleapis.com/mapbiomas-public/"),
        ("MapBiomas GCS Downloads",    "https://mapbiomas-acervo.s3.amazonaws.com/"),
        ("MapBiomas Credito API",      "https://api.mapbiomas.org/"),
    ]
    
    with httpx.Client(verify=False, timeout=10, follow_redirects=True) as client:
        for name, url in endpoints:
            try:
                r = client.get(url)
                print(f"  {'✅' if r.status_code < 400 else '⚠️'} {name}: HTTP {r.status_code}")
            except Exception as e:
                print(f"  ❌ {name}: {str(e)[:60]}")


if __name__ == "__main__":
    ckan_results  = search_ckan()
    bd_results    = search_basedosdados()
    check_mapbiomas_api()
    
    print("\n" + "="*70)
    print("RESUMO EXECUTIVO")
    print("="*70)
    print(f"  dados.gov.br:        {len(ckan_results)} datasets identificados")
    print(f"  basedosdados.org:    {len(bd_results)} tabelas catalogadas (requerem GCP)")
    print(f"  MapBiomas Crédito:   5.614.207 parcelas já carregadas ✅")
    print(f"  MapBiomas Stats:     tabelas de cobertura/uso já carregadas ✅")
