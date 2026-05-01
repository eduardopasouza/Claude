# sim-global

Simulador histórico-estratégico turn-based local. Frontend visual
mobile-friendly no browser, backend Python, motor narrativo via
Claude Opus 4.7 com OAuth da assinatura Claude Pro/Max — sem API key
paga, sem cloud externa.

Documentação completa em [`BRIEFING.md`](BRIEFING.md) (estratégia) e
[`CLAUDE.md`](CLAUDE.md) (constituição operacional).

## Como rodar

```bash
# 1. autenticação Claude (uma vez, abre browser)
claude setup-token
export CLAUDE_CODE_OAUTH_TOKEN=<o token impresso pelo setup-token>

# 2. instalar dependências (com o agent SDK)
cd backend
pip install -e ".[dev,agent]"

# 3. (opcional) rodar migrations Alembic em vez de init_db automático
SIMGLOBAL_DATABASE_URL=sqlite:///../saves/simglobal.db alembic upgrade head

# 4. rodar
python -m simglobal
# → backend sobe em http://localhost:8000
# → browser abre automaticamente
# → SQLite em saves/simglobal.db é criado e o cenário Brasil/1930 é
#   importado automaticamente na primeira execução.
```

Sem `CLAUDE_CODE_OAUTH_TOKEN`/`claude-agent-sdk` instalados, o app
funciona em modo **leitura**: você navega o cenário, vê mapa e
painéis, mas os endpoints `/api/.../turn`, `/advise` e `/dm`
respondem 503 com instrução clara.

## Endpoints principais

| Método | Rota                                 | Função                                     |
| ------ | ------------------------------------ | ------------------------------------------ |
| GET    | `/api/health`                        | status do backend e do agente              |
| GET    | `/api/campaigns`                     | lista campanhas no SQLite                  |
| POST   | `/api/campaigns/import-example`      | importa cenário-piloto (`brasil-vargas-1930`) |
| POST   | `/api/campaigns/new`                 | cria campanha procedural via scenario_builder |
| GET    | `/api/campaigns/{name}/state`        | estado completo (GameState)                |
| POST   | `/api/campaigns/{name}/turn`         | avança N meses (game_master)               |
| POST   | `/api/campaigns/{name}/advise`       | pergunta ao advisor                        |
| POST   | `/api/campaigns/{name}/dm`           | envia mensagem diplomática (diplomat)      |
| DELETE | `/api/campaigns/{name}`              | apaga campanha                             |

## Deploy público (cloud externa)

Você pediu URL pública. Eu não posso deployar por você (a inferência
consome quota da **sua** assinatura Pro/Max via OAuth). Mas o repo
já tem **3 caminhos prontos**, todos esperando você criar uma conta
no provider e apertar deploy.

### Caminho A — Fly.io (recomendado, volume persistente)

```bash
# 1. instalar CLI
curl -L https://fly.io/install.sh | sh

# 2. autenticar
flyctl auth signup           # ou: flyctl auth login

# 3. na raiz do repo:
cd sim-global
flyctl launch --copy-config --no-deploy
# → confirme app name único, região (gru = SP), sem Postgres,
#   sem Upstash, sem Sentry. NÃO deploy ainda.

# 4. volume pra SQLite persistente (1GB grátis no free tier)
flyctl volumes create simglobal_data --size 1 --region gru

# 5. token OAuth (gerado localmente uma vez via `claude setup-token`)
flyctl secrets set CLAUDE_CODE_OAUTH_TOKEN=<seu_token_longo>

# 6. deploy
flyctl deploy

# 7. URL: flyctl status → https://<app>.fly.dev
```

### Caminho B — Render.com (sem CLI, dashboard-only)

1. Conta grátis em https://render.com.
2. New → Blueprint → conecta repo `eduardopasouza/Claude`.
3. Render lê `render.yaml`. Confirma deploy.
4. Em Settings → Environment, cole `CLAUDE_CODE_OAUTH_TOKEN`.
5. URL aparece no dashboard.

Ressalva: free tier sem volume persistente. SQLite reseta a cada
redeploy/hibernate. Cada nova sessão volta para o cenário-piloto.
Para persistir, use Postgres free (expira em 90 dias) ou upgrade.

### Caminho C — Docker self-hosted (qualquer VPS)

```bash
git clone <repo> && cd sim-global
docker build -t simglobal .
docker run -d --name simglobal \
  -p 8000:8000 \
  -e CLAUDE_CODE_OAUTH_TOKEN=<token> \
  -v simglobal_data:/app/saves \
  simglobal
```

Aponte um reverse proxy (nginx/Caddy/Traefik) com TLS para o
container e pronto. Funciona em qualquer VPS — DigitalOcean Droplet
$4/mês, Hetzner CX11 €4/mês, Oracle Free Tier (gratuito), etc.

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
