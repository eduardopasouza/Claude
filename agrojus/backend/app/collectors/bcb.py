"""
Coletor de dados economicos e financeiros do Banco Central do Brasil.

API publica, gratuita, sem autenticacao.
Fonte: https://dadosabertos.bcb.gov.br/

Dados disponiveis:
- Taxa SELIC (serie 11)
- Dolar comercial (serie 1)
- IPCA (serie 433)
- IGP-M (serie 189)
- CDI (serie 12)
- Preco da terra (INCRA - serie 21340, se disponivel)
"""

import logging
from typing import Optional

from app.collectors.base import BaseCollector

logger = logging.getLogger("agrojus")


class BCBCollector(BaseCollector):
    """Dados financeiros reais do Banco Central do Brasil."""

    API_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"

    # Series disponiveis
    SERIES = {
        "selic": {"code": "11", "name": "Taxa SELIC", "unit": "% a.d."},
        "dolar": {"code": "1", "name": "Dolar Comercial (venda)", "unit": "R$"},
        "ipca": {"code": "433", "name": "IPCA", "unit": "% a.m."},
        "igpm": {"code": "189", "name": "IGP-M", "unit": "% a.m."},
        "cdi": {"code": "12", "name": "Taxa CDI", "unit": "% a.d."},
        "poupanca": {"code": "25", "name": "Rendimento Poupanca", "unit": "% a.m."},
        "tr": {"code": "226", "name": "Taxa Referencial (TR)", "unit": "% a.m."},
    }

    def __init__(self):
        super().__init__("bcb")

    async def get_serie(self, serie_key: str, ultimos: int = 10) -> dict:
        """Busca dados de uma serie temporal do BCB."""
        serie_info = self.SERIES.get(serie_key)
        if not serie_info:
            return {"error": f"Serie '{serie_key}' nao encontrada", "available": list(self.SERIES.keys())}

        cached = self._get_cached(f"serie:{serie_key}:{ultimos}")
        if cached:
            return cached

        try:
            url = f"{self.API_URL}.{serie_info['code']}/dados/ultimos/{ultimos}"
            response = await self._http_get(url, params={"formato": "json"}, timeout=10.0)
            data = response.json()

            result = {
                "serie": serie_info["name"],
                "code": serie_info["code"],
                "unit": serie_info["unit"],
                "records": data,
                "latest": data[-1] if data else None,
                "source": "Banco Central do Brasil",
            }

            self._set_cached(f"serie:{serie_key}:{ultimos}", result)
            return result
        except Exception as e:
            logger.warning("BCB API failed for %s: %s", serie_key, e)
            return {"error": str(e), "serie": serie_info["name"]}

    async def get_indicators_summary(self) -> dict:
        """Retorna resumo de todos os indicadores economicos atuais."""
        cached = self._get_cached("indicators_summary")
        if cached:
            return cached

        results = {}
        for key in ["selic", "dolar", "ipca", "igpm", "cdi"]:
            data = await self.get_serie(key, ultimos=1)
            if data.get("latest"):
                results[key] = {
                    "name": data["serie"],
                    "value": data["latest"]["valor"],
                    "date": data["latest"]["data"],
                    "unit": data["unit"],
                }

        self._set_cached("indicators_summary", results)
        return results
