"""Testa o schema GraphQL correto do BasedosDados.org"""
import httpx, json

BD = "https://backend.basedosdados.org/api/v1/graphql"
H  = {"Content-Type": "application/json"}

queries = [
    # Testa campos disponíveis
    ('slug simples',      '{allDataset(first:3, slug_Icontains: "ibge_pam") {edges {node {slug name}}}}'),
    ('pam sem status',    '{allDataset(first:5, slug_Icontains: "agropecuario") {edges {node {slug name tables {edges {node {name numberRows}}}}}}}'),
    ('ibge censo',        '{allDataset(first:5, slug_Icontains: "censo") {edges {node {slug name tables {edges {node {name numberRows}}}}}}}'),
    ('meio ambiente',     '{allDataset(first:5, slug_Icontains: "ibama") {edges {node {slug name tables {edges {node {name numberRows}}}}}}}'),
    ('trabalho escravo',  '{allDataset(first:5, slug_Icontains: "trabalho") {edges {node {slug name tables {edges {node {name numberRows}}}}}}}'),
    ('credito rural',     '{allDataset(first:5, slug_Icontains: "credito") {edges {node {slug name tables {edges {node {name numberRows}}}}}}}'),
    ('cnpj receita',      '{allDataset(first:5, slug_Icontains: "cnpj") {edges {node {slug name tables {edges {node {name numberRows}}}}}}}'),
    ('sicar car',         '{allDataset(first:5, slug_Icontains: "sicar") {edges {node {slug name tables {edges {node {name numberRows}}}}}}}'),
    ('pronaf',            '{allDataset(first:5, slug_Icontains: "pronaf") {edges {node {slug name tables {edges {node {name numberRows}}}}}}}'),
    ('pam producao',      '{allDataset(first:5, name_Icontains: "Producao Agricola") {edges {node {slug name tables {edges {node {name numberRows}}}}}}}'),
]

found = {}
with httpx.Client(timeout=15, verify=False) as c:
    for label, q in queries:
        r = c.post(BD, json={"query": q}, headers=H)
        if r.status_code != 200:
            print(f"[{label}] HTTP {r.status_code}")
            continue
        data = r.json()
        edges = data.get("data", {}).get("allDataset", {}).get("edges", [])
        if edges:
            print(f"\n[{label}] {len(edges)} datasets:")
            for e in edges:
                n = e["node"]
                tables = n.get("tables", {}).get("edges", [])
                print(f"  {n['slug']}  ({len(tables)} tabelas)")
                for t in tables[:3]:
                    rows = t["node"].get("numberRows", "?")
                    print(f"    └ {t['node']['name']} — {rows} linhas")
                    key = f"{n['slug']}.{t['node']['name']}"
                    found[key] = rows
        else:
            print(f"[{label}] sem resultados")

print(f"\n{'='*60}")
print(f"TOTAL ENCONTRADO: {len(found)} tabelas")
print("TOP 15 por volume:")
for k, v in sorted(found.items(), key=lambda x: x[1] or 0, reverse=True)[:15]:
    print(f"  basedosdados.{k}  — {v}")
