"""
Coletor de dados do IBGE — municipios, malhas, producao agricola.

Todas as APIs sao publicas, gratuitas e sem autenticacao.

Fontes:
- API Localidades: nomes, codigos IBGE, hierarquia UF/meso/micro
- API Malhas: contornos GeoJSON de estados e municipios
- API SIDRA: dados de producao agricola municipal (PAM)
"""

import logging
from typing import Optional

from app.collectors.base import BaseCollector

logger = logging.getLogger("agrojus")


class IBGECollector(BaseCollector):
    """Dados reais do IBGE — municipios, geometrias, producao agricola."""

    LOCALIDADES_URL = "https://servicodados.ibge.gov.br/api/v1/localidades"
    MALHAS_URL = "https://servicodados.ibge.gov.br/api/v3/malhas"
    SIDRA_URL = "https://apisidra.ibge.gov.br/values"

    # Codigos IBGE dos estados
    UF_CODES = {
        "AC": "12", "AL": "27", "AM": "13", "AP": "16", "BA": "29",
        "CE": "23", "DF": "53", "ES": "32", "GO": "52", "MA": "21",
        "MG": "31", "MS": "50", "MT": "51", "PA": "15", "PB": "25",
        "PE": "26", "PI": "22", "PR": "41", "RJ": "33", "RN": "24",
        "RO": "11", "RR": "14", "RS": "43", "SC": "42", "SE": "28",
        "SP": "35", "TO": "17",
    }

    def __init__(self):
        super().__init__("ibge")

    async def buscar_municipio_por_nome(self, nome: str) -> list[dict]:
        """Busca municipios por nome parcial. Retorna codigo IBGE, nome, UF."""
        cached = self._get_cached(f"mun_nome:{nome.lower()}")
        if cached:
            return cached

        try:
            response = await self._http_get(
                f"{self.LOCALIDADES_URL}/municipios",
                timeout=15.0,
            )
            todos = response.json()
            nome_lower = nome.lower()
            results = []
            for m in todos:
                if nome_lower in m.get("nome", "").lower():
                    uf = m.get("microrregiao", {}).get("mesorregiao", {}).get("UF", {})
                    results.append({
                        "codigo_ibge": str(m["id"]),
                        "nome": m["nome"],
                        "uf": uf.get("sigla", ""),
                        "estado": uf.get("nome", ""),
                    })

            self._set_cached(f"mun_nome:{nome.lower()}", results)
            return results
        except Exception as e:
            logger.warning("IBGE municipio search failed: %s", e)
            return []

    async def get_municipio_by_code(self, codigo: str) -> Optional[dict]:
        """Retorna dados de um municipio pelo codigo IBGE."""
        cached = self._get_cached(f"mun:{codigo}")
        if cached:
            return cached

        try:
            response = await self._http_get(
                f"{self.LOCALIDADES_URL}/municipios/{codigo}",
                timeout=10.0,
            )
            m = response.json()
            uf = m.get("microrregiao", {}).get("mesorregiao", {}).get("UF", {})
            result = {
                "codigo_ibge": str(m["id"]),
                "nome": m["nome"],
                "uf": uf.get("sigla", ""),
                "estado": uf.get("nome", ""),
                "microrregiao": m.get("microrregiao", {}).get("nome", ""),
                "mesorregiao": m.get("microrregiao", {}).get("mesorregiao", {}).get("nome", ""),
            }
            self._set_cached(f"mun:{codigo}", result)
            return result
        except Exception as e:
            logger.warning("IBGE municipio lookup failed: %s", e)
            return None

    async def get_malha_estado(self, uf: str, intrarregiao: str = "municipio") -> dict:
        """
        Retorna GeoJSON com malha de municipios de um estado.

        Retorna FeatureCollection com geometria de cada municipio.
        """
        uf_code = self.UF_CODES.get(uf.upper())
        if not uf_code:
            return {"type": "FeatureCollection", "features": []}

        cached = self._get_cached(f"malha:{uf}:{intrarregiao}")
        if cached:
            return cached

        try:
            response = await self._http_get(
                f"{self.MALHAS_URL}/estados/{uf_code}",
                params={
                    "formato": "application/vnd.geo+json",
                    "qualidade": "intermediaria",
                    "intrarregiao": intrarregiao,
                },
                timeout=30.0,
            )
            data = response.json()
            self._set_cached(f"malha:{uf}:{intrarregiao}", data)
            return data
        except Exception as e:
            logger.warning("IBGE malha failed: %s", e)
            return {"type": "FeatureCollection", "features": []}

    async def get_malha_municipio(self, codigo: str) -> dict:
        """Retorna GeoJSON com contorno de um municipio."""
        cached = self._get_cached(f"malha_mun:{codigo}")
        if cached:
            return cached

        try:
            response = await self._http_get(
                f"{self.MALHAS_URL}/municipios/{codigo}",
                params={
                    "formato": "application/vnd.geo+json",
                    "qualidade": "intermediaria",
                },
                timeout=15.0,
            )
            data = response.json()
            self._set_cached(f"malha_mun:{codigo}", data)
            return data
        except Exception as e:
            logger.warning("IBGE malha municipio failed: %s", e)
            return {"type": "FeatureCollection", "features": []}

    async def get_producao_agricola(self, codigo_municipio: str) -> dict:
        """
        Retorna dados de producao agricola do municipio (PAM/SIDRA).

        Tabela 5457: Area colhida, area plantada, quantidade produzida
        Culturas: soja (39), milho (33), cafe (9), cana (31), algodao (3)
        """
        cached = self._get_cached(f"producao:{codigo_municipio}")
        if cached:
            return cached

        try:
            url = (
                f"{self.SIDRA_URL}/t/5457/n6/{codigo_municipio}"
                f"/v/214,215,216/p/last%201/c782/39,33,9,31,3/f/n"
            )
            response = await self._http_get(url, timeout=15.0)
            raw = response.json()

            result = {"municipio_code": codigo_municipio, "culturas": []}

            if len(raw) > 1:
                for row in raw[1:]:
                    result["culturas"].append({
                        "cultura": row.get("D4N", ""),
                        "variavel": row.get("D2N", ""),
                        "valor": row.get("V", "0"),
                        "unidade": row.get("MN", ""),
                        "ano": row.get("D3N", ""),
                    })

            self._set_cached(f"producao:{codigo_municipio}", result)
            return result
        except Exception as e:
            logger.warning("IBGE SIDRA failed: %s", e)
            return {"municipio_code": codigo_municipio, "culturas": []}
