"""
Contract test do Portal da Transparência (CGU) — CEIS e CNEP.

Roda em 2 modos:
  - @pytest.mark.contract (default no CI): replay de cassette VCR
  - @pytest.mark.live (opt-in na auditoria): bate API real

O cassette é gravado uma vez com `VCR_RECORD_MODE=once pytest ...` e fica
versionado. Quando o upstream muda o contrato, o teste quebra — aí a gente
atualiza o cassette com intenção.

Token é filtrado pelo vcr_config (conftest) — nunca vai pro cassette.

IMPORTANTE (abr/2026): contract test pegou que o Portal mudou `orgaoSancionador`
para `fonteSancao`. O loader em app/collectors/dados_gov_loaders.py:602 ainda
lê do campo antigo — ver TODO no CHANGELOG 0.13.2.
"""

from __future__ import annotations

import os

import pytest

from app.collectors.portal_transparencia import PortalTransparenciaClient


def _client() -> PortalTransparenciaClient:
    """Helper: constrói cliente usando token do env (VCR filtra no cassette)."""
    return PortalTransparenciaClient(
        token=os.environ.get("PORTAL_TRANSPARENCIA_TOKEN", "filtered-by-vcr"),
    )


# Campos que o backend depende em pelo menos 1 lugar da camada de domínio.
# Quando esta lista quebra, algo na camada acima quebra também.
CEIS_CAMPOS_ESPERADOS = {
    "id",
    "dataInicioSancao",
    "dataFimSancao",
    "fonteSancao",   # ex-orgaoSancionador (upstream mudou ~abr/2026)
    "tipoSancao",
}

CNEP_CAMPOS_ESPERADOS = {
    "id",
    "dataInicioSancao",
    "dataFimSancao",
    "fonteSancao",
    "tipoSancao",
}


# ---------------------------------------------------------------------------
# CEIS
# ---------------------------------------------------------------------------


@pytest.mark.contract
@pytest.mark.vcr(filter_headers=["chave-api-dados"])
class TestPortalTransparenciaCEIS:
    def test_ceis_primeira_pagina_retorna_lista(self):
        pages = list(_client().iter_pages("/ceis", max_pages=1))
        assert len(pages) >= 1, "deveria retornar ao menos 1 página"
        first = pages[0]
        assert isinstance(first, list)
        assert len(first) > 0, "primeira página não deveria vir vazia"

    def test_ceis_schema_dos_registros(self):
        pages = list(_client().iter_pages("/ceis", max_pages=1))
        first_row = pages[0][0]
        for campo in CEIS_CAMPOS_ESPERADOS:
            assert campo in first_row, (
                f"campo esperado '{campo}' ausente no CEIS. "
                f"Upstream mudou contrato? Campos recebidos: {list(first_row.keys())}"
            )

    def test_ceis_tipo_sancao_tem_descricao_resumida(self):
        """O loader lê `tipoSancao.descricaoResumida` — dados_gov_loaders.py:601."""
        pages = list(_client().iter_pages("/ceis", max_pages=1))
        first_row = pages[0][0]
        tipo = first_row.get("tipoSancao", {})
        assert "descricaoResumida" in tipo, (
            f"tipoSancao sem descricaoResumida — upstream mudou? {list(tipo.keys())}"
        )

    def test_ceis_fonte_sancao_tem_nome_exibicao(self):
        """
        Contrato atual: `fonteSancao.nomeExibicao`. Antes era
        `orgaoSancionador.nome`. O loader em dados_gov_loaders.py:602 ainda
        lê do nome antigo — precisa reparar.
        """
        pages = list(_client().iter_pages("/ceis", max_pages=1))
        first_row = pages[0][0]
        fonte = first_row.get("fonteSancao", {})
        assert "nomeExibicao" in fonte, (
            f"fonteSancao sem nomeExibicao — upstream mudou de novo? {list(fonte.keys())}"
        )


# ---------------------------------------------------------------------------
# CNEP
# ---------------------------------------------------------------------------


@pytest.mark.contract
@pytest.mark.vcr(filter_headers=["chave-api-dados"])
class TestPortalTransparenciaCNEP:
    def test_cnep_primeira_pagina_retorna_lista(self):
        pages = list(_client().iter_pages("/cnep", max_pages=1))
        assert len(pages) >= 1
        assert isinstance(pages[0], list)
        assert len(pages[0]) > 0

    def test_cnep_schema_dos_registros(self):
        pages = list(_client().iter_pages("/cnep", max_pages=1))
        first_row = pages[0][0]
        for campo in CNEP_CAMPOS_ESPERADOS:
            assert campo in first_row, (
                f"campo '{campo}' ausente no CNEP. Upstream mudou? {list(first_row.keys())}"
            )

    def test_cnep_tipo_sancao_tem_descricao_resumida(self):
        pages = list(_client().iter_pages("/cnep", max_pages=1))
        first_row = pages[0][0]
        tipo = first_row.get("tipoSancao", {})
        assert "descricaoResumida" in tipo


# ---------------------------------------------------------------------------
# Erros controlados — unit, sem VCR
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPortalTransparenciaClientErros:
    def test_sem_token_levanta_erro(self, monkeypatch):
        from app.config import settings

        monkeypatch.setattr(settings, "portal_transparencia_token", "")
        with pytest.raises(RuntimeError, match="PORTAL_TRANSPARENCIA_TOKEN"):
            PortalTransparenciaClient()

    def test_token_explicito_sobrepoe_settings(self, monkeypatch):
        from app.config import settings

        monkeypatch.setattr(settings, "portal_transparencia_token", "")
        client = PortalTransparenciaClient(token="explicit-token")
        assert client.token == "explicit-token"
        assert client.headers["chave-api-dados"] == "explicit-token"

    def test_headers_contem_user_agent_agrojus(self):
        client = PortalTransparenciaClient(token="t")
        assert "AgroJus" in client.headers["User-Agent"]


# ---------------------------------------------------------------------------
# Live — opt-in (roda com PYTEST_LIVE=1, usado na auditoria semanal)
# ---------------------------------------------------------------------------


@pytest.mark.live
class TestPortalTransparenciaLive:
    """
    Health check real do upstream. Só roda quando PYTEST_LIVE=1.
    Requer PORTAL_TRANSPARENCIA_TOKEN válido no ambiente.
    """

    def test_upstream_acessivel_e_ceis_retorna_dados(self):
        token = os.environ.get("PORTAL_TRANSPARENCIA_TOKEN")
        if not token:
            pytest.skip("PORTAL_TRANSPARENCIA_TOKEN não configurado")
        client = PortalTransparenciaClient(token=token)
        pages = list(client.iter_pages("/ceis", max_pages=1))
        assert pages, "upstream CEIS retornou vazio — investigar"
        assert len(pages[0]) > 0

    def test_upstream_acessivel_e_cnep_retorna_dados(self):
        token = os.environ.get("PORTAL_TRANSPARENCIA_TOKEN")
        if not token:
            pytest.skip("PORTAL_TRANSPARENCIA_TOKEN não configurado")
        client = PortalTransparenciaClient(token=token)
        pages = list(client.iter_pages("/cnep", max_pages=1))
        assert pages, "upstream CNEP retornou vazio — investigar"
        assert len(pages[0]) > 0
