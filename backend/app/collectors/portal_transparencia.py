"""
Cliente Portal da Transparência (CGU).

Endpoints usados:
  - CEIS:    /api-de-dados/ceis?pagina=N
  - CNEP:    /api-de-dados/cnep?pagina=N
  - CEPIM:   /api-de-dados/cepim?pagina=N (entidades sem repasse)

Autenticação via header `chave-api-dados` (token em `.env` como
PORTAL_TRANSPARENCIA_TOKEN).

O portal pagina em blocos de 500 registros e aplica rate limit — o cliente
adiciona backoff simples entre páginas.
"""

from __future__ import annotations

import logging
import time
from typing import Generator

import httpx

from app.config import settings

logger = logging.getLogger("agrojus.portal_transparencia")


class PortalTransparenciaClient:
    BASE = "https://api.portaldatransparencia.gov.br/api-de-dados"

    def __init__(self, token: str | None = None, timeout: int = 30):
        self.token = token or settings.portal_transparencia_token
        self.timeout = timeout
        if not self.token:
            raise RuntimeError("PORTAL_TRANSPARENCIA_TOKEN não configurado em .env")

    @property
    def headers(self) -> dict:
        return {
            "User-Agent": "AgroJus/1.0",
            "chave-api-dados": self.token,
        }

    def iter_pages(self, endpoint: str, max_pages: int = 100) -> Generator[list[dict], None, None]:
        """Itera todas as páginas de um endpoint. Para ao receber página vazia."""
        url = f"{self.BASE}{endpoint}"
        with httpx.Client(timeout=self.timeout) as c:
            for page in range(1, max_pages + 1):
                r = c.get(url, params={"pagina": page}, headers=self.headers)
                if r.status_code == 429:
                    logger.warning("rate limit atingido, aguardando 60s")
                    time.sleep(60)
                    r = c.get(url, params={"pagina": page}, headers=self.headers)
                r.raise_for_status()
                rows = r.json()
                if not rows:
                    return
                yield rows
                time.sleep(0.6)  # respeitar rate limit conservador

    def fetch_ceis(self, max_pages: int = 100) -> list[dict]:
        """Busca todos os registros CEIS."""
        all_rows: list[dict] = []
        for page_rows in self.iter_pages("/ceis", max_pages=max_pages):
            all_rows.extend(page_rows)
            logger.info("CEIS: %d registros acumulados", len(all_rows))
        return all_rows

    def fetch_cnep(self, max_pages: int = 100) -> list[dict]:
        """Busca todos os registros CNEP."""
        all_rows: list[dict] = []
        for page_rows in self.iter_pages("/cnep", max_pages=max_pages):
            all_rows.extend(page_rows)
            logger.info("CNEP: %d registros acumulados", len(all_rows))
        return all_rows
