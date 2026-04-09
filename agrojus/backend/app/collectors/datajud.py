"""
Coletor de dados judiciais via DataJud (CNJ).

O DataJud é a base nacional de dados do Poder Judiciário,
mantida pelo CNJ (Conselho Nacional de Justiça).

API pública: https://datajud-wiki.cnj.jus.br/
Permite buscar processos por CPF/CNPJ do envolvido, assunto, tribunal, etc.
"""

from typing import Optional

from app.collectors.base import BaseCollector
from app.models.schemas import LawsuitRecord


# Tribunais disponíveis no DataJud
TRIBUNAIS = {
    # Justiça Estadual (1ª instância)
    "TJAC": "8.01", "TJAL": "8.02", "TJAM": "8.04", "TJAP": "8.03",
    "TJBA": "8.05", "TJCE": "8.06", "TJDFT": "8.07", "TJES": "8.08",
    "TJGO": "8.09", "TJMA": "8.10", "TJMG": "8.13", "TJMS": "8.12",
    "TJMT": "8.11", "TJPA": "8.14", "TJPB": "8.15", "TJPE": "8.17",
    "TJPI": "8.18", "TJPR": "8.16", "TJRJ": "8.19", "TJRN": "8.20",
    "TJRO": "8.22", "TJRR": "8.23", "TJRS": "8.21", "TJSC": "8.24",
    "TJSE": "8.25", "TJSP": "8.26", "TJTO": "8.27",
    # Justiça Federal
    "TRF1": "5.01", "TRF2": "5.02", "TRF3": "5.03", "TRF4": "5.04",
    "TRF5": "5.05", "TRF6": "5.06",
    # Justiça do Trabalho
    "TRT1": "6.01", "TRT2": "6.02", "TRT3": "6.03", "TRT4": "6.04",
    "TRT5": "6.05", "TRT6": "6.06", "TRT7": "6.07", "TRT8": "6.08",
    "TRT9": "6.09", "TRT10": "6.10", "TRT11": "6.11", "TRT12": "6.12",
    "TRT13": "6.13", "TRT14": "6.14", "TRT15": "6.15", "TRT16": "6.16",
    "TRT17": "6.17", "TRT18": "6.18", "TRT19": "6.19", "TRT20": "6.20",
    "TRT21": "6.21", "TRT22": "6.22", "TRT23": "6.23", "TRT24": "6.24",
}

# Assuntos relevantes para agronegócio (códigos TPU do CNJ)
ASSUNTOS_AGRO = {
    "10432": "Usucapião",
    "10445": "Desapropriação",
    "10452": "Servidão",
    "10455": "Posse",
    "10456": "Propriedade",
    "10673": "Dano Ambiental",
    "11793": "Trabalho Rural",
    "14045": "Contratos Agrários",
    "14046": "Arrendamento Rural",
    "14047": "Parceria Rural",
}


DATAJUD_API_URL = "https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal}/_search"


