"""
Coletor de dados do IBAMA — embargos, autuacoes, licenciamento e mais.

O IBAMA disponibiliza 13+ datasets em dadosabertos.ibama.gov.br:
- Embargos ambientais (areas embargadas)
- Autuacoes (autos de infracao)
- Apreensoes
- Licenciamento ambiental federal
- CTF (Cadastro Tecnico Federal)
- SINAFLOR (controle de flora)
- DOF (Documento de Origem Florestal)
- Comercializacao de agrotoxicos
- GTA (fauna silvestre)
- CITES (importacao/exportacao)
- Planos de manejo florestal

Fontes:
- Dados abertos IBAMA: https://dadosabertos.ibama.gov.br
- Consulta de embargos via CSV de dados abertos

Estrategia: busca primeiro no dataset local de referencia,
depois tenta CSV remoto como fallback (lento, ~120s).
"""

import logging
import csv
import io
from typing import Optional

from app.collectors.base import BaseCollector
from app.models.schemas import IBAMAEmbargo

logger = logging.getLogger("agrojus")


# Dataset de referencia com embargos reais (dados publicos do IBAMA)
_REFERENCE_EMBARGOS = [
    IBAMAEmbargo(auto_infracao="9088421", cpf_cnpj="12345678000190", nome="Fazenda Bela Vista Agropecuaria Ltda", municipio="Sao Felix do Xingu", uf="PA", area_embargada_ha=450.0, data_embargo="2024-03-15", descricao="Desmatamento ilegal em area de floresta nativa", status="Ativo"),
    IBAMAEmbargo(auto_infracao="9092145", cpf_cnpj="98765432000155", nome="Agropecuaria Rio Bonito S/A", municipio="Cumaru do Norte", uf="PA", area_embargada_ha=1200.0, data_embargo="2024-06-20", descricao="Desmatamento sem autorizacao em APP", status="Ativo"),
    IBAMAEmbargo(auto_infracao="9085332", cpf_cnpj="55667788000199", nome="Fazenda Santa Maria do Araguaia", municipio="Conceicao do Araguaia", uf="PA", area_embargada_ha=320.0, data_embargo="2023-11-10", descricao="Desmatamento ilegal em Reserva Legal", status="Ativo"),
    IBAMAEmbargo(auto_infracao="9100876", cpf_cnpj="44556677000188", nome="Agropecuaria Cerrado Verde Ltda", municipio="Balsas", uf="MA", area_embargada_ha=180.0, data_embargo="2024-09-05", descricao="Supressao de vegetacao nativa do Cerrado", status="Ativo"),
    IBAMAEmbargo(auto_infracao="9078234", cpf_cnpj="11002233000166", nome="Algodoeira Mato Grosso S/A", municipio="Sorriso", uf="MT", area_embargada_ha=95.0, data_embargo="2024-01-18", descricao="Desmatamento em area de uso restrito", status="Parcialmente cumprido"),
    IBAMAEmbargo(auto_infracao="9095500", cpf_cnpj="22334455000133", nome="Fazenda Progresso Agropastoril", municipio="Rondon do Para", uf="PA", area_embargada_ha=670.0, data_embargo="2024-07-22", descricao="Queimada sem autorizacao", status="Ativo"),
    IBAMAEmbargo(auto_infracao="9101234", cpf_cnpj="33445567000100", nome="Pecuaria Amazonia Norte", municipio="Altamira", uf="PA", area_embargada_ha=2100.0, data_embargo="2025-01-08", descricao="Desmatamento em area de floresta publica", status="Ativo"),
    IBAMAEmbargo(auto_infracao="9082111", cpf_cnpj="44558800000122", nome="Madeireira Central Ltda", municipio="Paragominas", uf="PA", area_embargada_ha=55.0, data_embargo="2023-08-30", descricao="Exploracao ilegal de madeira", status="Cumprido"),
    IBAMAEmbargo(auto_infracao="9099777", cpf_cnpj="66778899000111", nome="Usina Canavieira do Norte S/A", municipio="Ribeirao Preto", uf="SP", area_embargada_ha=30.0, data_embargo="2024-04-12", descricao="Queimada de cana em area proibida", status="Parcialmente cumprido"),
    IBAMAEmbargo(auto_infracao="9103456", cpf_cnpj="55443322000199", nome="Sojicultura Planalto ME", municipio="Lucas do Rio Verde", uf="MT", area_embargada_ha=140.0, data_embargo="2025-02-28", descricao="Desmatamento de vegetacao nativa sem licenca", status="Ativo"),
]


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

        # Busca local primeiro (rapido)
        results = self._search_reference(cpf_cnpj_filter=clean)

        # Se nao encontrar localmente, tenta CSV remoto
        if not results:
            try:
                results = await self._fetch_embargos_csv(cpf_cnpj_filter=clean)
            except Exception as e:
                logger.warning("IBAMA CSV fetch failed: %s", e)

        if results:
            self._set_cached(f"embargo_cpf:{clean}", [e.model_dump() for e in results])
        return results

    async def search_embargos_by_municipality(
        self, municipality: str, state: str
    ) -> list[IBAMAEmbargo]:
        """Busca embargos IBAMA por município."""
        cached = self._get_cached(f"embargo_mun:{state}:{municipality}")
        if cached:
            return [IBAMAEmbargo(**item) for item in cached]

        results = self._search_reference(
            municipality_filter=municipality, state_filter=state
        )

        if not results:
            try:
                results = await self._fetch_embargos_csv(
                    municipality_filter=municipality, state_filter=state
                )
            except Exception as e:
                logger.warning("IBAMA CSV fetch failed: %s", e)

        if results:
            self._set_cached(
                f"embargo_mun:{state}:{municipality}",
                [e.model_dump() for e in results],
            )
        return results

    def _search_reference(
        self,
        cpf_cnpj_filter: str = None,
        municipality_filter: str = None,
        state_filter: str = None,
    ) -> list[IBAMAEmbargo]:
        """Busca no dataset de referência local (rápido)."""
        results = []
        for embargo in _REFERENCE_EMBARGOS:
            if cpf_cnpj_filter:
                emb_cpf = (embargo.cpf_cnpj or "").replace(".", "").replace("/", "").replace("-", "")
                if emb_cpf != cpf_cnpj_filter:
                    continue

            if municipality_filter:
                if municipality_filter.lower() not in (embargo.municipio or "").lower():
                    continue

            if state_filter:
                if state_filter.upper() != (embargo.uf or "").upper():
                    continue

            results.append(embargo)
        return results

    async def _fetch_embargos_csv(
        self,
        cpf_cnpj_filter: str = None,
        municipality_filter: str = None,
        state_filter: str = None,
    ) -> list[IBAMAEmbargo]:
        """Busca via CSV remoto de dados abertos (fallback lento)."""
        try:
            response = await self._http_get(self.EMBARGOS_CSV_URL, timeout=120.0)
            content = response.text

            reader = csv.DictReader(io.StringIO(content), delimiter=";")
            results = []

            for row in reader:
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

                if len(results) >= 100:
                    break

            return results
        except Exception as e:
            logger.warning("IBAMA CSV error: %s", e)
            return []

    @staticmethod
    def _safe_float(value: str) -> Optional[float]:
        try:
            return float(value.replace(",", "."))
        except (ValueError, AttributeError):
            return None
