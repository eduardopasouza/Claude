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

    async def get_serie_historica_producao(
        self, codigo_municipio: str, cultura_code: str = "39", anos: int = 10
    ) -> dict:
        """
        Serie historica de producao agricola (PAM/SIDRA).

        Retorna area colhida, area plantada, quantidade produzida,
        valor da producao e rendimento medio (kg/ha) por ano.

        Codigos de cultura: 39=soja, 33=milho, 9=cafe, 31=cana,
        3=algodao, 40=arroz, 45=trigo, 15=feijao, 2713=sorgo.
        """
        cache_key = f"serie_hist:{codigo_municipio}:{cultura_code}:{anos}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        try:
            # v/214=area colhida, v/215=area plantada, v/216=qtd produzida,
            # v/112=rendimento medio, v/215=valor producao
            url = (
                f"{self.SIDRA_URL}/t/5457/n6/{codigo_municipio}"
                f"/v/214,215,216,112/p/last%20{anos}/c782/{cultura_code}/f/n"
            )
            response = await self._http_get(url, timeout=15.0)
            raw = response.json()

            # Organizar por ano
            anos_data = {}
            if len(raw) > 1:
                for row in raw[1:]:
                    ano = row.get("D3N", "")
                    variavel = row.get("D2N", "")
                    valor = row.get("V", "0")
                    unidade = row.get("MN", "")

                    if ano not in anos_data:
                        anos_data[ano] = {"ano": ano}
                    anos_data[ano][variavel] = {"valor": valor, "unidade": unidade}

            result = {
                "municipio_code": codigo_municipio,
                "cultura_code": cultura_code,
                "anos": anos,
                "serie": list(anos_data.values()),
                "total_anos": len(anos_data),
                "source": "IBGE/SIDRA (PAM - Tabela 5457)",
            }

            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.warning("IBGE serie historica failed: %s", e)
            return {"municipio_code": codigo_municipio, "serie": [], "error": str(e)}

    async def get_pecuaria_municipal(
        self, codigo_municipio: str, anos: int = 5
    ) -> dict:
        """
        Dados de pecuaria municipal (PPM/SIDRA).

        Tabela 3939: efetivo de rebanho.
        Codigos: 2670=bovinos, 2672=bubalinos, 2675=equinos,
        2681=suinos, 2683=caprinos, 2684=ovinos, 2682=galinaceos.
        """
        cache_key = f"pecuaria:{codigo_municipio}:{anos}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        try:
            url = (
                f"{self.SIDRA_URL}/t/3939/n6/{codigo_municipio}"
                f"/v/105/p/last%20{anos}/c79/2670,2672,2675,2681,2683,2684/f/n"
            )
            response = await self._http_get(url, timeout=15.0)
            raw = response.json()

            rebanhos = {}
            if len(raw) > 1:
                for row in raw[1:]:
                    tipo = row.get("D4N", "")
                    ano = row.get("D3N", "")
                    valor = row.get("V", "0")

                    if tipo not in rebanhos:
                        rebanhos[tipo] = []
                    rebanhos[tipo].append({"ano": ano, "quantidade": valor, "unidade": "Cabecas"})

            result = {
                "municipio_code": codigo_municipio,
                "rebanhos": rebanhos,
                "anos": anos,
                "source": "IBGE/SIDRA (PPM - Tabela 3939)",
            }

            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.warning("IBGE pecuaria failed: %s", e)
            return {"municipio_code": codigo_municipio, "rebanhos": {}, "error": str(e)}

    async def get_censo_agropecuario(self, codigo_municipio: str) -> dict:
        """
        Dados do Censo Agropecuario 2017 (SIDRA).

        Retorna: numero de estabelecimentos, area, despesas,
        uso do solo, mao de obra.
        """
        cache_key = f"censo_agro:{codigo_municipio}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        result = {
            "municipio_code": codigo_municipio,
            "ano": 2017,
            "dados": {},
            "source": "IBGE/SIDRA (Censo Agropecuario 2017)",
        }

        try:
            # Tabela 6855 - Estabelecimentos e preparo do solo
            url1 = f"{self.SIDRA_URL}/t/6855/n6/{codigo_municipio}/v/all/p/2017/f/n"
            r1 = await self._http_get(url1, timeout=15.0)
            data1 = r1.json()
            if len(data1) > 1:
                result["dados"]["preparo_solo"] = [
                    {"variavel": row.get("D2N", ""), "valor": row.get("V", "0"), "unidade": row.get("MN", "")}
                    for row in data1[1:]
                ]

            # Tabela 6899 - Despesas
            url2 = f"{self.SIDRA_URL}/t/6899/n6/{codigo_municipio}/v/all/p/2017/f/n"
            r2 = await self._http_get(url2, timeout=15.0)
            data2 = r2.json()
            if len(data2) > 1:
                result["dados"]["despesas"] = [
                    {"variavel": row.get("D2N", ""), "valor": row.get("V", "0"), "unidade": row.get("MN", "")}
                    for row in data2[1:]
                ]

            # Tabela 6780 - Producao vegetal
            url3 = f"{self.SIDRA_URL}/t/6780/n6/{codigo_municipio}/v/all/p/2017/f/n"
            r3 = await self._http_get(url3, timeout=15.0)
            data3 = r3.json()
            if len(data3) > 1:
                result["dados"]["producao_vegetal"] = [
                    {"variavel": row.get("D2N", ""), "valor": row.get("V", "0"), "unidade": row.get("MN", "")}
                    for row in data3[1:]
                ]

            self._set_cached(cache_key, result)
        except Exception as e:
            logger.warning("IBGE censo agro failed: %s", e)
            result["error"] = str(e)

        return result

    # Mapa de nomes de culturas para codigos SIDRA
    CULTURA_CODES = {
        "soja": "39", "milho": "33", "cafe": "9", "cana": "31",
        "algodao": "3", "arroz": "40", "trigo": "45", "feijao": "15",
        "sorgo": "2713", "mandioca": "2558", "laranja": "487",
        "banana": "2558", "cacau": "161",
    }
