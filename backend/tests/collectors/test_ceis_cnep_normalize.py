"""
Testes unit do normalizer de registros Portal da Transparência (CEIS/CNEP).

Função sob teste: `app.collectors.dados_gov_loaders._normalize_portal_record`

Objetivo: travar a regressão que fizemos quando o upstream mudou
`orgaoSancionador` para `fonteSancao` em ~abr/2026. Esses testes garantem
que o loader lê AMBOS os contratos (antigo + atual) e produz o mesmo shape
normalizado para o banco.
"""

from __future__ import annotations

from datetime import date

import pytest

from app.collectors.dados_gov_loaders import (
    _extrair_uf_de_endereco,
    _normalize_portal_record,
    _parse_br_date,
)


# ---------------------------------------------------------------------------
# Fixtures: JSONs sintéticos equivalentes aos que o Portal retorna
# ---------------------------------------------------------------------------


def record_contrato_antigo() -> dict:
    """Formato usado pelo Portal até ~mar/2026 (orgaoSancionador)."""
    return {
        "id": 42,
        "dataInicioSancao": "15/03/2025",
        "dataFimSancao": "15/03/2027",
        "tipoSancao": {"descricaoResumida": "Impedimento de licitar"},
        "orgaoSancionador": {"nome": "Tribunal de Contas da União", "siglaUf": "DF"},
        "sancionado": {"nome": "Empresa X Ltda", "codigoFormatado": "12.345.678/0001-90"},
        "pessoa": {
            "cnpjFormatado": "12.345.678/0001-90",
            "razaoSocialReceita": "EMPRESA X LTDA",
            "tipo": "CNPJ",
        },
        "fundamentacao": [
            {"descricao": "LEI 8666 ART 87"},
            {"descricao": "Lei 12.846"},
        ],
        "numeroProcesso": "TC-001/2025",
    }


def record_contrato_atual() -> dict:
    """Formato que o Portal retorna desde ~abr/2026 (fonteSancao)."""
    return {
        "id": 115267,
        "dataReferencia": "17/04/2026",
        "dataInicioSancao": "28/07/2017",
        "dataFimSancao": "Sem informação",
        "tipoSancao": {
            "descricaoResumida": "Declaração de Inidoneidade sem prazo determinado",
            "descricaoPortal": "Declaração de Inidoneidade sem prazo determinado",
        },
        "fonteSancao": {
            "nomeExibicao": "Secretaria Municipal de Gestão do Município de São Paulo - SP",
            "telefoneContato": "(11) 3396-7293",
            "enderecoContato": "Viaduto do Chá, nº 15 - Centro, São Paulo/SP",
        },
        "sancionado": {
            "nome": "INSTITUTO BEM VIVER",
            "codigoFormatado": "12.345.678/0001-90",
        },
        "pessoa": {
            "cnpjFormatado": "12.345.678/0001-90",
            "razaoSocialReceita": "INSTITUTO BEM VIVER",
            "tipo": "CNPJ",
        },
        "fundamentacao": [],
        "numeroProcesso": "2013-0.240.762-3",
    }


def record_pessoa_fisica() -> dict:
    """PF não tem cnpjFormatado — fallback pra codigoFormatado."""
    return {
        "id": 99,
        "dataInicioSancao": "01/01/2024",
        "dataFimSancao": "01/01/2026",
        "tipoSancao": {"descricaoResumida": "Improbidade"},
        "fonteSancao": {"nomeExibicao": "Min. Trabalho", "enderecoContato": "Brasília/DF"},
        "sancionado": {"nome": "João da Silva", "codigoFormatado": "123.456.789-00"},
        "pessoa": {"cpfFormatado": "123.456.789-00", "nome": "João da Silva", "tipo": "CPF"},
        "fundamentacao": [],
    }


def record_sem_cpf_cnpj() -> dict:
    """Quando doc vem zerado, normalizer retorna None (filtra lixo)."""
    return {
        "id": 1,
        "dataInicioSancao": "01/01/2024",
        "tipoSancao": {"descricaoResumida": "X"},
        "fonteSancao": {"nomeExibicao": "Órgão"},
        "sancionado": {"nome": "Sem doc", "codigoFormatado": ""},
        "pessoa": {},
    }