class DataJudCollector(BaseCollector):
    """Coleta dados de processos judiciais via DataJud/CNJ."""

    def __init__(self):
        super().__init__("datajud")
        self.api_key = ""  # API pública, mas requer cadastro para chave

    async def search_by_cpf_cnpj(
        self,
        cpf_cnpj: str,
        tribunais: list[str] = None,
        max_results: int = 20,
    ) -> list[LawsuitRecord]:
        """
        Busca processos judiciais por CPF/CNPJ em um ou mais tribunais.

        Se nenhum tribunal for especificado, busca nos TRFs (Justiça Federal)
        e nos TRTs (Justiça do Trabalho) por serem mais relevantes para
        questões agrárias.
        """
        clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")

        cached = self._get_cached(f"lawsuit:{clean}")
        if cached:
            return [LawsuitRecord(**item) for item in cached]

        if not tribunais:
            # Default: busca nos tribunais mais relevantes para agro
            tribunais = ["TRF1", "TRF2", "TRF3", "TRF4", "TRF5", "TRF6"]

        all_records = []
        for tribunal in tribunais:
            try:
                records = await self._search_tribunal(clean, tribunal, max_results)
                all_records.extend(records)
            except Exception as e:
                print(f"[DATAJUD] Error searching {tribunal}: {e}")

        if all_records:
            self._set_cached(
                f"lawsuit:{clean}",
                [r.model_dump() for r in all_records],
            )

        return all_records

    async def search_by_subject(
        self,
        subject_code: str,
        tribunal: str,
        municipality: str = None,
        max_results: int = 20,
    ) -> list[LawsuitRecord]:
        """Busca processos por assunto (código TPU) em um tribunal."""
        cache_key = f"subject:{tribunal}:{subject_code}:{municipality or 'all'}"
        cached = self._get_cached(cache_key)
        if cached:
            return [LawsuitRecord(**item) for item in cached]

        try:
            records = await self._search_by_subject_tribunal(
                subject_code, tribunal, municipality, max_results
            )
            if records:
                self._set_cached(cache_key, [r.model_dump() for r in records])
            return records
        except Exception as e:
            print(f"[DATAJUD] Error searching subject {subject_code} in {tribunal}: {e}")
            return []

    async def _search_tribunal(
        self, cpf_cnpj: str, tribunal: str, max_results: int
    ) -> list[LawsuitRecord]:
        """Busca processos em um tribunal específico via DataJud."""
        tribunal_code = TRIBUNAIS.get(tribunal)
        if not tribunal_code:
            return []

        url = DATAJUD_API_URL.format(tribunal=tribunal.lower())

        # DataJud uses Elasticsearch query syntax
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "numeroDocumentoPrincipal": cpf_cnpj
                            }
                        }
                    ]
                }
            },
            "size": max_results,
            "sort": [{"dataAjuizamento": {"order": "desc"}}],
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"APIKey {self.api_key}" if self.api_key else "",
        }

        try:
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=query, headers=headers)

                if response.status_code == 200:
                    return self._parse_datajud_response(response.json(), tribunal)
                elif response.status_code == 401:
                    print(f"[DATAJUD] API key required for {tribunal}")
                else:
                    print(f"[DATAJUD] {tribunal} returned {response.status_code}")
        except Exception as e:
            print(f"[DATAJUD] Connection error for {tribunal}: {e}")

        return []

    async def _search_by_subject_tribunal(
        self, subject_code: str, tribunal: str, municipality: str, max_results: int
    ) -> list[LawsuitRecord]:
        """Busca processos por assunto em um tribunal."""
        tribunal_code = TRIBUNAIS.get(tribunal)
        if not tribunal_code:
            return []

        url = DATAJUD_API_URL.format(tribunal=tribunal.lower())

        must_clauses = [
            {"match": {"assuntos.codigoNacional": subject_code}}
        ]
        if municipality:
            must_clauses.append(
                {"match": {"orgaoJulgador.municipio": municipality}}
            )

        query = {
            "query": {"bool": {"must": must_clauses}},
            "size": max_results,
            "sort": [{"dataAjuizamento": {"order": "desc"}}],
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"APIKey {self.api_key}" if self.api_key else "",
        }

        try:
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=query, headers=headers)
                if response.status_code == 200:
                    return self._parse_datajud_response(response.json(), tribunal)
        except Exception:
            pass

        return []

    def _parse_datajud_response(
        self, data: dict, tribunal: str
    ) -> list[LawsuitRecord]:
        """Parse resposta do DataJud."""
        records = []
        hits = data.get("hits", {}).get("hits", [])

        for hit in hits:
            source = hit.get("_source", {})

            # Extract subjects
            subjects = []
            for assunto in source.get("assuntos", []):
                subjects.append(assunto.get("nome", ""))

            # Extract parties
            parties = []
            for movimento in source.get("movimentos", [])[:3]:
                parties.append(movimento.get("nome", ""))

            # Extract court info
            orgao = source.get("orgaoJulgador", {})

            record = LawsuitRecord(
                case_number=source.get("numeroProcesso"),
                tribunal=tribunal,
                court=orgao.get("nomeOrgao"),
                municipality=orgao.get("municipio"),
                state=orgao.get("codigoMunicipioIBGE", "")[:2] if orgao.get("codigoMunicipioIBGE") else None,
                subjects=subjects,
                class_name=source.get("classe", {}).get("nome"),
                filing_date=source.get("dataAjuizamento"),
                last_update=source.get("dataUltimaAtualizacao"),
                status=source.get("situacao", {}).get("nome") if source.get("situacao") else None,
                degree=source.get("grau"),
                system=source.get("sistema", {}).get("nome") if source.get("sistema") else None,
            )
            records.append(record)

        return records
