# Multi-stage Dockerfile para sim-global.
# - builder instala dependências em /opt/venv
# - runtime: imagem slim, copia venv e código

FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY backend/pyproject.toml backend/README.md ./backend/
COPY backend/src ./backend/src
RUN pip install --upgrade pip \
    && pip install ./backend[agent]

FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    SIMGLOBAL_HOST=0.0.0.0 \
    SIMGLOBAL_PORT=8000 \
    SIMGLOBAL_OPEN_BROWSER=0 \
    SIMGLOBAL_PROJECT_ROOT=/app

# Node.js não é necessário; Tailwind/HTMX/Alpine vêm via CDN no template.

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY backend ./backend
COPY data ./data
COPY examples ./examples
COPY config.yaml ./config.yaml
COPY BRIEFING.md CLAUDE.md README.md ./

# saves/ vira volume montado em runtime — em Fly.io: /data/saves.
RUN mkdir -p saves

EXPOSE 8000

# Healthcheck via /api/health (não requer banco populado).
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3).status == 200 else 1)" || exit 1

CMD ["python", "-m", "simglobal"]
