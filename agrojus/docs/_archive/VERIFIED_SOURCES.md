# AgroJus — Fontes de Dados Verificadas

**Última validação: 2026-04-11 14:01 (BRT)**
**Validado por: Supra Gerente (Antigravity)**

## Resumo

| Status | Qtde |
|--------|------|
| ✅ Online (200) | 11 |
| ⚠️ Parcial (400) | 1 |
| ❌ Offline/Erro | 1 |
| **Total** | **13** |

## Detalhamento

| # | Fonte | URL | Status | Código | Notas |
|---|-------|-----|--------|--------|-------|
| 1 | BrasilAPI (CNPJ) | brasilapi.com.br/api/cnpj/v1 | ✅ Online | 200 | Livre, sem key |
| 2 | FUNAI WFS (Terras Indígenas) | geoserver.funai.gov.br | ✅ Online | 200 | WFS público |
| 3 | INPE TerraBrasilis (PRODES) | terrabrasilis.dpi.inpe.br | ✅ Online | 200 | WFS público |
| 4 | IBGE API (Localidades) | servicodados.ibge.gov.br | ✅ Online | 200 | REST público |
| 5 | IBGE SIDRA (Produção) | apisidra.ibge.gov.br | ✅ Online | 200 | REST público |
| 6 | BCB API (Indicadores) | api.bcb.gov.br | ✅ Online | 200 | REST público |
| 7 | BCB SICOR (Crédito Rural) | olinda.bcb.gov.br/SICOR | ⚠️ Parcial | 400 | OData — requer parâmetros corretos, endpoint acessível |
| 8 | NASA POWER (Clima) | power.larc.nasa.gov | ✅ Online | 200 | REST público, coords obrigatórias |
| 9 | ANM GeoServer (Mineração) | geo.anm.gov.br | ✅ Online | 200 | ArcGIS REST |
| 10 | ANEEL SIGEL (Energia) | sigel.aneel.gov.br | ✅ Online | 200 | Portal web |
| 11 | Nominatim/OSM (Geocoding) | nominatim.openstreetmap.org | ✅ Online | 200 | Rate limit 1 req/s |
| 12 | SICAR/CAR (Ambiental) | car.gov.br | ❌ Offline | ConnectError | Servidor não responde — monitorar |
| 13 | SIGEF/INCRA (Georreferenciamento) | sigef.incra.gov.br | ✅ Online | 200 | URL corrigida — estava com 404, agora funciona |

## DataJud/CNJ — Situação Especial

- **Endpoint**: `api-publica.datajud.cnj.jus.br`
- **Status**: API aberta, sem autenticação necessária
- **Problema encontrado**: Retorna HTTP 401 em chamadas POST (necessário verificar formato da query Elasticsearch)
- **Ação**: Backend Dev deve ajustar headers/auth no DataJudCollector

## Próxima Validação

Revalidar em: 2026-04-18 (semanal)
Responsável: Pesquisador ou Supra Gerente
