"""
Coletor de dados da Receita Federal (CNPJ).

Fontes:
- BrasilAPI: https://brasilapi.com.br/api/cnpj/v1/{cnpj} (API pública gratuita)
- ReceitaWS: https://www.receitaws.com.br/v1/cnpj/{cnpj} (alternativa)
"""

from typing import Optional

from app.collectors.base import BaseCollector
from app.models.schemas import CNPJData
from app.config import settings


class ReceitaFederalCollector(BaseCollector):
    """Coleta dados cadastrais de CNPJ da Receita Federal."""

    def __init__(self):
        super().__init__("receita_federal")
        self.api_url = settings.receita_federal_url

    async def get_cnpj(self, cnpj: str) -> Optional[CNPJData]:
        """Busca dados cadastrais de um CNPJ."""
        # Clean CNPJ (remove formatting)
        cnpj_clean = cnpj.replace(".", "").replace("/", "").replace("-", "")

        cached = self._get_cached(f"cnpj:{cnpj_clean}")
        if cached:
            return CNPJData(**cached)

        try:
            data = await self._fetch_cnpj_brasilapi(cnpj_clean)
            if data:
                self._set_cached(f"cnpj:{cnpj_clean}", data.model_dump())
            return data
        except Exception as e:
            print(f"[RECEITA] Error fetching CNPJ {cnpj}: {e}")
            return None

    async def _fetch_cnpj_brasilapi(self, cnpj: str) -> Optional[CNPJData]:
        """Consulta CNPJ via BrasilAPI (pública e gratuita)."""
        url = f"{self.api_url}/{cnpj}"

        try:
            response = await self._http_get(url, timeout=15.0)
            if response.status_code == 200:
                result = response.json()

                socios = []
                for socio in result.get("qsa", []):
                    socios.append({
                        "nome": socio.get("nome_socio"),
                        "cpf_cnpj": socio.get("cnpj_cpf_do_socio"),
                        "qualificacao": socio.get("qualificacao_socio"),
                    })

                endereco_parts = [
                    result.get("logradouro", ""),
                    result.get("numero", ""),
                    result.get("complemento", ""),
                    result.get("bairro", ""),
                ]
                endereco = ", ".join(p for p in endereco_parts if p)

                return CNPJData(
                    cnpj=cnpj,
                    razao_social=result.get("razao_social"),
                    nome_fantasia=result.get("nome_fantasia"),
                    situacao_cadastral=result.get("descricao_situacao_cadastral"),
                    data_situacao_cadastral=result.get("data_situacao_cadastral"),
                    cnae_principal=result.get("cnae_fiscal_descricao"),
                    endereco=endereco,
                    municipio=result.get("municipio"),
                    uf=result.get("uf"),
                    socios=socios,
                )
        except Exception:
            pass

        return None

    async def validate_cpf_cnpj(self, document: str) -> dict:
        """Verifica se um CPF/CNPJ é válido e retorna tipo."""
        clean = document.replace(".", "").replace("/", "").replace("-", "")

        if len(clean) == 11:
            return {"type": "CPF", "valid": self._validate_cpf(clean), "document": clean}
        elif len(clean) == 14:
            return {"type": "CNPJ", "valid": self._validate_cnpj(clean), "document": clean}
        else:
            return {"type": "unknown", "valid": False, "document": clean}

    @staticmethod
    def _validate_cpf(cpf: str) -> bool:
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        for i in range(9, 11):
            total = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
            digit = (total * 10) % 11
            if digit == 10:
                digit = 0
            if int(cpf[i]) != digit:
                return False
        return True

    @staticmethod
    def _validate_cnpj(cnpj: str) -> bool:
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False

        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        total = sum(int(cnpj[i]) * weights1[i] for i in range(12))
        digit1 = 11 - (total % 11)
        if digit1 >= 10:
            digit1 = 0

        total = sum(int(cnpj[i]) * weights2[i] for i in range(13))
        digit2 = 11 - (total % 11)
        if digit2 >= 10:
            digit2 = 0

        return int(cnpj[12]) == digit1 and int(cnpj[13]) == digit2
