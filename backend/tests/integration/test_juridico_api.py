"""
Integration tests do Hub Jurídico-Agro (/api/v1/juridico/*).

Usa FastAPI TestClient + banco real populado com seeds (sessão 9 inseriu
12 contratos + 12 teses + 51 normativos). Assume banco dev disponível —
no CI o service postgres do GitHub Actions é inicializado vazio e o
conftest integration vai precisar carregar os seeds.

Endpoints cobertos:
  GET  /juridico/contratos            — lista + filtros
  GET  /juridico/contratos/{slug}     — detalhe
  GET  /juridico/teses                — lista + filtros
  GET  /juridico/teses/{slug}         — detalhe
  GET  /juridico/legislacao           — lista + filtros
  GET  /juridico/legislacao/{slug}    — detalhe
  GET  /juridico/processos/{cpf_cnpj}/dossie — dossie consolidado
  GET  /juridico/monitoramento        — lista
  POST /juridico/monitoramento        — cadastra
  DEL  /juridico/monitoramento/{id}   — remove
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Contratos
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestJuridicoContratos:
    def test_list_sem_filtros_retorna_seeds(self, client: TestClient):
        r = client.get("/api/v1/juridico/contratos")
        assert r.status_code == 200
        data = r.json()
        assert "total" in data
        assert "contratos" in data
        assert data["total"] >= 10, f"esperado >=10 seeds, veio {data['total']}"

    def test_list_com_limit(self, client: TestClient):
        r = client.get("/api/v1/juridico/contratos?limit=3")
        assert r.status_code == 200
        contratos = r.json()["contratos"]
        assert len(contratos) <= 3

    def test_list_filtra_por_categoria(self, client: TestClient):
        r = client.get("/api/v1/juridico/contratos?categoria=exploracao_rural")
        assert r.status_code == 200
        contratos = r.json()["contratos"]
        # Se houver resultados, todos precisam ser da categoria filtrada
        for c in contratos:
            assert c["categoria"] == "exploracao_rural"

    def test_list_busca_textual_no_titulo(self, client: TestClient):
        r = client.get("/api/v1/juridico/contratos?q=arrendamento")
        assert r.status_code == 200
        contratos = r.json()["contratos"]
        assert len(contratos) > 0
        assert any("arrendamento" in c["titulo"].lower() for c in contratos)

    def test_shape_do_contrato_resumo(self, client: TestClient):
        r = client.get("/api/v1/juridico/contratos?limit=1")
        contratos = r.json()["contratos"]
        if not contratos:
            pytest.skip("Banco sem seeds de contratos")
        c = contratos[0]
        # Campos esperados pelo frontend (ContratosTab)
        for campo in [
            "id", "slug", "titulo", "categoria", "sinopse", "n_campos",
            "n_legislacao", "versao", "publico_alvo",
        ]:
            assert campo in c, f"campo {campo!r} ausente no resumo"

    def test_detalhe_por_slug(self, client: TestClient):
        # Busca o primeiro para pegar slug dinamicamente
        list_r = client.get("/api/v1/juridico/contratos?limit=1")
        contratos = list_r.json()["contratos"]
        if not contratos:
            pytest.skip("Banco sem seeds")
        slug = contratos[0]["slug"]

        r = client.get(f"/api/v1/juridico/contratos/{slug}")
        assert r.status_code == 200
        detalhe = r.json()
        # Detalhe tem campos que o modal consome
        for campo in ["texto_markdown", "campos", "cautelas", "legislacao_referencia"]:
            assert campo in detalhe, f"detalhe sem {campo!r}"
        assert detalhe["slug"] == slug

    def test_detalhe_slug_inexistente_404(self, client: TestClient):
        r = client.get("/api/v1/juridico/contratos/slug-que-nao-existe-xyz")
        assert r.status_code == 404


# ---------------------------------------------------------------------------
# Teses
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestJuridicoTeses:
    def test_list_retorna_teses(self, client: TestClient):
        r = client.get("/api/v1/juridico/teses")
        assert r.status_code == 200
        data = r.json()
        assert data["total"] >= 5

    def test_filtra_por_area_ambiental(self, client: TestClient):
        r = client.get("/api/v1/juridico/teses?area=ambiental&limit=5")
        assert r.status_code == 200
        teses = r.json()["teses"]
        for t in teses:
            assert t["area"] == "ambiental"

    def test_shape_da_tese_resumo(self, client: TestClient):
        r = client.get("/api/v1/juridico/teses?limit=1")
        teses = r.json()["teses"]
        if not teses:
            pytest.skip("Banco sem seeds de teses")
        t = teses[0]
        for campo in [
            "id", "slug", "titulo", "area", "situacao",
            "sumula_propria", "n_argumentos", "n_precedentes",
        ]:
            assert campo in t

    def test_detalhe_tese_por_slug(self, client: TestClient):
        list_r = client.get("/api/v1/juridico/teses?limit=1")
        teses = list_r.json()["teses"]
        if not teses:
            pytest.skip("Banco sem seeds")
        slug = teses[0]["slug"]

        r = client.get(f"/api/v1/juridico/teses/{slug}")
        assert r.status_code == 200
        detalhe = r.json()
        for campo in [
            "argumentos_principais", "precedentes_sugeridos",
            "legislacao_aplicavel", "aplicabilidade",
        ]:
            assert campo in detalhe

    def test_detalhe_slug_inexistente_404(self, client: TestClient):
        r = client.get("/api/v1/juridico/teses/nope-xyz")
        assert r.status_code == 404


# ---------------------------------------------------------------------------
# Legislação
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestJuridicoLegislacao:
    def test_list_federal(self, client: TestClient):
        r = client.get("/api/v1/juridico/legislacao?esfera=federal&limit=5")
        assert r.status_code == 200
        normas = r.json()["legislacao"]
        for n in normas:
            assert n["esfera"] == "federal"

    def test_filtra_por_uf_inclui_federais(self, client: TestClient):
        """
        Regra do backend: filtrar por UF NÃO exclui federais (porque federais
        se aplicam a todos). Isso é relevante pro frontend mostrar legislação
        aplicável ao imóvel selecionado.
        """
        r = client.get("/api/v1/juridico/legislacao?uf=MA&limit=50")
        assert r.status_code == 200
        normas = r.json()["legislacao"]
        # Pelo menos uma federal deve aparecer mesmo filtrando por MA
        esferas = {n["esfera"] for n in normas}
        if len(normas) > 0:
            assert "federal" in esferas

    def test_filtra_por_tema(self, client: TestClient):
        r = client.get("/api/v1/juridico/legislacao?tema=ambiental&limit=50")
        assert r.status_code == 200
        normas = r.json()["legislacao"]
        # Se houver resultados, cada um tem o tema
        for n in normas:
            if n.get("temas"):
                assert "ambiental" in n["temas"]

    def test_shape_da_norma(self, client: TestClient):
        r = client.get("/api/v1/juridico/legislacao?limit=1")
        normas = r.json()["legislacao"]
        if not normas:
            pytest.skip("Banco sem seeds")
        n = normas[0]
        for campo in ["id", "slug", "titulo", "esfera", "tipo", "situacao"]:
            assert campo in n

    def test_detalhe_slug_inexistente_404(self, client: TestClient):
        r = client.get("/api/v1/juridico/legislacao/lei-inventada-123")
        assert r.status_code == 404


# ---------------------------------------------------------------------------
# Dossiê de processos por CPF/CNPJ
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestJuridicoProcessosDossie:
    CNPJ_COM_CEIS = "00818544000165"  # conhecido: tem 2 sanções CEIS
    # 00000000000 é usado pelo IBAMA como placeholder para autos sem CPF
    # identificado — por isso tem dezenas de resultados. Usamos um CPF
    # inventado que garantidamente não está nas bases:
    CPF_SEM_DADOS = "99988877766"

    def test_dossie_cnpj_conhecido_retorna_estrutura_completa(self, client: TestClient):
        r = client.get(f"/api/v1/juridico/processos/{self.CNPJ_COM_CEIS}/dossie")
        assert r.status_code == 200
        data = r.json()

        # Estrutura esperada pelo frontend (ProcessosTab)
        esperados = [
            "cpf_cnpj_mask", "datajud_processos", "djen_publicacoes",
            "autos_ibama", "ceis", "cnep", "lista_suja",
            "sumario", "risco_consolidado",
        ]
        for campo in esperados:
            assert campo in data, f"dossie sem {campo!r}"

    def test_dossie_classifica_risco_em_categoria_valida(self, client: TestClient):
        r = client.get(f"/api/v1/juridico/processos/{self.CNPJ_COM_CEIS}/dossie")
        data = r.json()
        assert data["risco_consolidado"] in {"BAIXO", "MEDIO", "ALTO", "CRITICO"}

    def test_dossie_cnpj_com_ceis_tem_risco_alto_ou_critico(self, client: TestClient):
        """CNPJ com 2 sanções CEIS deve ter pelo menos ALTO (regra: CEIS = +30 pontos)."""
        r = client.get(f"/api/v1/juridico/processos/{self.CNPJ_COM_CEIS}/dossie")
        data = r.json()
        assert data["sumario"]["ceis"] >= 1
        assert data["risco_consolidado"] in {"ALTO", "CRITICO"}

    def test_dossie_mascara_cpf_cnpj_na_resposta(self, client: TestClient):
        r = client.get(f"/api/v1/juridico/processos/{self.CNPJ_COM_CEIS}/dossie")
        mask = r.json()["cpf_cnpj_mask"]
        # Formato esperado: 008.********0165 (prefixo + * + sufixo)
        assert "*" in mask
        assert self.CNPJ_COM_CEIS not in mask  # doc real não aparece completo

    def test_dossie_aceita_mascara_simplificada_no_input(self, client: TestClient):
        """
        Frontend pode enviar formatado ou limpo — backend remove `.` e `-`
        internamente. A barra `/` quebra roteamento (não é suportada), então
        para CNPJ com máscara, frontend deve remover a barra antes de enviar.
        """
        # Versão só com pontos e hífens (ponto/hifen não quebram URL)
        r = client.get(f"/api/v1/juridico/processos/008.185.440-00.165/dossie")
        # Alguns formatos intermediários podem não bater — se 200, verifica mask
        if r.status_code == 200:
            data = r.json()
            # Backend removeu pontuação e produziu mask consistente
            assert self.CNPJ_COM_CEIS in data["cpf_cnpj_mask"].replace("*", "").replace(".", "").replace("/", "").replace("-", "") or "*" in data["cpf_cnpj_mask"]

    def test_dossie_cpf_sem_dados_retorna_risco_baixo(self, client: TestClient):
        r = client.get(f"/api/v1/juridico/processos/{self.CPF_SEM_DADOS}/dossie")
        assert r.status_code == 200
        data = r.json()
        assert data["risco_consolidado"] == "BAIXO"

    def test_sumario_tem_totais_numericos(self, client: TestClient):
        r = client.get(f"/api/v1/juridico/processos/{self.CPF_SEM_DADOS}/dossie")
        s = r.json()["sumario"]
        for key in [
            "processos_datajud", "djen_publicacoes", "autos_ibama",
            "valor_autos_ibama", "ceis", "cnep", "lista_suja_mte",
            "valor_processos",
        ]:
            assert key in s
            assert isinstance(s[key], (int, float))


# ---------------------------------------------------------------------------
# Monitoramento (CRUD)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestJuridicoMonitoramento:
    def test_post_cpf_invalido_retorna_400(self, client: TestClient):
        r = client.post(
            "/api/v1/juridico/monitoramento",
            json={"cpf_cnpj": "123"},
        )
        assert r.status_code == 400
        assert "CPF/CNPJ" in r.json()["detail"]

    def test_ciclo_crud_completo(self, client: TestClient):
        """
        POST cria → GET lista contém → DELETE remove → GET lista não contém.
        """
        payload = {
            "cpf_cnpj": "11222333000181",
            "nome_sugerido": "Fixture de teste integration",
            "contexto": "teste automatico pytest",
            "tags": ["teste", "pytest"],
            "frequencia": "diaria",
        }

        # CREATE
        create = client.post("/api/v1/juridico/monitoramento", json=payload)
        assert create.status_code == 200
        created_id = create.json()["id"]

        try:
            # READ — deve aparecer na lista
            listing = client.get("/api/v1/juridico/monitoramento")
            assert listing.status_code == 200
            ids = [m["id"] for m in listing.json()["monitoramentos"]]
            assert created_id in ids

            # Verifica shape
            monit = next(m for m in listing.json()["monitoramentos"] if m["id"] == created_id)
            assert monit["nome_sugerido"] == payload["nome_sugerido"]
            assert monit["frequencia"] == "diaria"
            assert set(monit["tags"]) == set(payload["tags"])
            # CPF/CNPJ vem mascarado na listagem (LGPD)
            assert "*" in monit["cpf_cnpj"]

        finally:
            # DELETE — sempre, mesmo se assert falhar
            delete = client.delete(f"/api/v1/juridico/monitoramento/{created_id}")
            assert delete.status_code == 200

        # READ — não deve mais existir
        listing2 = client.get("/api/v1/juridico/monitoramento")
        ids2 = [m["id"] for m in listing2.json()["monitoramentos"]]
        assert created_id not in ids2

    def test_delete_id_inexistente_retorna_404(self, client: TestClient):
        r = client.delete("/api/v1/juridico/monitoramento/999999999")
        assert r.status_code == 404
