"""
Coletor de protestos de titulos via CENPROT/IEPTB.

Fontes:
- CENPROT Nacional: pesquisaprotesto.com.br (consulta publica)
- CENPROT SP: protestosp.com.br (consulta gratuita por CPF/CNPJ)

Status: Sites bloqueiam acesso automatizado (403).
Para producao: integrar via InfoSimples API ou parceria direta com IEPTB.
Custo estimado: R$0.20/consulta via InfoSimples.
"""

import logging
from typing import Optional
from pydantic import BaseModel

from app.collectors.base import BaseCollector

logger = logging.getLogger("agrojus")


class ProtestoRecord(BaseModel):
    """Registro de protesto de titulo."""
    cpf_cnpj: str
    has_protests: Optional[bool] = None
    total_protests: int = 0
    protests: list[dict] = []
    source: str = "CENPROT/IEPTB"
    status: str = "consulted"


class ProtestosCollector(BaseCollector):
    """Consulta protestos de titulos via CENPROT."""

    CENPROT_URL = "https://www.pesquisaprotesto.com.br"
    CENPROT_SP_URL = "https://protestosp.com.br/consulta-de-protesto"

    def __init__(self):
        super().__init__("protestos")

    async def consultar_protestos(self, cpf_cnpj: str) -> ProtestoRecord:
        """
        Consulta protestos por CPF/CNPJ.

        Tentativa de acesso direto ao CENPROT.
        Se bloqueado, retorna status indicando necessidade de consulta manual.
        """
        clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")

        cached = self._get_cached(f"protesto:{clean}")
        if cached:
            return ProtestoRecord(**cached)

        result = ProtestoRecord(
            cpf_cnpj=clean,
            status="unavailable",
            source="CENPROT (acesso automatizado bloqueado - consulte manualmente em pesquisaprotesto.com.br)",
        )

        # Tentar scraping do CENPROT
        try:
            data = await self._fetch_cenprot(clean)
            if data:
                result = data
        except Exception as e:
            logger.info("CENPROT blocked as expected: %s", type(e).__name__)

        self._set_cached(f"protesto:{clean}", result.model_dump())
        return result

    async def _fetch_cenprot(self, cpf_cnpj: str) -> Optional[ProtestoRecord]:
        """Tentativa de consulta ao CENPROT."""
        try:
            response = await self._http_get(
                self.CENPROT_URL,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                },
                timeout=15.0,
            )
            if response.status_code == 200:
                # Parse response for protest data
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, "html.parser")
                # Structure depends on site layout
                logger.info("CENPROT accessible, parsing...")
                return None  # Will be implemented when access is available
        except Exception:
            pass
        return None
