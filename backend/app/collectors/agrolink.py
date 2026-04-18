"""
Coletor Agrolink — cotações regionalizadas via páginas de histórico por UF.

Descoberta: as páginas `/cotacoes/historico/{uf}/{commodity-unit}` têm
preços em TEXTO PURO (tabela HTML sem imagens), contendo histórico
mensal completo por UF (estadual vs nacional).

Exemplo: /cotacoes/historico/mt/soja-em-grao-sc-60kg
  → 266 rows desde 2003: [Mês/Ano | Estadual | Nacional]

Para cada commodity, existem ~10 UFs disponíveis (principais produtoras).

Cobertura:
  soja (10 UFs): GO, TO, PR, MS, RS, SP, MT, PA, BA, MA
  milho, café, etc. — mesma estrutura

Cache 6h (dados mensais — não muda no dia).
"""

from __future__ import annotations

import asyncio
import logging
import re
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from app.collectors.base import BaseCollector

logger = logging.getLogger("agrojus")

AGROLINK_BASE = "https://www.agrolink.com.br"

# Todas UFs — coletor tenta cada uma, mantém as que responderam
ALL_UFS = [
    "ac", "al", "am", "ap", "ba", "ce", "df", "es", "go", "ma",
    "mg", "ms", "mt", "pa", "pb", "pe", "pi", "pr", "rj", "rn",
    "ro", "rr", "rs", "sc", "se", "sp", "to",
]

# Commodity → (path_principal, slug-do-historico)
AGROLINK_PATHS: dict[str, dict] = {
    "soja": {
        "main": "/cotacoes/graos/soja",
        "slug": "soja-em-grao-sc-60kg",
        "unit": "R$/sc 60kg",
        "label": "Soja em grão",
    },
    "milho": {
        "main": "/cotacoes/graos/milho",
        "slug": "milho-seco-sc-60kg",
        "unit": "R$/sc 60kg",
        "label": "Milho seco",
    },
    "cafe": {
        "main": "/cotacoes/graos/cafe",
        "slug": "cafe-arabica-tipo-6-bebida-dura-sc-60kg",
        "unit": "R$/sc 60kg",
        "label": "Café arábica T6",
    },
    "trigo": {
        "main": "/cotacoes/graos/trigo",
        "slug": "trigo-em-grao-nacional-sc-60kg",
        "unit": "R$/sc 60kg",
        "label": "Trigo em grão",
    },
    "arroz": {
        "main": "/cotacoes/graos/arroz",
        "slug": "arroz-em-casca-sc-60kg",
        "unit": "R$/sc 60kg",
        "label": "Arroz em casca",
    },
    "feijao": {
        "main": "/cotacoes/graos/feijao",
        "slug": "feijao-carioca-sc-60kg",
        "unit": "R$/sc 60kg",
        "label": "Feijão carioca",
    },
    "boi": {
        "main": "/cotacoes/carnes/bovinos",
        "slug": "boi-gordo-15kg",
        "unit": "R$/@ (15kg)",
        "label": "Boi gordo",
    },
    "algodao": {
        "main": "/cotacoes/fibras/algodao",
        "slug": "algodao-em-pluma-15kg",
        "unit": "R$/@ pluma",
        "label": "Algodão em pluma",
    },
    "cana": {
        "main": "/cotacoes/diversos/cana-de-acucar",
        "slug": "cana-de-acucar-1ton",
        "unit": "R$/ton",
        "label": "Cana-de-açúcar",
    },
    "leite": {
        "main": "/cotacoes/diversos/leite",
        "slug": "leite-1l",
        "unit": "R$/litro",
        "label": "Leite ao produtor",
    },
    "frango": {
        "main": "/cotacoes/carnes/aves",
        "slug": "frango-1kg",
        "unit": "R$/kg",
        "label": "Frango vivo",
    },
    "sorgo": {
        "main": "/cotacoes/graos/sorgo",
        "slug": "sorgo-sc-60kg",
        "unit": "R$/sc 60kg",
        "label": "Sorgo em grão",
    },
    "acucar": {
        "main": "/cotacoes/acucar-e-alcool/acucar",
        "slug": "acucar-vhp-sc-50kg",
        "unit": "R$/sc 50kg",
        "label": "Açúcar VHP",
    },
}


def _parse_brl(s: str) -> Optional[float]:
    """Converte '1.234,56' em float."""
    if not s:
        return None
    cleaned = s.strip().replace(".", "").replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


