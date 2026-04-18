"""
Testes unit do service de jurisdição e cálculo de Reserva Legal.

Funções sob teste:
  app.services.jurisdicao.get_jurisdicao(uf)
  app.services.jurisdicao.get_all_jurisdicoes()
  app.services.jurisdicao.get_reserva_legal_info(uf, bioma=None)

Regras do Código Florestal (Lei 12.651/2012):
  - Imóvel em floresta amazônica (qualquer UF): 80%
  - Imóvel em Cerrado dentro da Amazônia Legal: 35%
  - Demais (Mata Atlântica, Caatinga, Pampa, Pantanal): 20%
  - Estados Amazônia Legal: AC, AM, AP, MA, MT, PA, RO, RR, TO
"""

from __future__ import annotations

import pytest

from app.services.jurisdicao import (
    get_all_jurisdicoes,
    get_jurisdicao,
    get_reserva_legal_info,
)


@pytest.mark.unit
class TestGetJurisdicao:
    def test_uf_existente_retorna_dict(self):
        result = get_jurisdicao("MA")
        assert result is not None
        assert isinstance(result, dict)

    def test_uf_em_minuscula_retorna_mesmo_que_maiuscula(self):
        ma_upper = get_jurisdicao("MA")
        ma_lower = get_jurisdicao("ma")
        assert ma_upper == ma_lower

    def test_uf_inexistente_retorna_none(self):
        assert get_jurisdicao("ZZ") is None
        assert get_jurisdicao("") is None

    def test_todas_27_ufs_presentes(self):
        all_ufs = get_all_jurisdicoes()
        assert len(all_ufs) == 27
        # Checa um sample espalhado por regiões
        for uf in ["AC", "MA", "MG", "RS", "SP", "DF", "BA"]:
            assert uf in all_ufs


@pytest.mark.unit
class TestReservaLegalInfo:
    # --- Amazônia Legal ---
    @pytest.mark.parametrize(
        "uf",
        ["AC", "AM", "AP", "MA", "MT", "PA", "RO", "RR", "TO"],
    )
    def test_amazonia_legal_sem_bioma_retorna_80_percent(self, uf):
        """UF da Amazônia Legal sem bioma específico assume 80% por default."""
        info = get_reserva_legal_info(uf)
        assert info["percentual"] == 80
        assert "Código Florestal" in info["fundamento"]
        assert "Amazônia Legal" in info["detalhes"]

    # --- Bioma sobrescreve UF ---
    def test_bioma_amazonia_sempre_80(self):
        """
        O matcher do código faz `"amazônia" in bioma.lower()`.
        "Amazônia" (com a final) bate; "Amazônica" (com ca final) NÃO.
        Documentamos o comportamento real — se quiser cobrir variantes,
        ver issue sessão 12.
        """
        info = get_reserva_legal_info("BA", bioma="Amazônia")
        assert info["percentual"] == 80

    def test_bioma_amazonica_variante_nao_matcha_comportamento_atual(self):
        """
        Limitação conhecida: 'Amazônica' (adjetivo) não bate com 'amazônia'
        substring. Fica 20%. Se isso for bug, abrir issue.
        """
        info = get_reserva_legal_info("BA", bioma="Floresta Amazônica")
        assert info["percentual"] == 20  # hoje bate na regra geral

    def test_cerrado_em_amazonia_legal_retorna_35(self):
        info = get_reserva_legal_info("MT", bioma="Cerrado")
        assert info["percentual"] == 35
        assert "Cerrado" in info["detalhes"]

    def test_cerrado_fora_amazonia_legal_retorna_20(self):
        """Cerrado em SP/MG (fora da AL) → regra geral 20%."""
        info = get_reserva_legal_info("GO", bioma="Cerrado")
        # GO não está na lista de AL do código — fica 20%
        assert info["percentual"] == 20

    # --- Não-AL, biomas comuns ---
    @pytest.mark.parametrize(
        "uf,bioma",
        [
            ("SP", "Mata Atlântica"),
            ("RS", "Pampa"),
            ("CE", "Caatinga"),
            ("MS", "Pantanal"),
            ("RJ", None),
        ],
    )
    def test_fora_amazonia_legal_retorna_20(self, uf, bioma):
        info = get_reserva_legal_info(uf, bioma=bioma)
        assert info["percentual"] == 20

    def test_case_insensitive_no_uf_e_bioma(self):
        info_lower = get_reserva_legal_info("mt", bioma="cerrado")
        info_upper = get_reserva_legal_info("MT", bioma="CERRADO")
        assert info_lower == info_upper

    # --- Estrutura do retorno ---
    def test_sempre_tem_3_chaves(self):
        info = get_reserva_legal_info("SP")
        assert set(info.keys()) == {"percentual", "fundamento", "detalhes"}

    def test_fundamento_sempre_cita_lei_12651(self):
        for uf in ["AC", "MT", "SP", "RS"]:
            info = get_reserva_legal_info(uf)
            assert "12.651" in info["fundamento"]