# ---------------------------------------------------------------------------
# _normalize_portal_record
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestNormalizePortalRecord:
    def test_contrato_antigo_mapeia_orgao_sancionador(self):
        n = _normalize_portal_record(record_contrato_antigo())
        assert n is not None
        assert n["orgao_sancionador"] == "Tribunal de Contas da União"
        assert n["uf_orgao"] == "DF"

    def test_contrato_atual_mapeia_fonte_sancao(self):
        """
        REGRESSÃO: antes do fix o contrato atual voltava orgao_sancionador=''
        porque o loader lia apenas `orgaoSancionador.nome`.
        """
        n = _normalize_portal_record(record_contrato_atual())
        assert n is not None
        assert n["orgao_sancionador"] == (
            "Secretaria Municipal de Gestão do Município de São Paulo - SP"
        )
        assert n["uf_orgao"] == "SP"  # extraído do endereço "São Paulo/SP"

    def test_campos_comuns_entre_os_dois_contratos(self):
        for record, esperado_doc in [
            (record_contrato_antigo(), "12345678000190"),
            (record_contrato_atual(), "12345678000190"),
        ]:
            n = _normalize_portal_record(record)
            assert n is not None
            assert n["cpf_cnpj"] == esperado_doc
            assert n["tipo_pessoa"] == "PJ"
            assert n["tipo_sancao"]
            assert n["data_inicio_sancao"] is not None

    def test_data_fim_sem_informacao_vira_none(self):
        n = _normalize_portal_record(record_contrato_atual())
        assert n is not None
        assert n["data_fim_sancao"] is None

    def test_pessoa_fisica_usa_cpf_e_marca_pf(self):
        n = _normalize_portal_record(record_pessoa_fisica())
        assert n is not None
        assert n["cpf_cnpj"] == "12345678900"
        assert n["tipo_pessoa"] == "PF"
        assert n["nome"] == "João da Silva"

    def test_registro_sem_documento_retorna_none(self):
        assert _normalize_portal_record(record_sem_cpf_cnpj()) is None

    def test_documento_todo_zeros_retorna_none(self):
        rec = record_contrato_atual()
        rec["pessoa"]["cnpjFormatado"] = "00.000.000/0000-00"
        rec["sancionado"]["codigoFormatado"] = ""
        assert _normalize_portal_record(rec) is None

    def test_fundamentacao_concatenada_com_limite(self):
        n = _normalize_portal_record(record_contrato_antigo())
        assert n is not None
        assert "LEI 8666" in n["fundamentacao"]
        assert "Lei 12.846" in n["fundamentacao"]
        assert "; " in n["fundamentacao"]
        assert len(n["fundamentacao"]) <= 2000

    def test_raw_data_preservado_para_debug(self):
        rec = record_contrato_atual()
        n = _normalize_portal_record(rec)
        assert n is not None
        assert n["raw_data"] is rec

    def test_processo_limitado_a_100_chars(self):
        rec = record_contrato_atual()
        rec["numeroProcesso"] = "X" * 500
        n = _normalize_portal_record(rec)
        assert n is not None
        assert len(n["processo"]) == 100


# ---------------------------------------------------------------------------
# _parse_br_date
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseBrDate:
    def test_formato_br_valido(self):
        assert _parse_br_date("15/03/2025") == date(2025, 3, 15)

    def test_none_retorna_none(self):
        assert _parse_br_date(None) is None

    def test_vazio_retorna_none(self):
        assert _parse_br_date("") is None

    def test_sem_informacao_retorna_none(self):
        assert _parse_br_date("Sem informação") is None
        assert _parse_br_date("sem informacao") is None

    def test_formato_invalido_retorna_none(self):
        assert _parse_br_date("2025-03-15") is None
        assert _parse_br_date("15-03-2025") is None
        assert _parse_br_date("lorem ipsum") is None

    def test_trim_whitespace(self):
        assert _parse_br_date("  15/03/2025  ") == date(2025, 3, 15)


# ---------------------------------------------------------------------------
# _extrair_uf_de_endereco
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestExtrairUfDeEndereco:
    @pytest.mark.parametrize(
        "endereco,esperado",
        [
            ("Viaduto do Chá, nº 15 - Centro, São Paulo/SP", "SP"),
            ("Rua X, 1 - Centro, Rio de Janeiro/RJ", "RJ"),
            ("Av Y, 100, Brasília/DF", "DF"),
            ("", ""),
            ("Sem UF nesse endereço", ""),
            ("Cidade sem barra SP", ""),  # precisa do /XX
        ],
    )
    def test_extracao(self, endereco, esperado):
        assert _extrair_uf_de_endereco(endereco) == esperado
