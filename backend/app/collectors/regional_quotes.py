"""
Coletor de cotações REGIONAIS (preços por praça/UF).

Scraping de Notícias Agrícolas — tabelas HTML estáticas com preços
de mercado físico por praça (ex: Sorriso/MT, Rondonópolis/MT,
Não-Me-Toque/RS, Castro/PR).

Cada commodity tem 20-100+ praças cobrindo principais UFs produtoras.

Cache TTL 1h (preços atualizam 1-2× ao dia).

Commodities suportadas:
  soja, milho, cafe, boi (boi gordo), trigo, algodao, arroz, acucar
"""

from __future__ import annotations

import logging
import re
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from app.collectors.base import BaseCollector

logger = logging.getLogger("agrojus")


REGIONAL_SOURCE = "https://www.noticiasagricolas.com.br/cotacoes"

# Commodity slug → URL path + unidade
COMMODITY_MAP: dict[str, dict] = {
    "soja": {"path": "soja", "unit": "R$/sc 60kg", "label": "Soja em grão"},
    "milho": {"path": "milho", "unit": "R$/sc 60kg", "label": "Milho em grão"},
    "cafe": {"path": "cafe", "unit": "R$/sc 60kg", "label": "Café arábica"},
    "boi": {"path": "boi", "unit": "R$/@", "label": "Boi gordo"},
    "trigo": {"path": "trigo", "unit": "R$/sc 60kg", "label": "Trigo"},
    "algodao": {"path": "algodao", "unit": "R$/@", "label": "Algodão"},
    "arroz": {"path": "arroz", "unit": "R$/sc 50kg", "label": "Arroz"},
    "acucar": {"path": "acucar", "unit": "R$/sc 50kg", "label": "Açúcar"},
    "feijao": {"path": "feijao", "unit": "R$/sc 60kg", "label": "Feijão"},
    "leite": {"path": "leite", "unit": "R$/litro", "label": "Leite ao produtor"},
}

# Formato 1: "Cidade/UF (fonte opcional)" — ex "Sorriso/MT (Sindicato)"
PRACA_PATTERN = re.compile(
    r"^([A-ZÁÉÍÓÚÃÕÇÂÊÔ][A-Za-zÀ-ú\s\-\.']+?)\s*/\s*([A-Z]{2})\b"
)
# Formato 2: "UF Cidade" — ex "SP Barretos", "MG Triângulo Mineiro"
PRACA_PATTERN_UF_PREFIX = re.compile(
    r"^([A-Z]{2})\s+([A-ZÁÉÍÓÚÃÕÇÂÊÔ][A-Za-zÀ-ú\s\-\.']{2,60})$"
)

VALID_UFS = {
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA",
    "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN",
    "RO", "RR", "RS", "SC", "SE", "SP", "TO",
}


def _parse_number_brl(text: str) -> Optional[float]:
    """Converte '1.234,56' ou '+0,85' ou '-1,50' em float."""
    cleaned = text.strip().replace("R$", "").replace(" ", "").replace("%", "")
    cleaned = cleaned.replace(".", "").replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


class RegionalQuotesCollector(BaseCollector):
    """Cotações físicas por praça (Notícias Agrícolas)."""

    def __init__(self) -> None:
        super().__init__("regional_quotes")

    async def fetch_commodity(self, commodity: str) -> dict:
        """Retorna estrutura: {commodity, unit, quotes: [{praca, uf, fonte, preco, var_pct}]}"""
        if commodity not in COMMODITY_MAP:
            return {"error": f"Commodity '{commodity}' não suportada",
                    "supported": list(COMMODITY_MAP.keys())}

        meta = COMMODITY_MAP[commodity]

        cache_key = f"regional:{commodity}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        url = f"{REGIONAL_SOURCE}/{meta['path']}"

        try:
            async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as c:
                r = await c.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 AgroJus",
                        "Accept": "text/html",
                    },
                )
                r.raise_for_status()
                html = r.text
        except Exception as e:
            logger.warning("regional_quotes %s erro: %s", commodity, e)
            return {"error": str(e), "commodity": commodity}

        quotes = self._parse_html(html)

        # Sanity filter: remove outliers (> 3x mediana)
        if len(quotes) >= 5:
            prices = sorted([q["preco"] for q in quotes])
            median = prices[len(prices) // 2]
            threshold = median * 3
            quotes = [q for q in quotes if q["preco"] <= threshold]

        # Estatísticas agregadas
        by_uf: dict[str, list[float]] = {}
        for q in quotes:
            by_uf.setdefault(q["uf"], []).append(q["preco"])
        uf_stats = [
            {
                "uf": uf,
                "total_pracas": len(ps),
                "preco_min": min(ps),
                "preco_max": max(ps),
                "preco_medio": round(sum(ps) / len(ps), 2),
            }
            for uf, ps in sorted(by_uf.items(), key=lambda x: -sum(x[1]) / len(x[1]))
        ]

        result = {
            "commodity": commodity,
            "label": meta["label"],
            "unit": meta["unit"],
            "source": "Notícias Agrícolas (mercado físico)",
            "source_url": url,
            "total_pracas": len(quotes),
            "quotes": quotes,
            "uf_stats": uf_stats,
        }

        # Cache TTL mais curto que default (mercado muda no dia)
        if quotes:
            self._set_cached(cache_key, result)

        return result

    def _parse_html(self, html: str) -> list[dict]:
        """Extrai pracas das tabelas HTML."""
        soup = BeautifulSoup(html, "html.parser")
        quotes: list[dict] = []
        seen: set[str] = set()

        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) < 2:
                    continue
                first = cells[0].get_text(strip=True)

                # Tenta "Cidade/UF" primeiro
                match = PRACA_PATTERN.match(first)
                cidade = ""
                uf = ""
                fonte = ""
                if match:
                    cidade = match.group(1).strip()
                    uf = match.group(2)
                    paren = re.search(r"\(([^)]+)\)", first)
                    if paren:
                        fonte = paren.group(1).strip()
                else:
                    # Formato "UF Cidade"
                    match2 = PRACA_PATTERN_UF_PREFIX.match(first)
                    if match2 and match2.group(1) in VALID_UFS:
                        uf = match2.group(1)
                        cidade = match2.group(2).strip()
                    else:
                        continue

                preco_txt = cells[1].get_text(strip=True)
                var_txt = cells[2].get_text(strip=True) if len(cells) >= 3 else ""
                data_txt = cells[3].get_text(strip=True) if len(cells) >= 4 else ""

                preco = _parse_number_brl(preco_txt)
                var = _parse_number_brl(var_txt)

                if preco is None or preco <= 0 or preco > 100_000:
                    continue

                # Sanity check: variação fora do intervalo [-50,+50] %
                # provavelmente não é variação (pode ser preço de outra coluna)
                if var is not None and (var > 50 or var < -50):
                    var = None

                # dedupe por (cidade, uf, fonte)
                key = f"{cidade}|{uf}|{fonte}"
                if key in seen:
                    continue
                seen.add(key)

                quotes.append({
                    "praca": cidade,
                    "uf": uf,
                    "fonte": fonte,
                    "preco": preco,
                    "variacao_pct": var,
                    "data": data_txt or None,
                })

        return quotes

    async def fetch_all(self) -> dict:
        """Baixa todas commodities em paralelo."""
        import asyncio
        tasks = {
            c: self.fetch_commodity(c)
            for c in ["soja", "milho", "cafe", "boi", "trigo"]
        }
        results = await asyncio.gather(*tasks.values())
        return dict(zip(tasks.keys(), results))
