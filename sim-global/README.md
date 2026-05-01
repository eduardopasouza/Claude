# sim-global

Simulador histórico-estratégico turn-based local. Frontend visual
mobile-friendly no browser, backend Python, motor narrativo via
Claude Opus 4.7 com OAuth da assinatura Claude Pro/Max — sem API key
paga, sem cloud externa.

Documentação completa em [`BRIEFING.md`](BRIEFING.md) (estratégia) e
[`CLAUDE.md`](CLAUDE.md) (constituição operacional).

## Como rodar

```bash
# instalar dependências
cd backend
pip install -e ".[dev]"

# rodar
python -m simglobal
# → backend sobe em http://localhost:8000
# → browser abre automaticamente
```

A integração com Claude Agent SDK (motor narrativo) entra em fase
posterior. Antes dela:

```bash
claude setup-token                    # uma vez, gera token longo
export CLAUDE_CODE_OAUTH_TOKEN=...    # exporte ou ponha em .env
```

## Jogar pelo celular (Tailscale)

A UI é responsiva: bottom tabs no celular (Mapa | Polity | Eventos |
Diplo | Advisor), layout 3-col no desktop. Para acessar o backend a
partir do celular **de qualquer lugar**, sem expor o PC publicamente:

1. Crie conta gratuita em [tailscale.com](https://tailscale.com).
2. Instale Tailscale no PC que vai rodar o backend e no seu celular.
   Faça login na mesma conta nos dois.
3. No `config.yaml`, troque `server.host` para `0.0.0.0`.
4. Rode o backend: `python -m simglobal`.
5. No app Tailscale do celular, copie o IP do PC (ex.: `100.x.y.z`).
6. Abra no navegador do celular: `http://100.x.y.z:8000`.
7. (Opcional) Adicione à tela inicial do celular para virar PWA
   instalável (manifest.json + service worker já configurados).

Para jogar **só em casa, na mesma WiFi**, pule Tailscale e use o IP
local do PC (ex.: `192.168.1.10`). A regra `host: 0.0.0.0` continua
necessária. Cuidado: 0.0.0.0 expõe na rede inteira; só use em redes
confiáveis ou atrás de Tailscale.

## Estrutura

```
sim-global/
├── backend/                # Python: FastAPI + simengine + Agent SDK
├── frontend/               # HTMX + Alpine.js + Tailwind via CDN
├── data/                   # mapa Natural Earth + bandeiras + retratos
├── examples/               # cenários-piloto (Brasil/1930)
└── saves/                  # SQLite local (gitignored)
```

## Cenário de exemplo

[`examples/brasil-vargas-1930/`](examples/brasil-vargas-1930/) é o
cenário-piloto: Brasil em 03/11/1930 (posse de Vargas), 10 regiões
brasileiras + 10 polities-bloco externas, 30 eventos pré-programados
até 1945. Lore com fontes citadas em Wikipedia, IBGE, FGV CPDOC e
Biblioteca Nacional Digital. Serve como fixture de teste e como
referência de formato esperado pelo `scenario_builder`.

## Status

Em construção. Roadmap em [`BRIEFING.md`](BRIEFING.md) §10. Acompanhe
em `git log --oneline`.
