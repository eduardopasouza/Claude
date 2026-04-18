"""
Cliente base CKAN para dados.gov.br.

Uso típico dos coletores:
    from app.collectors.dados_gov import DadosGovClient

    client = DadosGovClient()
    pkg = client.package_show("sigmine-processos-minerarios")
    # pkg["resources"] tem a lista de arquivos para download
    shp_resource = client.pick_resource(pkg, format_hint="SHP", name_hint="brasil")
    data_bytes = client.download_resource(shp_resource)

O CKAN oficial do dados.gov.br às vezes retorna 403 sem o header Authorization
ou falha silenciosamente — o cliente tenta fallback para download direto da
URL do resource quando a API retornar metadata mas a URL do recurso for
pública (maioria dos casos).
"""

from __future__ import annotations

import logging
from typing import Optional

import httpx

from app.config import settings

logger = logging.getLogger("agrojus.dados_gov")


class DadosGovClient:
    """Cliente HTTP para a API CKAN do dados.gov.br."""

    BASE = "https://dados.gov.br/api/publico/3/action"

    def __init__(self, token: Optional[str] = None, timeout: int = 60):
        self.token = token or settings.dados_gov_token
        self.timeout = timeout

    @property
    def headers(self) -> dict:
        h = {"User-Agent": "AgroJus/1.0 (+https://agrojus.com.br)"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    # ------------------------------------------------------------------ API
    def package_show(self, package_id: str) -> dict:
        """Retorna metadados + resources de um dataset."""
        url = f"{self.BASE}/package_show"
        with httpx.Client(timeout=self.timeout, follow_redirects=True) as c:
            r = c.get(url, params={"id": package_id}, headers=self.headers)
            r.raise_for_status()
        payload = r.json()
        if not payload.get("success"):
            raise RuntimeError(f"CKAN package_show falhou: {payload.get('error')}")
        return payload["result"]

    def package_search(self, query: str, groups: Optional[str] = None, rows: int = 50) -> list[dict]:
        """Busca datasets. `groups` restringe por tema (ex: 'meio-ambiente')."""
        url = f"{self.BASE}/package_search"
        fq = f"groups:{groups}" if groups else ""
        with httpx.Client(timeout=self.timeout, follow_redirects=True) as c:
            r = c.get(url, params={"q": query, "fq": fq, "rows": rows}, headers=self.headers)
            r.raise_for_status()
        payload = r.json()
        return payload.get("result", {}).get("results", [])

    # ------------------------------------------------------------------ Resources
    @staticmethod
    def pick_resource(
        pkg: dict,
        format_hint: Optional[str] = None,
        name_hint: Optional[str] = None,
    ) -> Optional[dict]:
        """Escolhe um resource do pacote por formato (SHP/CSV/ZIP) + nome."""
        resources = pkg.get("resources") or []
        scored: list[tuple[int, dict]] = []
        for r in resources:
            score = 0
            if format_hint:
                fmt = (r.get("format") or "").upper()
                if format_hint.upper() in fmt:
                    score += 10
            if name_hint:
                nm = (r.get("name") or "").lower() + " " + (r.get("url") or "").lower()
                for token in name_hint.lower().split():
                    if token in nm:
                        score += 3
            if r.get("url"):
                score += 1  # só considera se tem URL
            if score > 0:
                scored.append((score, r))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored else (resources[0] if resources else None)

    def download_resource(self, resource_or_url: dict | str, *, max_mb: int = 500) -> bytes:
        """Baixa o conteúdo do resource. Aceita dict do CKAN ou URL direta."""
        url = resource_or_url if isinstance(resource_or_url, str) else resource_or_url.get("url")
        if not url:
            raise ValueError("resource sem URL")
        size_limit = max_mb * 1024 * 1024
        chunks: list[bytes] = []
        total = 0
        with httpx.stream(
            "GET", url, timeout=self.timeout * 3, follow_redirects=True,
            headers={"User-Agent": "AgroJus/1.0"},
        ) as r:
            r.raise_for_status()
            for chunk in r.iter_bytes():
                chunks.append(chunk)
                total += len(chunk)
                if total > size_limit:
                    raise RuntimeError(f"Download excedeu {max_mb}MB — aborto")
        return b"".join(chunks)
