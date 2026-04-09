"""
Coletor de dados do IBAMA (embargos e infrações ambientais).

Fontes:
- Dados abertos IBAMA: https://dadosabertos.ibama.gov.br
- Consulta de embargos: https://servicos.ibama.gov.br/ctf/publico/areasembargadas/ConsultaPublicaAreasEmbargadas.php
- Consulta de autuações: dados abertos CSV
"""

import logging
import csv
import io
from typing import Optional

from app.collectors.base import BaseCollector
from app.models.schemas import IBAMAEmbargo

logger = logging.getLogger("agrojus")


class IBAMACollector(BaseCollector):
    """Coleta dados de embargos e infrações ambientais do IBAMA."""

    EMBARGOS_CSV_URL = "https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/termo_embargo/termo_embargo.csv"
    EMBARGOS_COORDS_URL = "https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/coordenadas/coordenadas.csv"
    AUTUACOES_CSV_URL = "https://dadosabertos.ibama.gov.br/dados/SIFISC/auto_infracao/auto_infracao/auto_infracao.csv"

    def __init__(self):
        super().__init__("ibama")

    async def search_embargos_by_cpf_cnpj(self, cpf_cnpj: str) -> list[IBAMAEmbargo]:
        """Busca embargos IBAMA por CPF/CNPJ."""
        clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")

        cached = self._get_cached(f"embargo_cpf:{clean}")
        if cached:
            return [IBAMAEmbargo(**item) for item in cached]

        try:
            embargos = await self._fetch_embargos_csv(cpf_cnpj_filter=clean)
            if embargos:
                self._set_cached(
                    f"embargo_cpf:{clean}",
                    [e.model_dump() for e in embargos],
                )
            return embargos
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return []

    async def search_embargos_by_municipality(
        self, municipality: str, state: str
    ) -> list[IBAMAEmbargo]:
        """Busca embargos IBAMA por município."""
        cached = self._get_cached(f"embargo_mun:{state}:{municipality}")
        if cached:
            return [IBAMAEmbargo(**item) for item in cached]

        try:
            embargos = await self._fetch_embargos_csv(
                municipality_filter=municipality, state_filter=state
            )
            if embargos:
                self._set_cached(
                    f"embargo_mun:{state}:{municipality}",
                    [e.model_dump() for e in embargos],
                )
            return embargos
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return []

    async def _fetch_embargos_csv(
        self,
        cpf_cnpj_filter: str = None,
        municipality_filter: str = None,
        state_filter: str = None,
    ) -> list[IBAMAEmbargo]:
        """
        Busca dados de embargos do IBAMA via CSV de dados abertos.

        Note: Em produção, o CSV completo seria baixado periodicamente e
        armazenado no banco de dados. Para o MVP, fazemos a busca direta.
        """
        try:
            response = await self._http_get(self.EMBARGOS_CSV_URL, timeout=120.0)
            content = response.text

            reader = csv.DictReader(io.StringIO(content), delimiter=";")
            results = []

            for row in reader:
                # Apply filters
                if cpf_cnpj_filter:
                    row_cpf = row.get("CPF/CNPJ", "").replace(".", "").replace("/", "").replace("-", "")
                    if row_cpf != cpf_cnpj_filter:
                        continue

                if municipality_filter:
                    if municipality_filter.lower() not in row.get("Município", "").lower():
                        continue

                if state_filter:
                    if state_filter.upper() != row.get("UF", "").upper():
                        continue

                embargo = IBAMAEmbargo(
                    auto_infracao=row.get("Número TAD", ""),
                    cpf_cnpj=row.get("CPF/CNPJ", ""),
                    nome=row.get("Nome", ""),
                    municipio=row.get("Município", ""),
                    uf=row.get("UF", ""),
                    area_embargada_ha=self._safe_float(row.get("Área (ha)", "0")),
                    data_embargo=row.get("Data Embargo", ""),
                    descricao=row.get("Infração", ""),
                    status=row.get("Situação", ""),
                )
                results.append(embargo)

                # Limit results
                if len(results) >= 100:
                    break

            return results
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return []

    @staticmethod
    def _safe_float(value: str) -> Optional[float]:
        try:
            return float(value.replace(",", "."))
        except (ValueError, AttributeError):
            return None
