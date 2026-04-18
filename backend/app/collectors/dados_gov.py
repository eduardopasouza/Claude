"""
Cliente base CKAN para dados.gov.br com fallback a URLs diretas.

Uso típico dos coletores:
    from app.collectors.dados_gov import DadosGovClient

    client = DadosGovClient()
    pkg = client.package_show("sigmine-processos-minerarios")
    # pkg["resources"] tem a lista de arquivos para download
    shp_resource = client.pick_resource(pkg, format_hint="SHP", name_hint="brasil")
    data_bytes = client.download_resource(shp_resource)

**Fallback automático**: quando `DADOS_GOV_TOKEN` não está presente, está
expirado (401) ou o portal está fora do ar (5xx/timeout), o cliente cai
automaticamente para a tabela `KNOWN_RESOURCES` abaixo, que mapeia cada
dataset_id para URLs públicas diretas conhecidas do arquivo (CSV/ZIP/SHP).

Essas URLs são as mesmas que o CKAN devolveria em `package.resources[].url`.
Se mudarem, basta atualizar a tabela. O resto do fluxo (`pick_resource`,
`download_resource`) funciona sem alterações.
"""

from __future__ import annotations

import logging
from typing import Optional

import httpx

from app.config import settings

logger = logging.getLogger("agrojus.dados_gov")


# ==========================================================================
# Fallback: URLs públicas diretas dos recursos quando CKAN estiver offline
# ou o token estiver expirado. Validadas manualmente contra os portais de
# origem — atualizar quando publisher mover o arquivo.
# ==========================================================================

