"""
Coletor de dados de CPF na Receita Federal.

Fontes:
- Consulta publica: servicos.receita.fazenda.gov.br (requer captcha + data nascimento)
- SERPRO API: loja.serpro.gov.br (pago, R$0.66/consulta)
- Para o MVP: validacao local + dados basicos via BrasilAPI quando CNPJ

Status: A consulta publica da RF exige reCAPTCHA.
Para producao, integrar via SERPRO API ou servico de captcha.
"""

import logging
from typing import Optional
from pydantic import BaseModel

from app.collectors.base import BaseCollector
from app.collectors.receita_federal import ReceitaFederalCollector

logger = logging.getLogger("agrojus")


class CPFData(BaseModel):
    """Dados de CPF consultado."""
    cpf: str
    valid: bool
    name: Optional[str] = None
    situation: Optional[str] = None  # Regular, Suspensa, Cancelada, etc.
    birth_date: Optional[str] = None
    registration_date: Optional[str] = None
    source: str = "Validacao local"


class CPFCollector(BaseCollector):
    """Consulta dados de CPF."""

    RECEITA_URL = "https://servicos.receita.fazenda.gov.br/servicos/cpf/consultasituacao/ConsultaPublicaExibir.asp"
    SERPRO_URL = "https://gateway.apiserpro.serpro.gov.br/consulta-cpf-df/v1/cpf"

    def __init__(self):
        super().__init__("cpf")
        from app.config import settings
        self.serpro_token = getattr(settings, "serpro_api_token", "")

    async def consultar_cpf(self, cpf: str) -> CPFData:
        """
        Consulta CPF usando a melhor fonte disponivel.

        Ordem de prioridade:
        1. SERPRO API (se token configurado)
        2. Validacao local + dados disponiveis
        """
        clean = cpf.replace(".", "").replace("-", "")

        cached = self._get_cached(f"cpf:{clean}")
        if cached:
            return CPFData(**cached)

        # Validar localmente
        rf = ReceitaFederalCollector()
        is_valid = rf._validate_cpf(clean)

        result = CPFData(
            cpf=clean,
            valid=is_valid,
        )

        # Tentar SERPRO se configurado
        if self.serpro_token and is_valid:
            serpro_data = await self._consultar_serpro(clean)
            if serpro_data:
                result = serpro_data

        if not result.name:
            result.source = "Validacao algoritmica (SERPRO API nao configurada)"

        self._set_cached(f"cpf:{clean}", result.model_dump())
        return result

    async def _consultar_serpro(self, cpf: str) -> Optional[CPFData]:
        """Consulta CPF via SERPRO API (pago)."""
        try:
            response = await self._http_get(
                f"{self.SERPRO_URL}/{cpf}",
                headers={
                    "Authorization": f"Bearer {self.serpro_token}",
                    "Accept": "application/json",
                },
                timeout=15.0,
            )
            if response.status_code == 200:
                data = response.json()
                return CPFData(
                    cpf=cpf,
                    valid=True,
                    name=data.get("nome"),
                    situation=data.get("situacao", {}).get("descricao"),
                    birth_date=data.get("nascimento"),
                    registration_date=data.get("inscricao"),
                    source="SERPRO API",
                )
        except Exception as e:
            logger.warning("SERPRO CPF query failed: %s", e)
        return None
