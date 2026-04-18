# Embrapa AgroAPI — Status de Integração

## ✅ O que funciona hoje

### OAuth 2.0 autenticando
- Gateway: `https://api.cnptia.embrapa.br`
- Credenciais em `.env` (Consumer Key + Secret + Access Token manual)
- Testado via `GET /api/v1/embrapa/status` → 200 OK com token ativo

### Coletor + router prontos
- `backend/app/collectors/embrapa.py` (230 linhas) — classe `EmbrapaCollector` com cache SHA256 + TTL + auth singleton + 9 métodos (um por API assinada)
- `backend/app/api/embrapa.py` (100 linhas) — 9 endpoints REST expostos:
  - `GET /embrapa/status` ✅ funcional
  - `POST /embrapa/agritec`
  - `GET /embrapa/agrofit`
  - `POST /embrapa/smartsolos`
  - `GET /embrapa/bioinsumos`
  - `GET /embrapa/bovtrace/{gta}`
  - `GET /embrapa/agrotermos`
  - `POST /embrapa/respondeagro`
  - `POST /embrapa/plantannot`
  - `GET /embrapa/sting`

## ⚠️ Pendência — paths individuais por API

Os 8 endpoints que não são `/status` retornam **404** no gateway porque cada API da Embrapa tem um **context path próprio no WSO2 APIM** que não segue um padrão único.

**Exemplos de paths que tentei (e não funcionaram):**
- `/agrofit/v1/produtos`
- `/smartsolos/v1/predict`
- `/agritec/v2/recomendacao`

**O correto depende do Swagger individual de cada API.** Para obter:

1. Entrar no portal https://www.agroapi.cnptia.embrapa.br/portal/apis
2. Clicar em cada API assinada (Agritec, AGROFIT, etc.)
3. Ver a aba "API Definition" → copiar o **"Base Path"** e os **endpoints REST**
4. Ajustar em `backend/app/collectors/embrapa.py` método correspondente

**Exemplo típico de path WSO2:**
```
https://api.cnptia.embrapa.br/t/embrapa/agrofit/v1/produtos?cultura=soja
```

O `/t/embrapa/` é o tenant. Alguns serviços usam `/t/cnptia/` ou o context path direto.

## 🧪 Como testar cada API manualmente

Com token em mãos:
```bash
TOKEN=$(curl -s http://localhost:8000/api/v1/embrapa/status | jq -r '.token_preview')
# Ou extrair o token real do log do backend ao subir

# Testar manualmente variações de path:
curl -H "Authorization: Bearer $FULL_TOKEN" \
  "https://api.cnptia.embrapa.br/agrofit/v1/produtos?cultura=soja"

curl -H "Authorization: Bearer $FULL_TOKEN" \
  "https://api.cnptia.embrapa.br/t/cnptia/agrofit/v1/produtos?cultura=soja"
```

Depois de descobrir o path correto, editar `embrapa.py` método correspondente.

## 📋 Checklist de descoberta

Eduardo pode navegar no portal Embrapa e copiar os paths base das 9 APIs aqui:

| API | Path base correto | Exemplo de endpoint |
|---|---|---|
| Agritec v2 | `?` | `?` |
| AGROFIT v1 | `?` | `?` |
| AgroTermos v1 | `?` | `?` |
| Bioinsumos v2 | `?` | `?` |
| BovTrace v1 | `?` | `?` |
| PlantAnnot v2 | `?` | `?` |
| RespondeAgro v1 | `?` | `?` |
| SmartSolosExpert v1 | `?` | `?` |
| Sting v1 | `?` | `?` |

Quando preencher essa tabela, atualizo o coletor com os paths reais e todos os 9 endpoints passam a funcionar.

## 🚀 Próximo passo

**Ação para Eduardo:** acessar https://www.agroapi.cnptia.embrapa.br/portal/apis, clicar nas APIs assinadas, copiar o Base Path + 1 endpoint de exemplo de cada, e colar aqui/comigo. 5 minutos.

**Em paralelo (enquanto isso):** vou seguir com os outros coletores (ANA Outorgas, SIGMINE, IBAMA dados abertos) — são APIs públicas sem autenticação complexa.