KNOWN_RESOURCES: dict[str, list[dict]] = {
    # SIGMINE/ANM — processos minerários do Brasil (ponto de origem da ANM,
    # não passa pelo CKAN dados.gov.br; estável há anos)
    "sigmine-processos-minerarios": [
        {
            "name": "SIGMINE Brasil - processos minerários SHP zipado",
            "format": "SHP",
            "url": "https://app.anm.gov.br/dadosabertos/SIGMINE/PROCESSOS_MINERARIOS/BRASIL.zip",
        },
    ],
    # INCRA — Certificação / Acervo Fundiário
    "assentamentos-brasil": [
        {
            "name": "INCRA Assentamentos Brasil SHP",
            "format": "SHP",
            "url": "https://certificacao.incra.gov.br/csv_shp/zip/Assentamento%20Brasil.zip",
        },
    ],
    "areas-quilombolas": [
        {
            "name": "INCRA Áreas Quilombolas SHP",
            "format": "SHP",
            "url": "https://certificacao.incra.gov.br/csv_shp/zip/%C3%81reas%20de%20Quilombolas.zip",
        },
    ],
    # ANA — Outorgas (CSV público) e Base Hidrográfica Ottocodificada
    "outorgas-de-direito-de-uso-de-recursos-hidricos": [
        {
            "name": "ANA Cadastro Nacional de Usuários de Recursos Hídricos (CNARH40) - outorgas",
            "format": "CSV",
            "url": "https://metadados.snirh.gov.br/files/d2deb9e1-5961-490c-9df1-11d2a2d56d5b/outorga_federal_convertida.csv",
        },
    ],
    "base-hidrografica-ottocodificada": [
        {
            "name": "ANA BHO Multiescalas SHP zipado",
            "format": "SHP",
            "url": "https://metadados.snirh.gov.br/files/6f2bcbd2-4a77-4103-a5f1-5a8a6cb4d180/geoft_bho_2017_5k.zip",
        },
    ],
    # ANEEL SIGA — Sistema de Informações de Geração (CKAN próprio ANEEL, validado 2026-04-18)
    "siga-sistema-de-informacoes-de-geracao-da-aneel": [
        {
            "name": "ANEEL SIGA - empreendimentos de geração (CSV)",
            "format": "CSV",
            "url": "https://dadosabertos.aneel.gov.br/dataset/6d90b77c-c5f5-4d81-bdec-7bc619494bb9/resource/11ec447d-698d-4ab8-977f-b424d5deee6a/download/siga-empreendimentos-geracao.csv",
        },
    ],
    # Alias do nome antigo usado no loader: redireciona pro mesmo recurso
    "empreendimentos-de-geracao-de-energia-eletrica-siga-aneel": [
        {
            "name": "ANEEL SIGA - empreendimentos de geração (CSV, alias)",
            "format": "CSV",
            "url": "https://dadosabertos.aneel.gov.br/dataset/6d90b77c-c5f5-4d81-bdec-7bc619494bb9/resource/11ec447d-698d-4ab8-977f-b424d5deee6a/download/siga-empreendimentos-geracao.csv",
        },
    ],
    # ANEEL SIGEL (linhas de transmissão georreferenciadas) — não publicado em CKAN, só no portal SIGEL;
    # deixamos stub para que o loader retorne erro explícito.
    "sistema-de-informacoes-georreferenciadas-do-setor-eletrico-sigel": [],
    # ANA Outorgas (SNIRH) — não há CSV público estável conhecido no CKAN oficial ainda;
    # extração requer varrer GeoNetwork. Stub.
    "outorgas-de-direito-de-uso-de-recursos-hidricos": [],
    # ANA BHO — mesma situação
    "base-hidrografica-ottocodificada": [],
    # Garantia-Safra — Portal Transparência protege arquivo zip por sessão web (403 via curl direto).
    # Coletar via API paginada seria viável como CEIS/CNEP; stub por ora.
    "beneficiarios-do-programa-garantia-safra": [],
    # IBAMA embargos/CTF — IBAMA tem CKAN próprio (dadosabertos.ibama.gov.br).
    # URL do SHP georreferenciado valida em abr/2026:
    "ibama-termo-de-embargo": [
        {
            "name": "IBAMA termo de embargo — SHP com geometria",
            "format": "SHP",
            "url": "https://pamgia.ibama.gov.br/geoservicos/arquivos/adm_embargo_ibama_a.shp.zip",
        },
        {
            "name": "IBAMA termo de embargo — CSV (sem geometria)",
            "format": "CSV",
            "url": "https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/termo_embargo/termo_embargo_csv.zip",
        },
    ],
    "fiscalizacao-auto-de-infracao": [
        {
            "name": "IBAMA autos de infração (SIFISC CSV zipado)",
            "format": "CSV",
            "url": "https://dadosabertos.ibama.gov.br/dados/SIFISC/auto_infracao/auto_infracao/auto_infracao_csv.zip",
        },
    ],
    "ibama-cadastro-tecnico-federal-de-atividades-potencialmente-poluidoras-e-ou-utilizadoras-de-recursos-ambientais": [],
}


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
    def _fallback_pkg(self, package_id: str, reason: str) -> dict:
        """Retorna dict sintético compatível com package_show usando KNOWN_RESOURCES."""
        resources = KNOWN_RESOURCES.get(package_id, [])
        if not resources:
            raise RuntimeError(
                f"CKAN package_show falhou ({reason}) e não há URLs diretas conhecidas "
                f"para '{package_id}'. Atualize KNOWN_RESOURCES em dados_gov.py ou "
                f"renove o DADOS_GOV_TOKEN."
            )
        logger.warning(
            "CKAN indisponível para %s (%s) — usando fallback com %d recurso(s) direto(s)",
            package_id, reason, len(resources),
        )
        return {
            "id": package_id,
            "name": package_id,
            "resources": resources,
            "_fallback": True,
            "_fallback_reason": reason,
        }

    def package_show(self, package_id: str) -> dict:
        """Retorna metadados + resources. Fallback para URLs diretas se CKAN falhar."""
        url = f"{self.BASE}/package_show"
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as c:
                r = c.get(url, params={"id": package_id}, headers=self.headers)
            if r.status_code == 401:
                return self._fallback_pkg(package_id, "token expirado/ausente (401)")
            if r.status_code >= 500:
                return self._fallback_pkg(package_id, f"CKAN {r.status_code}")
            r.raise_for_status()
            payload = r.json()
            if not payload.get("success"):
                return self._fallback_pkg(package_id, f"success=false ({payload.get('error')})")
            return payload["result"]
        except httpx.TimeoutException:
            return self._fallback_pkg(package_id, "timeout")
        except httpx.RequestError as e:
            return self._fallback_pkg(package_id, f"erro de conexão: {e}")

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