class AgrolinkCollector(BaseCollector):
    """Cotações Agrolink via histórico por UF (texto puro, sem OCR)."""

    def __init__(self) -> None:
        super().__init__("agrolink")

    async def fetch_commodity(self, commodity: str) -> dict:
        """Busca cotações atuais + histórico por UF.

        Retorna:
          {
            commodity, label, unit,
            total_ufs: 10,
            ufs: [
              { uf, preco_atual_estadual, preco_atual_nacional,
                variacao_pct, mes_ref,
                historico: [{ mes, estadual, nacional }]
              }
            ],
            uf_stats: [...]  # resumo para cards/map
          }
        """
        if commodity not in AGROLINK_PATHS:
            return {"error": f"Commodity '{commodity}' não suportada",
                    "supported": list(AGROLINK_PATHS.keys())}

        meta = AGROLINK_PATHS[commodity]
        cache_key = f"agrolink_uf:{commodity}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        # 1) Tenta as 27 UFs em paralelo; mantém só as que responderem 200 com dados
        tasks = {uf: self._fetch_uf_history(uf, meta["slug"]) for uf in ALL_UFS}
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)

        ufs_data = []
        for uf, res in zip(tasks.keys(), results):
            if isinstance(res, Exception):
                logger.warning("agrolink %s/%s: %s", commodity, uf, res)
                continue
            if res:
                ufs_data.append(res)

        # 3) Agregar: estatísticas de preço atual por UF
        uf_stats = []
        for d in ufs_data:
            ultimo = d.get("historico", [None])[0] if d.get("historico") else None
            if ultimo and ultimo.get("estadual") is not None:
                uf_stats.append({
                    "uf": d["uf"].upper(),
                    "preco_atual": ultimo["estadual"],
                    "preco_nacional": ultimo.get("nacional"),
                    "mes_ref": ultimo["mes"],
                    "total_meses_historico": len(d["historico"]),
                })

        uf_stats.sort(key=lambda x: -(x["preco_atual"] or 0))

        result = {
            "commodity": commodity,
            "label": meta["label"],
            "unit": meta["unit"],
            "source": "Agrolink — histórico mensal por UF",
            "source_url_example": f"{AGROLINK_BASE}/cotacoes/historico/mt/{meta['slug']}",
            "total_ufs": len(ufs_data),
            "ufs": ufs_data,
            "uf_stats": uf_stats,
        }

        # Cache 6h — dados mensais, mudam lento
        if ufs_data:
            self._set_cached(cache_key, result)

        return result

    async def _discover_ufs(self, main_url: str, slug: str) -> list[str]:
        """Descobre lista de UFs disponíveis via página principal."""
        try:
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as c:
                r = await c.get(main_url, headers={"User-Agent": "Mozilla/5.0 AgroJus"})
                r.raise_for_status()
        except Exception as e:
            logger.warning("agrolink discover_ufs erro: %s", e)
            return []

        pattern = re.compile(
            rf"/cotacoes/historico/([a-z]{{2}})/{re.escape(slug)}"
        )
        found = set(pattern.findall(r.text))
        return sorted(found)

    async def _fetch_uf_history(self, uf: str, slug: str) -> Optional[dict]:
        """Busca tabela de histórico mensal de uma UF."""
        url = f"{AGROLINK_BASE}/cotacoes/historico/{uf}/{slug}"
        try:
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as c:
                r = await c.get(url, headers={"User-Agent": "Mozilla/5.0 AgroJus"})
                r.raise_for_status()
                html = r.text
        except Exception as e:
            logger.warning("agrolink history %s/%s: %s", uf, slug, e)
            return None

        soup = BeautifulSoup(html, "html.parser")
        historico = []
        for t in soup.find_all("table"):
            rows = t.find_all("tr")
            if len(rows) < 3:
                continue
            # Cabeçalho deve ter "Mês/Ano" ou "Mês"
            header_cells = [c.get_text(strip=True).lower() for c in rows[0].find_all(["th", "td"])]
            if not any("mês" in h or "mes" in h for h in header_cells):
                continue
            # Parse body — mês está em <th>, valores em <td>
            for row in rows[1:]:
                cells = [c.get_text(strip=True) for c in row.find_all(["th", "td"])]
                if len(cells) < 2:
                    continue
                mes = cells[0]
                if not re.match(r"^\d{1,2}/\d{4}$", mes):
                    continue
                estadual = _parse_brl(cells[1]) if len(cells) >= 2 else None
                nacional = _parse_brl(cells[2]) if len(cells) >= 3 else None
                historico.append({
                    "mes": mes,
                    "estadual": estadual,
                    "nacional": nacional,
                })

        if not historico:
            return None

        return {
            "uf": uf.upper(),
            "source_url": url,
            "historico": historico,
        }
