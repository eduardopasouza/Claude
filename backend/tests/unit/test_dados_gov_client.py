"""
Testes unit de lógica pura do DadosGovClient.

Foco em:
  - `_fallback_pkg` — resiliência quando CKAN cai
  - `pick_resource` — algoritmo de scoring para escolher CSV/SHP/ZIP
  - KNOWN_RESOURCES — estrutura do fallback

Não testa download nem package_show (são contract — ver testes com VCR).
"""

from __future__ import annotations

import pytest

from app.collectors.dados_gov import KNOWN_RESOURCES, DadosGovClient


# ---------------------------------------------------------------------------
# KNOWN_RESOURCES — garante que o fallback está decente
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestKnownResources:
    def test_known_resources_nao_vazio(self):
        assert len(KNOWN_RESOURCES) > 0

    def test_cada_package_id_e_string_nao_vazia(self):
        for package_id in KNOWN_RESOURCES:
            assert isinstance(package_id, str)
            assert len(package_id) > 0

    def test_cada_resource_tem_url_ou_esta_vazio(self):
        for package_id, resources in KNOWN_RESOURCES.items():
            for r in resources:
                assert "url" in r, f"{package_id}: resource sem url: {r}"
                assert r["url"].startswith(("http://", "https://"))


# ---------------------------------------------------------------------------
# _fallback_pkg — comportamento quando CKAN indisponível
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestFallbackPkg:
    def test_fallback_para_package_conhecido_retorna_resources(self):
        # Escolhe qualquer package_id de KNOWN_RESOURCES com pelo menos 1 recurso
        pid_com_resources = next(
            pid for pid, r in KNOWN_RESOURCES.items() if len(r) > 0
        )
        client = DadosGovClient(token="")
        pkg = client._fallback_pkg(pid_com_resources, "teste")
        assert pkg["id"] == pid_com_resources
        assert pkg["name"] == pid_com_resources
        assert pkg["_fallback"] is True
        assert pkg["_fallback_reason"] == "teste"
        assert len(pkg["resources"]) > 0

    def test_fallback_para_package_desconhecido_levanta_erro(self):
        client = DadosGovClient(token="")
        with pytest.raises(RuntimeError, match="KNOWN_RESOURCES"):
            client._fallback_pkg("package-inexistente-no-map", "teste")

    def test_fallback_marca_flag_para_detectar_no_caller(self):
        pid_com_resources = next(
            pid for pid, r in KNOWN_RESOURCES.items() if len(r) > 0
        )
        client = DadosGovClient(token="")
        pkg = client._fallback_pkg(pid_com_resources, "401 Unauthorized")
        # Caller pode diferenciar fallback de resposta real olhando essa flag
        assert pkg.get("_fallback") is True


# ---------------------------------------------------------------------------
# pick_resource — algoritmo de scoring
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPickResource:
    def test_package_sem_resources_retorna_none(self):
        assert DadosGovClient.pick_resource({}) is None
        assert DadosGovClient.pick_resource({"resources": []}) is None

    def test_package_com_1_resource_sem_hints_retorna_ele(self):
        pkg = {"resources": [{"url": "http://a.com/x.csv", "format": "CSV"}]}
        r = DadosGovClient.pick_resource(pkg)
        assert r is not None
        assert r["url"] == "http://a.com/x.csv"

    def test_format_hint_prioriza_formato_certo(self):
        pkg = {
            "resources": [
                {"url": "http://a.com/x.pdf", "format": "PDF"},
                {"url": "http://a.com/x.csv", "format": "CSV"},
                {"url": "http://a.com/x.shp", "format": "SHP"},
            ],
        }
        r = DadosGovClient.pick_resource(pkg, format_hint="SHP")
        assert r["format"] == "SHP"

    def test_format_hint_aceita_case_insensitive(self):
        pkg = {
            "resources": [
                {"url": "http://a.com/x.csv", "format": "CSV"},
                {"url": "http://a.com/x.shp", "format": "shp"},  # lowercase
            ],
        }
        r = DadosGovClient.pick_resource(pkg, format_hint="shp")
        assert r["format"].upper() == "SHP"

    def test_name_hint_pontua_por_token_match(self):
        pkg = {
            "resources": [
                {"url": "http://a.com/x.csv", "format": "CSV", "name": "nacional geral"},
                {"url": "http://a.com/y.csv", "format": "CSV", "name": "estadual MA especifico"},
            ],
        }
        r = DadosGovClient.pick_resource(pkg, name_hint="estadual MA")
        assert r["name"] == "estadual MA especifico"

    def test_format_e_name_hint_combinados(self):
        """SHP + nome bate — SHP ganha por formato + CSV bate por nome."""
        pkg = {
            "resources": [
                {"url": "http://a.com/a.csv", "format": "CSV", "name": "nacional"},
                {"url": "http://a.com/b.shp", "format": "SHP", "name": "nacional"},
            ],
        }
        r = DadosGovClient.pick_resource(pkg, format_hint="SHP", name_hint="nacional")
        # SHP (+10) + name match (+3) + url (+1) = 14 vence CSV (+3 name + 1 url = 4)
        assert r["format"] == "SHP"

    def test_resource_sem_url_nao_ganha_pontos_de_url(self):
        pkg = {
            "resources": [
                {"format": "CSV"},  # sem URL
                {"format": "CSV", "url": "http://a.com/x"},
            ],
        }
        r = DadosGovClient.pick_resource(pkg, format_hint="CSV")
        # O que tem URL ganha
        assert r.get("url") == "http://a.com/x"

    def test_ordem_do_resources_nao_altera_escolha_com_hint(self):
        pkg_a = {
            "resources": [
                {"url": "http://a.com/x.pdf", "format": "PDF"},
                {"url": "http://a.com/x.csv", "format": "CSV"},
            ],
        }
        pkg_b = {
            "resources": [
                {"url": "http://a.com/x.csv", "format": "CSV"},
                {"url": "http://a.com/x.pdf", "format": "PDF"},
            ],
        }
        assert (
            DadosGovClient.pick_resource(pkg_a, format_hint="CSV")["format"]
            == DadosGovClient.pick_resource(pkg_b, format_hint="CSV")["format"]
            == "CSV"
        )


# ---------------------------------------------------------------------------
# Headers / construção
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDadosGovClientInit:
    def test_user_agent_sempre_presente(self):
        client = DadosGovClient(token="")
        assert "User-Agent" in client.headers
        assert "AgroJus" in client.headers["User-Agent"]

    def test_authorization_header_so_quando_token_setado(self):
        sem_token = DadosGovClient(token="")
        com_token = DadosGovClient(token="abc123")
        assert "Authorization" not in sem_token.headers
        assert com_token.headers.get("Authorization") == "Bearer abc123"

    def test_timeout_default_60s(self):
        client = DadosGovClient(token="")
        assert client.timeout == 60

    def test_timeout_customizavel(self):
        client = DadosGovClient(token="", timeout=120)
        assert client.timeout == 120
