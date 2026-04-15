import httpx, json

# Busca datasets agro no basedosdados
q = '{ allDataset(first:20, search:"agropecuario") { edges { node { slug name tableList { name } } } } }'
r = httpx.post('https://backend.basedosdados.org/api/v1/graphql', json={'query': q}, timeout=15, verify=False)
d = r.json()
print("=== BasedosDados - Datasets agropecuário ===")
for edge in d['data']['allDataset']['edges']:
    n = edge['node']
    tables = [t['name'] for t in (n.get('tableList') or [])]
    print(f"  {n['slug']}: {n['name']}")
    for t in tables:
        print(f"    - {t}")

# Busca IBAMA, ambiente
q2 = '{ allDataset(first:15, search:"ibama") { edges { node { slug name tableList { name } } } } }'
r2 = httpx.post('https://backend.basedosdados.org/api/v1/graphql', json={'query': q2}, timeout=15, verify=False)
d2 = r2.json()
print("\n=== BasedosDados - IBAMA ===")
for edge in d2['data']['allDataset']['edges']:
    n = edge['node']
    tables = [t['name'] for t in (n.get('tableList') or [])]
    print(f"  {n['slug']}: {n['name']}")
    for t in tables:
        print(f"    - {t}")
