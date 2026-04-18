"""
Testes unit do parser DataJud.

Função sob teste:
  DataJudCollector._parse_datajud_response(data, tribunal) -> list[LawsuitRecord]

Também testa constantes:
  TRIBUNAIS (mapa tribunal → codigo TPU CNJ)
  ASSUNTOS_AGRO (assuntos relevantes pro agro)
"""

from __future__ import annotations

import pytest

from app.collectors.datajud import ASSUNTOS_AGRO, TRIBUNAIS, DataJudCollector
from app.models.schemas import LawsuitRecord


def _elasticsearch_hits(sources: list[dict]) -> dict:
    """Shape real da resposta Elasticsearch usada pelo DataJud."""
    return {
        "hits": {
            "total": {"value": len(sources), "relation": "eq"},
            "hits": [{"_source": s, "_index": "x", "_id": str(i)} for i, s in enumerate(sources)],
        }
    }


@pytest.mark.unit
class TestParseDataJudResponse:
    def test_resposta_vazia_retorna_lista_vazia(self):
        collector = DataJudCollector()
        result = collector._parse_datajud_response(_elasticsearch_hits([]), "TRF1")
        assert result == []

    def test_extrai_campos_basicos_do_processo(self):
        collector = DataJudCollector()
        source = {
            "numeroProcesso": "0001234-56.2024.4.01.0000",
            "dataAjuizamento": "2024-03-15T00:00:00",
            "dataUltimaAtualizacao": "2024-05-20T00:00:00",
            "classe": {"nome": "Ação Civil Pública"},
            "orgaoJulgador": {
                "nomeOrgao": "1ª Vara Federal",
                "municipio": "São Luís",
                "codigoMunicipioIBGE": "2111300",
            },
            "situacao": {"nome": "Em tramitação"},
            "grau": "G1",
            "sistema": {"nome": "PJe"},
            "assuntos": [{"nome": "Dano Ambiental"}, {"nome": "Multa"}],
        }

        result = collector._parse_datajud_response(_elasticsearch_hits([source]), "TRF1")
        assert len(result) == 1
        r = result[0]
        assert isinstance(r, LawsuitRecord)
        assert r.case_number == "0001234-56.2024.4.01.0000"
        assert r.tribunal == "TRF1"
        assert r.court == "1ª Vara Federal"
        assert r.municipality == "São Luís"
        assert r.class_name == "Ação Civil Pública"
        assert r.status == "Em tramitação"
        assert r.degree == "G1"
        assert r.system == "PJe"
        assert r.subjects == ["Dano Ambiental", "Multa"]

    def test_state_extraido_dos_2_primeiros_digitos_do_municipio(self):
        """codigoMunicipioIBGE = 2111300 → UF = 21 = MA."""
        collector = DataJudCollector()
        source = {
            "numeroProcesso": "X",
            "orgaoJulgador": {"codigoMunicipioIBGE": "2111300"},
        }
        result = collector._parse_datajud_response(_elasticsearch_hits([source]), "TRF1")
        assert result[0].state == "21"

    def test_sem_codigoMunicipioIBGE_state_e_none(self):
        collector = DataJudCollector()
        source = {"numeroProcesso": "X", "orgaoJulgador": {}}
        result = collector._parse_datajud_response(_elasticsearch_hits([source]), "TRF1")
        assert result[0].state is None

    def test_campos_opcionais_ausentes_nao_quebram(self):
        """situacao, sistema, classe podem vir nulos — parser tolera."""
        collector = DataJudCollector()
        source = {
            "numeroProcesso": "X",
            "situacao": None,
            "sistema": None,
            "orgaoJulgador": {},
        }
        result = collector._parse_datajud_response(_elasticsearch_hits([source]), "TRF1")
        assert result[0].status is None
        assert result[0].system is None

    def test_multiplos_processos_na_resposta(self):
        collector = DataJudCollector()
        sources = [
            {"numeroProcesso": "proc-1", "orgaoJulgador": {}},
            {"numeroProcesso": "proc-2", "orgaoJulgador": {}},
            {"numeroProcesso": "proc-3", "orgaoJulgador": {}},
        ]
        result = collector._parse_datajud_response(_elasticsearch_hits(sources), "TRF1")
        assert [r.case_number for r in result] == ["proc-1", "proc-2", "proc-3"]

    def test_subjects_vazio_quando_assuntos_ausente(self):
        collector = DataJudCollector()
        source = {"numeroProcesso": "X", "orgaoJulgador": {}}
        result = collector._parse_datajud_response(_elasticsearch_hits([source]), "TRF1")
        assert result[0].subjects == []


@pytest.mark.unit
class TestTribunaisConstante:
    def test_todos_27_tjs_presentes(self):
        tjs = [k for k in TRIBUNAIS if k.startswith("TJ")]
        assert len(tjs) == 27, f"Esperado 27 TJs, encontrado {len(tjs)}: {tjs}"

    def test_6_trfs_presentes(self):
        trfs = [k for k in TRIBUNAIS if k.startswith("TRF")]
        assert sorted(trfs) == ["TRF1", "TRF2", "TRF3", "TRF4", "TRF5", "TRF6"]

    def test_24_trts_presentes(self):
        trts = [k for k in TRIBUNAIS if k.startswith("TRT")]
        assert len(trts) == 24

    def test_sem_duplicatas_de_codigo(self):
        codes = list(TRIBUNAIS.values())
        assert len(codes) == len(set(codes))


@pytest.mark.unit
class TestAssuntosAgro:
    def test_contem_assuntos_core_agrarios(self):
        """Garante que os 3 assuntos mais buscados no agro estão mapeados."""
        nomes = list(ASSUNTOS_AGRO.values())
        for nome_esperado in ("Usucapião", "Dano Ambiental", "Arrendamento Rural"):
            assert nome_esperado in nomes

    def test_codigos_sao_strings_de_digitos(self):
        for codigo in ASSUNTOS_AGRO:
            assert codigo.isdigit(), f"codigo {codigo!r} não é só dígitos"

    def test_tem_pelo_menos_10_assuntos(self):
        assert len(ASSUNTOS_AGRO) >= 10
