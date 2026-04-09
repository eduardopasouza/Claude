"""
Coletor de dados financeiros do agronegócio.

Fontes:
- SICOR/BCB: Crédito rural (API do Banco Central)
- FNP/ESALQ: Preços de terras
- CVM: Fundos imobiliários rurais (FIAGRO)
- BNDES: Operações de financiamento
"""

from typing import Optional

from app.collectors.base import BaseCollector
from app.models.schemas import RuralCreditRecord, LandPriceData, FinancialSummary


class FinancialDataCollector(BaseCollector):
    """Coleta dados financeiros do agronegócio."""

    # SICOR - Sistema de Operações do Crédito Rural e do Proagro
    SICOR_API_URL = "https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata"

    # BCB Open Data
    BCB_OPENDATA_URL = "https://dadosabertos.bcb.gov.br/dataset"

    def __init__(self):
        super().__init__("financial")

    async def get_rural_credits_by_cpf_cnpj(self, cpf_cnpj: str) -> list[RuralCreditRecord]:
        """
        Busca créditos rurais vinculados a um CPF/CNPJ via SICOR/BCB.

        Note: O SICOR público não permite busca por CPF/CNPJ individual
        por questões de sigilo. Disponibiliza dados agregados por município.
        Para busca individual seria necessário convênio com BCB.
        """
        clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")

        cached = self._get_cached(f"credit:{clean}")
        if cached:
            return [RuralCreditRecord(**item) for item in cached]

        # SICOR public API only provides aggregate data by municipality
        # Individual lookups require institutional access
        return []

    async def get_rural_credits_by_municipality(
        self, municipality_code: str, year: int = 2025
    ) -> list[RuralCreditRecord]:
        """
        Busca créditos rurais por município via SICOR/BCB (dados agregados).
        Dados públicos do Banco Central.
        """
        cached = self._get_cached(f"credit_mun:{municipality_code}:{year}")
        if cached:
            return [RuralCreditRecord(**item) for item in cached]

        try:
            # SICOR OData API - aggregate by municipality
            url = (
                f"{self.SICOR_API_URL}/RecursosMunicipios"
                f"?$filter=AnoEmissao eq '{year}' and cdMunicipio eq '{municipality_code}'"
                f"&$format=json"
                f"&$top=100"
            )

            response = await self._http_get(url, timeout=30.0)
            data = response.json()

            records = []
            for item in data.get("value", []):
                record = RuralCreditRecord(
                    bank=item.get("InstituicaoFinanceira"),
                    credit_line=item.get("Programa"),
                    purpose=item.get("Finalidade"),
                    amount=self._safe_float(item.get("VlCusteio", "0")),
                    municipality=item.get("Municipio"),
                    state=item.get("UF"),
                    year=year,
                    crop=item.get("Produto"),
                )
                records.append(record)

            if records:
                self._set_cached(
                    f"credit_mun:{municipality_code}:{year}",
                    [r.model_dump() for r in records],
                )
            return records
        except Exception as e:
            print(f"[FINANCIAL] Error fetching SICOR data: {e}")
            return []

    async def get_land_prices(
        self, state: str, municipality: Optional[str] = None
    ) -> list[LandPriceData]:
        """
        Busca preços de terras por região.

        Note: FNP/ESALQ publica dados de preços de terras, mas não tem API pública.
        Em produção, os dados seriam importados periodicamente.
        Alternativa: IEA (SP), FAEG (GO), dados de leilões públicos.
        """
        cached = self._get_cached(f"land_price:{state}:{municipality or 'all'}")
        if cached:
            return [LandPriceData(**item) for item in cached]

        # Placeholder - land price data would be periodically imported
        return []

    async def get_financial_summary_by_municipality(
        self, municipality_code: str
    ) -> FinancialSummary:
        """Gera resumo financeiro de um município."""
        credits = await self.get_rural_credits_by_municipality(municipality_code)
        total = sum(c.amount or 0 for c in credits)

        return FinancialSummary(
            rural_credits=credits,
            total_credit_amount=total if total > 0 else None,
            land_prices=[],
            avg_land_price_per_ha=None,
        )

    async def get_fiagro_funds(self) -> list[dict]:
        """
        Busca informações sobre fundos FIAGRO (CVM).

        Note: CVM disponibiliza dados de fundos via dados abertos.
        Em produção, seriam baixados e processados periodicamente.
        """
        cached = self._get_cached("fiagro_funds")
        if cached:
            return cached

        # Placeholder - CVM data would be periodically imported
        return []

    @staticmethod
    def _safe_float(value) -> Optional[float]:
        try:
            if isinstance(value, str):
                return float(value.replace(",", "."))
            return float(value)
        except (ValueError, TypeError):
            return None
