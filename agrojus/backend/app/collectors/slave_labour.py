"""
Coletor da Lista Suja do Trabalho Escravo (MTE).

Fontes:
- Dados abertos MTE: cadastro de empregadores que submeteram trabalhadores
  a condições análogas à de escravo
- Portal da Transparência: https://portaldatransparencia.gov.br
"""

import logging
from typing import Optional

from app.collectors.base import BaseCollector
from app.models.schemas import SlaveLabourEntry

logger = logging.getLogger("agrojus")


class SlaveLabourCollector(BaseCollector):
    """Coleta dados da Lista Suja do Trabalho Escravo."""

    # URL dos dados abertos do MTE (cadastro de empregadores)
    LISTA_SUJA_URL = "https://portaldatransparencia.gov.br/download-de-dados/trabalho-escravo"

    def __init__(self):
        super().__init__("slave_labour")

    async def search_by_cpf_cnpj(self, cpf_cnpj: str) -> list[SlaveLabourEntry]:
        """Busca registros na lista suja por CPF/CNPJ."""
        clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")

        cached = self._get_cached(f"slave:{clean}")
        if cached:
            return [SlaveLabourEntry(**item) for item in cached]

        try:
            entries = await self._fetch_slave_labour_data(cpf_cnpj_filter=clean)
            self._set_cached(
                f"slave:{clean}",
                [e.model_dump() for e in entries],
            )
            return entries
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return []

    async def search_by_name(self, name: str) -> list[SlaveLabourEntry]:
        """Busca registros na lista suja por nome."""
        cached = self._get_cached(f"slave_name:{name.lower()}")
        if cached:
            return [SlaveLabourEntry(**item) for item in cached]

        try:
            entries = await self._fetch_slave_labour_data(name_filter=name)
            self._set_cached(
                f"slave_name:{name.lower()}",
                [e.model_dump() for e in entries],
            )
            return entries
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return []

    async def search_by_municipality(self, municipality: str, state: str) -> list[SlaveLabourEntry]:
        """Busca registros na lista suja por município."""
        cached = self._get_cached(f"slave_mun:{state}:{municipality}")
        if cached:
            return [SlaveLabourEntry(**item) for item in cached]

        try:
            entries = await self._fetch_slave_labour_data(
                municipality_filter=municipality, state_filter=state
            )
            self._set_cached(
                f"slave_mun:{state}:{municipality}",
                [e.model_dump() for e in entries],
            )
            return entries
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return []

    async def _fetch_slave_labour_data(
        self,
        cpf_cnpj_filter: str = None,
        name_filter: str = None,
        municipality_filter: str = None,
        state_filter: str = None,
    ) -> list[SlaveLabourEntry]:
        """
        Busca dados da lista suja.

        Note: Em produção, o dataset seria baixado periodicamente do Portal da
        Transparência e armazenado no banco. Para o MVP, simulamos a estrutura
        e a busca seria feita contra o banco local.
        """
        # The actual data would be fetched from Portal da Transparência
        # and stored in the database. The search would then be against the DB.
        # For now, we return an empty list as the data source requires
        # periodic download and import.
        return []

    async def import_data_from_csv(self, csv_path: str) -> int:
        """
        Importa dados da lista suja a partir de CSV baixado do Portal da Transparência.

        Returns: número de registros importados.
        """
        import csv

        count = 0
        try:
            with open(csv_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f, delimiter=";")
                entries = []

                for row in reader:
                    entry = SlaveLabourEntry(
                        employer_name=row.get("EMPREGADOR"),
                        cpf_cnpj=row.get("CPF/CNPJ"),
                        establishment=row.get("ESTABELECIMENTO"),
                        municipality=row.get("MUNICÍPIO"),
                        state=row.get("UF"),
                        workers_rescued=self._safe_int(row.get("TRABALHADORES ENVOLVIDOS", "0")),
                        inspection_date=row.get("DATA DA FISCALIZAÇÃO"),
                    )
                    entries.append(entry)
                    count += 1

            # In production, these would be stored in the database
            logger.info("%s: %s", type(e).__name__, e)
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)

        return count

    @staticmethod
    def _safe_int(value: str) -> Optional[int]:
        try:
            return int(value)
        except (ValueError, AttributeError):
            return None
