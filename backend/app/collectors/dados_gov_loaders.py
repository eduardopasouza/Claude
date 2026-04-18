"""
Loaders do Sprint 4 — 10 datasets do dados.gov.br + 2 do Portal Transparência.

Cada loader:
  1. Usa DadosGovClient / PortalTransparenciaClient para baixar o recurso
  2. Descomprime (se for .zip de shapefile) via /tmp
  3. Lê com geopandas (shapefile) ou pandas (CSV)
  4. Normaliza colunas e persiste na tabela correspondente
  5. Registra em `dados_gov_ingest_log`

Todos são idempotentes: TRUNCATE + INSERT a cada rodada (a frequência típica
é mensal via cron).

O script master `backend/scripts/run_dados_gov_etl.py` invoca-os em sequência.
"""

from __future__ import annotations

import io
import logging
import os
import tempfile
import zipfile
from datetime import datetime, timezone
from typing import Callable, Optional

from app.collectors.dados_gov import DadosGovClient
from app.collectors.portal_transparencia import PortalTransparenciaClient
from app.models.database import (
    SigmineProcesso, AnaOutorga, AnaBho,
    IncraAssentamento, IncraQuilombola,
    AneelUsina, AneelLinhaTransmissao,
    GarantiaSafraBeneficiario,
    CeisRegistro, CnepRegistro,
    IbamaEmbargo, IbamaCtf, IbamaAutoInfracao,
    DadosGovIngestLog,
    get_engine, get_session,
)

logger = logging.getLogger("agrojus.dados_gov.loaders")


# ==========================================================================
# Helpers
# ==========================================================================


def _truncate(table_name: str) -> None:
    """Limpa uma tabela."""
    engine = get_engine()
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
        conn.commit()


def _clean_for_json(d: dict) -> dict:
    """Remove NaN/Infinity/tipos incompatíveis com JSON pra evitar erro no Postgres."""
    import math
    out = {}
    for k, v in d.items():
        if v is None:
            out[k] = None
        elif isinstance(v, float):
            if math.isnan(v) or math.isinf(v):
                out[k] = None
            else:
                out[k] = v
        elif isinstance(v, str) and v.lower() == "nan":
            out[k] = None
        else:
            out[k] = v
    return out


def _log_ingest(loader: str, dataset_id: str, url: str, started, finished, status, fetched, persisted, error=None):
    session = get_session()
    try:
        log = DadosGovIngestLog(
            loader=loader, dataset_id=dataset_id, resource_url=url,
            started_at=started, finished_at=finished, status=status,
            rows_fetched=fetched, rows_persisted=persisted, error=error,
        )
        session.add(log)
        session.commit()
    finally:
        session.close()


def _extract_shapefile(content: bytes, hint_name: Optional[str] = None) -> Optional[str]:
    """Escreve shapefile em tempdir e retorna caminho .shp principal."""
    tmpdir = tempfile.mkdtemp(prefix="agrojus_dadosgov_")
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            z.extractall(tmpdir)
    except zipfile.BadZipFile:
        # Talvez seja o .shp direto (não compactado)
        if hint_name:
            path = os.path.join(tmpdir, hint_name)
            with open(path, "wb") as f:
                f.write(content)
            return path
        return None

    # Encontra o .shp principal
    for root, _, files in os.walk(tmpdir):
        for f in files:
            if f.lower().endswith(".shp"):
                return os.path.join(root, f)
    return None


def _run_loader(
    loader_name: str,
    dataset_id: str,
    fn: Callable[[], tuple[int, int, str]],
) -> dict:
    """Wrapper comum: roda o loader e grava log."""
    started = datetime.now(timezone.utc)
    try:
        fetched, persisted, url = fn()
        finished = datetime.now(timezone.utc)
        _log_ingest(loader_name, dataset_id, url, started, finished, "success", fetched, persisted)
        return {"loader": loader_name, "fetched": fetched, "persisted": persisted, "status": "success"}
    except Exception as e:  # noqa: BLE001
        finished = datetime.now(timezone.utc)
        logger.exception("loader %s falhou", loader_name)
        _log_ingest(loader_name, dataset_id, "", started, finished, "failed", 0, 0, error=str(e))
        return {"loader": loader_name, "fetched": 0, "persisted": 0, "status": "failed", "error": str(e)[:400]}


# ==========================================================================
# Shapefile loader genérico (via geopandas)
# ==========================================================================


def _load_shapefile_to_table(
    shp_path: str,
    model_class,
    table_name: str,
    column_map: dict[str, str],
    *,
    truncate: bool = True,
    batch_size: int = 500,
) -> int:
    """Carrega shapefile em tabela mapeando colunas.

    column_map: {nome_coluna_shp: nome_atributo_modelo}. 'geometry' sempre.
    """
    import geopandas as gpd

    gdf = gpd.read_file(shp_path)
    if gdf.empty:
        return 0
    # Normaliza CRS para WGS84
    try:
        if gdf.crs and gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs(epsg=4326)
    except Exception:
        pass

    if truncate:
        _truncate(table_name)

    session = get_session()
    total = 0
    try:
        batch: list = []
        for _, row in gdf.iterrows():
            kwargs = {}
            for shp_col, attr in column_map.items():
                if shp_col in row:
                    v = row[shp_col]
                    if v is not None and str(v).lower() != "nan":
                        kwargs[attr] = v
            if row.geometry is not None and not row.geometry.is_empty:
                from shapely.geometry import MultiPolygon, MultiLineString, Polygon, LineString
                geom = row.geometry
                # Força multi quando necessário
                if isinstance(geom, Polygon):
                    geom = MultiPolygon([geom])
                elif isinstance(geom, LineString):
                    geom = MultiLineString([geom])
                kwargs["geometry"] = f"SRID=4326;{geom.wkt}"
            batch.append(model_class(**kwargs))
            if len(batch) >= batch_size:
                session.bulk_save_objects(batch)
                session.commit()
                total += len(batch)
                batch = []
        if batch:
            session.bulk_save_objects(batch)
            session.commit()
            total += len(batch)
    finally:
        session.close()
    return total


# ==========================================================================
# Loaders individuais
# ==========================================================================


def load_sigmine() -> dict:
    def fn():
        client = DadosGovClient()
        pkg = client.package_show("sigmine-processos-minerarios")
        res = client.pick_resource(pkg, format_hint="SHP", name_hint="brasil")
        if not res:
            raise RuntimeError("Recurso SHP SIGMINE não encontrado")
        content = client.download_resource(res, max_mb=400)
        shp = _extract_shapefile(content)
        if not shp:
            raise RuntimeError("SHP não extraído")
        persisted = _load_shapefile_to_table(
            shp, SigmineProcesso, "sigmine_processos",
            column_map={
                "PROCESSO": "processo", "ANO": "ano", "FASE": "fase",
                "ULT_EVENTO": "ult_evento", "NOME": "nome",
                "SUBS": "subs", "UF": "uf", "AREA_HA": "area_ha", "USO": "uso",
            },
        )
        return persisted, persisted, res.get("url", "")
    return _run_loader("sigmine", "sigmine-processos-minerarios", fn)


def load_ana_outorgas() -> dict:
    def fn():
        client = DadosGovClient()
        pkg = client.package_show("outorgas-de-direito-de-uso-de-recursos-hidricos")
        res = client.pick_resource(pkg, format_hint="CSV", name_hint="outorga")
        if not res:
            raise RuntimeError("Recurso CSV ANA não encontrado")
        content = client.download_resource(res, max_mb=200)
        import pandas as pd
        df = pd.read_csv(io.BytesIO(content), sep=None, engine="python", dtype=str, on_bad_lines="skip")
        if df.empty:
            return 0, 0, res.get("url", "")

        _truncate("ana_outorgas_full")
        session = get_session()
        persisted = 0
        try:
            batch = []
            for _, r in df.iterrows():
                try:
                    lat = float(str(r.get("LATITUDE") or r.get("lat") or "0").replace(",", "."))
                    lon = float(str(r.get("LONGITUDE") or r.get("lon") or "0").replace(",", "."))
                except Exception:
                    lat, lon = 0, 0
                if lat == 0 and lon == 0:
                    continue
                o = AnaOutorga(
                    numero_ato=str(r.get("NUMERO_ATO") or r.get("numero_ato") or "")[:100],
                    uf=str(r.get("UF") or "")[:2],
                    municipio=str(r.get("MUNICIPIO") or "")[:200],
                    finalidade=str(r.get("FINALIDADE") or "")[:200],
                    nome_corpo_hidrico=str(r.get("CORPO_HIDRICO") or r.get("nome_corpo_hidrico") or "")[:300],
                    geometry=f"SRID=4326;POINT({lon} {lat})",
                    raw_data=_clean_for_json(r.to_dict()),
                )
                batch.append(o)
                if len(batch) >= 500:
                    session.bulk_save_objects(batch)
                    session.commit()
                    persisted += len(batch)
                    batch = []
            if batch:
                session.bulk_save_objects(batch)
                session.commit()
                persisted += len(batch)
        finally:
            session.close()
        return len(df), persisted, res.get("url", "")
    return _run_loader("ana_outorgas", "outorgas-de-direito-de-uso-de-recursos-hidricos", fn)


def load_ana_bho() -> dict:
    def fn():
        client = DadosGovClient()
        pkg = client.package_show("base-hidrografica-ottocodificada-multiescalas-2017-5k")
        res = client.pick_resource(pkg, format_hint="SHP", name_hint="trecho")
        if not res:
            # fallback
            pkg = client.package_show("base-hidrografica-ottocodificada")
            res = client.pick_resource(pkg, format_hint="SHP")
        if not res:
            raise RuntimeError("Recurso ANA BHO não encontrado")
        content = client.download_resource(res, max_mb=500)
        shp = _extract_shapefile(content)
        if not shp:
            raise RuntimeError("SHP BHO não extraído")
        persisted = _load_shapefile_to_table(
            shp, AnaBho, "ana_bho",
            column_map={
                "cocursodag": "cocursodag", "cotrecho": "cotrecho",
                "noriocomp": "nome_curso", "nuordemcda": "nu_ordem",
                "nucompch": "nu_comptrec", "nuareacont": "nu_areacont",
            },
        )
        return persisted, persisted, res.get("url", "")
    return _run_loader("ana_bho", "base-hidrografica-ottocodificada", fn)


def load_assentamentos() -> dict:
    def fn():
        client = DadosGovClient()
        pkg = client.package_show("assentamentos-brasil")
        res = client.pick_resource(pkg, format_hint="SHP")
        if not res:
            raise RuntimeError("Recurso SHP assentamentos não encontrado")
        content = client.download_resource(res, max_mb=300)
        shp = _extract_shapefile(content)
        if not shp:
            raise RuntimeError("SHP assentamentos não extraído")
        persisted = _load_shapefile_to_table(
            shp, IncraAssentamento, "incra_assentamentos",
            column_map={
                "nome_proje": "nome_proje", "cd_sipra": "cd_sipra",
                "municipio": "municipio", "uf": "uf",
                "area_ha": "area_ha", "capacidade": "capacidade",
                "num_famili": "num_famili", "data_criac": "data_criac",
                "fase": "fase", "forma_obte": "forma_obte", "esfera": "esfera",
            },
        )
        return persisted, persisted, res.get("url", "")
    return _run_loader("assentamentos", "assentamentos-brasil", fn)


def load_quilombolas() -> dict:
    def fn():
        client = DadosGovClient()
        pkg = client.package_show("areas-quilombolas")
        res = client.pick_resource(pkg, format_hint="SHP")
        if not res:
            raise RuntimeError("Recurso SHP quilombolas não encontrado")
        content = client.download_resource(res, max_mb=200)
        shp = _extract_shapefile(content)
        if not shp:
            raise RuntimeError("SHP quilombolas não extraído")
        persisted = _load_shapefile_to_table(
            shp, IncraQuilombola, "incra_quilombolas",
            column_map={
                "nome": "nome", "municipio": "municipio", "uf": "uf",
                "area_ha": "area_ha", "num_famili": "num_famili",
                "fase": "fase", "esfera": "esfera",
            },
        )
        return persisted, persisted, res.get("url", "")
    return _run_loader("quilombolas", "areas-quilombolas", fn)


def load_aneel_usinas() -> dict:
    def fn():
        client = DadosGovClient()
        pkg = client.package_show("empreendimentos-de-geracao-de-energia-eletrica-siga-aneel")
        res = client.pick_resource(pkg, format_hint="CSV")
        if not res:
            pkg = client.package_show("empreendimentos-de-geracao-de-energia-eletrica-big")
            res = client.pick_resource(pkg, format_hint="CSV")
        if not res:
            raise RuntimeError("Recurso CSV ANEEL não encontrado")
        content = client.download_resource(res, max_mb=200)
        import pandas as pd
        df = None
        # ANEEL CSV usa Latin-1/ISO-8859-1 e ; como separador
        for enc in ("latin-1", "cp1252", "utf-8"):
            try:
                df = pd.read_csv(
                    io.BytesIO(content), sep=";", dtype=str,
                    on_bad_lines="skip", encoding=enc,
                )
                break
            except Exception:
                continue
        if df is None or df.empty:
            # último fallback: autodetecção
            df = pd.read_csv(
                io.BytesIO(content), sep=None, engine="python", dtype=str,
                on_bad_lines="skip", encoding_errors="replace",
            )
        if df.empty:
            return 0, 0, res.get("url", "")
        _truncate("aneel_usinas")
        session = get_session()
        persisted = 0
        try:
            batch = []
            for _, r in df.iterrows():
                try:
                    lat = float(str(r.get("LAT") or r.get("DscEmprLat") or "0").replace(",", "."))
                    lon = float(str(r.get("LON") or r.get("DscEmprLong") or "0").replace(",", "."))
                except Exception:
                    lat, lon = 0, 0
                try:
                    pot = float(str(r.get("POT_MW") or r.get("MdaPotenciaOutorgadaKw") or "0").replace(",", "."))
                except Exception:
                    pot = 0
                o = AneelUsina(
                    ceg=str(r.get("CEG") or "")[:50],
                    nome=str(r.get("EMPREENDIMENTO") or r.get("NomEmpreendimento") or "")[:300],
                    tipo=str(r.get("TIPO") or r.get("SigTipoGeracao") or "")[:50],
                    combustivel=str(r.get("COMBUSTIVEL") or r.get("DscFonteCombustivel") or "")[:100],
                    potencia_mw=pot,
                    uf=str(r.get("UF") or r.get("SigUFPrincipal") or "")[:2],
                    municipio=str(r.get("MUNICIPIO") or r.get("DscMuninicpios") or "")[:200],
                    geometry=f"SRID=4326;POINT({lon} {lat})" if lat else None,
                    raw_data=_clean_for_json(r.to_dict()),
                )
                batch.append(o)
                if len(batch) >= 500:
                    session.bulk_save_objects(batch)
                    session.commit()
                    persisted += len(batch)
                    batch = []
            if batch:
                session.bulk_save_objects(batch)
                session.commit()
                persisted += len(batch)
        finally:
            session.close()
        return len(df), persisted, res.get("url", "")
    return _run_loader("aneel_usinas", "empreendimentos-de-geracao-de-energia-eletrica-siga-aneel", fn)


def load_aneel_linhas() -> dict:
    """
    Linhas de Transmissão do SIGET (ANEEL) via ArcGIS FeatureServer.

    O CKAN do dados.gov.br não publica este dataset em formato SHP público.
    Extraímos direto do servidor ArcGIS da ANEEL (SIGEL), que expõe GeoJSON
    via `/query?f=geojson`. ~176 linhas monitoradas.
    """
    def fn():
        import httpx
        import json as _json
        base = "https://sigel.aneel.gov.br/arcgis/rest/services/GGT/Dados_WebApp_GGT/MapServer/0/query"
        all_features: list[dict] = []
        offset = 0
        page_size = 500
        with httpx.Client(timeout=60, follow_redirects=True) as c:
            while True:
                r = c.get(base, params={
                    "where": "1=1",
                    "outFields": "*",
                    "resultOffset": offset,
                    "resultRecordCount": page_size,
                    "f": "geojson",
                    "outSR": 4326,
                }, headers={"User-Agent": "AgroJus/1.0"})
                r.raise_for_status()
                payload = r.json()
                feats = payload.get("features", [])
                if not feats:
                    break
                all_features.extend(feats)
                if len(feats) < page_size:
                    break
                offset += page_size

        if not all_features:
            return 0, 0, base

        _truncate("aneel_linhas_transmissao")

        from shapely.geometry import shape as _shape, MultiLineString, LineString
        session = get_session()
        persisted = 0
        try:
            batch = []
            for f in all_features:
                props = f.get("properties", {}) or {}
                geom = None
                g = f.get("geometry")
                if g:
                    try:
                        shp = _shape(g)
                        if isinstance(shp, LineString):
                            shp = MultiLineString([shp])
                        if not shp.is_empty:
                            geom = f"SRID=4326;{shp.wkt}"
                    except Exception:
                        pass
                try:
                    tensao = float(props.get("TENSAO_KV") or 0)
                except Exception:
                    tensao = None
                try:
                    extensao = float(props.get("EXT_REDE_KM") or props.get("EX_SIGET_KM") or 0)
                except Exception:
                    extensao = None

                batch.append(AneelLinhaTransmissao(
                    nome=str(props.get("LINHA_TRANS") or "")[:300],
                    tensao_kv=tensao,
                    operador=str(props.get("TRANSMISSOR") or "")[:300],
                    situacao=str(props.get("SITUACAO") or "")[:50],
                    comprimento_km=extensao,
                    geometry=geom,
                ))
                if len(batch) >= 500:
                    session.bulk_save_objects(batch)
                    session.commit()
                    persisted += len(batch)
                    batch = []
            if batch:
                session.bulk_save_objects(batch)
                session.commit()
                persisted += len(batch)
        finally:
            session.close()
        return len(all_features), persisted, base
    return _run_loader("aneel_linhas", "aneel-siget-linhas-transmissao", fn)


def load_garantia_safra() -> dict:
    def fn():
        client = DadosGovClient()
        pkg = client.package_show("beneficiarios-do-programa-garantia-safra")
        res = client.pick_resource(pkg, format_hint="CSV")
        if not res:
            raise RuntimeError("Recurso CSV Garantia-Safra não encontrado")
        content = client.download_resource(res, max_mb=500)
        import pandas as pd
        df = pd.read_csv(io.BytesIO(content), sep=None, engine="python", dtype=str, on_bad_lines="skip", encoding_errors="replace")
        if df.empty:
            return 0, 0, res.get("url", "")
        _truncate("garantia_safra")
        session = get_session()
        persisted = 0
        try:
            batch = []
            for _, r in df.iterrows():
                try:
                    valor = float(str(r.get("VALOR") or r.get("VALOR_BENEFICIO") or "0").replace(",", "."))
                except Exception:
                    valor = 0
                try:
                    ano = int(str(r.get("ANO_SAFRA") or r.get("ANO") or "0")[:4])
                except Exception:
                    ano = 0
                o = GarantiaSafraBeneficiario(
                    nis=str(r.get("NIS") or "")[:20],
                    nome=str(r.get("NOME") or "")[:300],
                    cpf_cnpj=str(r.get("CPF") or r.get("CPF_CNPJ") or "")[:20],
                    municipio=str(r.get("MUNICIPIO") or "")[:200],
                    uf=str(r.get("UF") or "")[:2],
                    ano_safra=ano,
                    valor_beneficio=valor,
                    raw_data=_clean_for_json(r.to_dict()),
                )
                batch.append(o)
                if len(batch) >= 1000:
                    session.bulk_save_objects(batch)
                    session.commit()
                    persisted += len(batch)
                    batch = []
            if batch:
                session.bulk_save_objects(batch)
                session.commit()
                persisted += len(batch)
        finally:
            session.close()
        return len(df), persisted, res.get("url", "")
    return _run_loader("garantia_safra", "beneficiarios-do-programa-garantia-safra", fn)


# -------------------------------------------------------------------------
# Portal Transparência
# -------------------------------------------------------------------------


def _parse_br_date(s: str):
    """Converte dd/mm/yyyy para date ou retorna None."""
    if not s or "Sem informação" in s or "sem informa" in s.lower():
        return None
    try:
        from datetime import datetime as _dt
        return _dt.strptime(s.strip(), "%d/%m/%Y").date()
    except Exception:
        return None


def _normalize_portal_record(r: dict) -> Optional[dict]:
    """
    Extrai campos do registro CEIS/CNEP do Portal da Transparência.
    Schema real (verificado em abr/2026):
      - sancionado.codigoFormatado        → CPF/CNPJ mascarado
      - sancionado.nome                   → nome
      - pessoa.cpfFormatado | cnpjFormatado → CPF ou CNPJ
      - pessoa.nome, razaoSocialReceita, nomeFantasiaReceita, tipo
      - tipoSancao.descricaoResumida
      - orgaoSancionador.nome, siglaUf, poder, esfera
      - fonteSancao.nomeExibicao
      - dataInicioSancao, dataFimSancao (dd/mm/yyyy)
      - numeroProcesso
    """
    sancionado = r.get("sancionado", {}) or {}
    pessoa = r.get("pessoa", {}) or {}
    sancao = r.get("tipoSancao", {}) or {}
    orgao = r.get("orgaoSancionador", {}) or {}

    # Preferência: pessoa.cnpjFormatado > pessoa.cpfFormatado > sancionado.codigoFormatado
    doc_raw = (
        pessoa.get("cnpjFormatado")
        or pessoa.get("cpfFormatado")
        or sancionado.get("codigoFormatado")
        or ""
    )
    cpf_cnpj = str(doc_raw).replace(".", "").replace("/", "").replace("-", "")
    if not cpf_cnpj or cpf_cnpj in ("00000000000", "00000000000000"):
        return None

    is_pj = bool(pessoa.get("cnpjFormatado")) or "cnpj" in str(pessoa.get("tipo", "")).lower()

    return {
        "cpf_cnpj": cpf_cnpj[:20],
        "nome": str(sancionado.get("nome") or pessoa.get("nome") or "")[:500],
        "razao_social": str(pessoa.get("razaoSocialReceita") or sancionado.get("nome") or "")[:500],
        "tipo_pessoa": "PJ" if is_pj else "PF",
        "tipo_sancao": str(sancao.get("descricaoResumida") or sancao.get("descricaoPortal") or "")[:200],
        "data_inicio_sancao": _parse_br_date(r.get("dataInicioSancao")),
        "data_fim_sancao": _parse_br_date(r.get("dataFimSancao")),
        "orgao_sancionador": str(orgao.get("nome") or "")[:300],
        "uf_orgao": str(orgao.get("siglaUf") or "")[:2],
        "fundamentacao": "; ".join(
            f.get("descricao", "")[:200]
            for f in (r.get("fundamentacao") or [])
            if isinstance(f, dict)
        )[:2000],
        "processo": str(r.get("numeroProcesso") or "")[:100],
        "raw_data": r,
    }


def load_ibama_embargos() -> dict:
    """IBAMA termos de embargo com geometria (SHP do pamgia.ibama.gov.br)."""
    def fn():
        client = DadosGovClient()
        pkg = client.package_show("ibama-termo-de-embargo")
        res = client.pick_resource(pkg, format_hint="SHP")
        if not res:
            raise RuntimeError("SHP IBAMA embargos não encontrado")
        content = client.download_resource(res, max_mb=600)
        shp = _extract_shapefile(content)
        if not shp:
            raise RuntimeError("SHP embargos não extraído")

        # Campos do SHP do IBAMA variam levemente ao longo do tempo;
        # usamos mapeamento flexível que aceita variantes conhecidas.
        import geopandas as gpd
        gdf = gpd.read_file(shp)
        if gdf.empty:
            return 0, 0, res.get("url", "")
        try:
            if gdf.crs and gdf.crs.to_epsg() != 4326:
                gdf = gdf.to_crs(epsg=4326)
        except Exception:
            pass

        _truncate("ibama_embargos")

        def pick(row, *candidates):
            for k in candidates:
                if k in row and row[k] is not None and str(row[k]).lower() != "nan":
                    return row[k]
            return None

        session = get_session()
        persisted = 0
        try:
            batch = []
            for _, r in gdf.iterrows():
                cpf = str(pick(r, "CPF_CNPJ_S", "CPF_CNPJ", "CNPJ_INFR", "CPF_INFRA") or "").replace(".", "").replace("/", "").replace("-", "")
                area_str = str(pick(r, "AREA_EMB_H", "AREA_HA", "AREA_EMBARG") or "0").replace(",", ".")
                try:
                    area_ha = float(area_str)
                except Exception:
                    area_ha = None
                data_str = pick(r, "DATA_TAD", "DT_EMBARGO", "DATA_EMBARG")
                data_embargo = None
                if data_str:
                    try:
                        from datetime import datetime as _dt
                        data_embargo = _dt.strptime(str(data_str)[:10], "%Y-%m-%d").date()
                    except Exception:
                        try:
                            from datetime import datetime as _dt
                            data_embargo = _dt.strptime(str(data_str)[:10], "%d/%m/%Y").date()
                        except Exception:
                            pass

                geom_wkt = None
                if r.geometry is not None and not r.geometry.is_empty:
                    from shapely.geometry import MultiPolygon, Polygon
                    geom = r.geometry
                    if isinstance(geom, Polygon):
                        geom = MultiPolygon([geom])
                    geom_wkt = f"SRID=4326;{geom.wkt}"

                batch.append(IbamaEmbargo(
                    numero_termo=str(pick(r, "NUM_TAD", "N_TAD", "TAD_NUM") or "")[:50],
                    cpf_cnpj=cpf[:20] or None,
                    nome_pessoa=str(pick(r, "NOM_PESSOA", "NOME_PESSO", "NOME_INFR") or "")[:500],
                    uf=str(pick(r, "UF", "UF_EMB") or "")[:2],
                    municipio=str(pick(r, "MUNICIPIO", "MUN_EMB") or "")[:200],
                    area_embargada_ha=area_ha,
                    data_embargo=data_embargo,
                    tipo_infracao=str(pick(r, "DES_INFRA", "TIPO_INFRA") or "")[:300],
                    situacao=str(pick(r, "SIT_EMB", "SITUACAO", "STATUS") or "")[:50],
                    geometry=geom_wkt,
                    raw_data=_clean_for_json(dict(r.drop(labels=["geometry"], errors="ignore"))),
                ))
                if len(batch) >= 500:
                    session.bulk_save_objects(batch)
                    session.commit()
                    persisted += len(batch)
                    batch = []
            if batch:
                session.bulk_save_objects(batch)
                session.commit()
                persisted += len(batch)
        finally:
            session.close()
        return persisted, persisted, res.get("url", "")
    return _run_loader("ibama_embargos", "ibama-termo-de-embargo", fn)


def load_ibama_autos_infracao() -> dict:
    """IBAMA autos de infração completos — ZIP com múltiplos CSVs (1 por ano)."""
    def fn():
        client = DadosGovClient()
        pkg = client.package_show("fiscalizacao-auto-de-infracao")
        res = client.pick_resource(pkg, format_hint="CSV")
        if not res:
            raise RuntimeError("CSV autos IBAMA não encontrado")
        content = client.download_resource(res, max_mb=400)

        import zipfile, io as _io
        import pandas as pd

        def _date(s):
            if not s or str(s).strip() == "" or str(s).lower() == "nan":
                return None
            from datetime import datetime as _dt
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y"):
                try:
                    return _dt.strptime(str(s).strip()[:len(fmt)+2], fmt).date()
                except Exception:
                    continue
            return None

        def _flt(s):
            try:
                return float(str(s).replace(",", "."))
            except Exception:
                return None

        _truncate("ibama_autos_infracao")

        session = get_session()
        total_rows = 0
        persisted = 0
        seen_nums: set[str] = set()

        try:
            with zipfile.ZipFile(_io.BytesIO(content)) as zf:
                csv_names = sorted(n for n in zf.namelist() if n.lower().endswith(".csv"))
                if not csv_names:
                    raise RuntimeError("ZIP sem CSV dentro")
                logger.info("IBAMA autos: %d CSVs no zip", len(csv_names))

                for csv_name in csv_names:
                    with zf.open(csv_name) as f:
                        raw = f.read()
                    df = None
                    for enc in ("latin-1", "cp1252", "utf-8"):
                        try:
                            df = pd.read_csv(
                                _io.BytesIO(raw), sep=";", dtype=str,
                                on_bad_lines="skip", encoding=enc,
                            )
                            break
                        except Exception:
                            continue
                    if df is None or df.empty:
                        continue
                    total_rows += len(df)

                    batch = []
                    for _, r in df.iterrows():
                        num = str(
                            r.get("NUM_AUTO_INFRACAO") or r.get("SEQ_AUTO_INFRACAO") or ""
                        ).strip()[:50]
                        if not num:
                            continue
                        # serie + numero é a chave natural; garante unicidade
                        serie = str(r.get("SER_AUTO_INFRACAO") or "").strip()[:20]
                        key = f"{num}-{serie}"
                        if key in seen_nums:
                            continue
                        seen_nums.add(key)

                        cpf = str(r.get("CPF_CNPJ_INFRATOR") or "").replace(".", "").replace("/", "").replace("-", "")[:20]
                        batch.append(IbamaAutoInfracao(
                            numero_auto=num,
                            serie_auto=serie,
                            tipo_auto=str(r.get("TIPO_AUTO") or "")[:50],
                            cpf_cnpj_infrator=cpf or None,
                            nome_infrator=str(r.get("NOME_INFRATOR") or "")[:500],
                            data_auto=_date(r.get("DAT_HORA_AUTO_INFRACAO")),
                            data_lavratura=_date(r.get("DT_LANCAMENTO")),
                            uf=str(r.get("UF") or "")[:2],
                            municipio=str(r.get("MUNICIPIO") or "")[:200],
                            valor_auto=_flt(r.get("VAL_AUTO_INFRACAO")),
                            status_debito=str(r.get("DES_STATUS_FORMULARIO") or r.get("DS_SIT_AUTO_AIE") or "")[:50],
                            desc_infracao=(str(r.get("DES_AUTO_INFRACAO") or r.get("DES_INFRACAO") or "")[:3000]) or None,
                            enq_legal=str(r.get("DS_ENQUADRAMENTO_ADMINISTRATIVO") or r.get("DS_ENQUADRAMENTO_NAO_ADMINISTRATIVO") or "")[:200],
                            lat=_flt(r.get("NUM_LATITUDE_AUTO")),
                            lon=_flt(r.get("NUM_LONGITUDE_AUTO")),
                            raw_data=None,  # raw muito grande (70+ colunas × 600k+ linhas)
                        ))
                        if len(batch) >= 1000:
                            session.bulk_save_objects(batch)
                            session.commit()
                            persisted += len(batch)
                            batch = []
                    if batch:
                        session.bulk_save_objects(batch)
                        session.commit()
                        persisted += len(batch)

                    if len(seen_nums) % 50000 < 1000:
                        logger.info(
                            "IBAMA autos: %d processados (%d persistidos)",
                            total_rows, persisted,
                        )
        finally:
            session.close()
        return total_rows, persisted, res.get("url", "")
    return _run_loader("ibama_autos_infracao", "fiscalizacao-auto-de-infracao", fn)


def load_ceis() -> dict:
    def fn():
        client = PortalTransparenciaClient()
        rows = client.fetch_ceis(max_pages=200)
        _truncate("ceis_registros")
        session = get_session()
        persisted = 0
        try:
            batch = []
            for r in rows:
                norm = _normalize_portal_record(r)
                if not norm:
                    continue
                batch.append(CeisRegistro(**norm))
                if len(batch) >= 500:
                    session.bulk_save_objects(batch)
                    session.commit()
                    persisted += len(batch)
                    batch = []
            if batch:
                session.bulk_save_objects(batch)
                session.commit()
                persisted += len(batch)
        finally:
            session.close()
        return len(rows), persisted, "api.portaldatransparencia.gov.br/api-de-dados/ceis"
    return _run_loader("ceis", "ceis-portal-transparencia", fn)


def load_cnep() -> dict:
    def fn():
        client = PortalTransparenciaClient()
        rows = client.fetch_cnep(max_pages=200)
        _truncate("cnep_registros")
        session = get_session()
        persisted = 0
        try:
            batch = []
            for r in rows:
                norm = _normalize_portal_record(r)
                if not norm:
                    continue
                try:
                    valor = float(r.get("valorMultaAtualizado") or r.get("valorMulta") or 0)
                except Exception:
                    valor = 0
                norm.pop("uf_orgao", None)  # não existe em CNEP model
                norm.pop("fundamentacao", None)  # CNEP usa Text mesmo, manter
                norm["valor_multa"] = valor
                # CNEP model tem campos ligeiramente diferentes; reusa maioria
                batch.append(CnepRegistro(
                    cpf_cnpj=norm["cpf_cnpj"],
                    nome=norm["nome"],
                    razao_social=norm["razao_social"],
                    tipo_pessoa=norm["tipo_pessoa"],
                    tipo_sancao=norm["tipo_sancao"],
                    data_inicio_sancao=norm.get("data_inicio_sancao"),
                    data_fim_sancao=norm.get("data_fim_sancao"),
                    valor_multa=valor,
                    orgao_sancionador=norm["orgao_sancionador"],
                    fundamentacao="; ".join(
                        f.get("descricao", "")[:200]
                        for f in (r.get("fundamentacao") or [])
                        if isinstance(f, dict)
                    )[:2000],
                    processo=norm["processo"],
                    raw_data=r,
                ))
                if len(batch) >= 500:
                    session.bulk_save_objects(batch)
                    session.commit()
                    persisted += len(batch)
                    batch = []
            if batch:
                session.bulk_save_objects(batch)
                session.commit()
                persisted += len(batch)
        finally:
            session.close()
        return len(rows), persisted, "api.portaldatransparencia.gov.br/api-de-dados/cnep"
    return _run_loader("cnep", "cnep-portal-transparencia", fn)


# -------------------------------------------------------------------------
# Registro central
# -------------------------------------------------------------------------

LOADERS: dict[str, Callable[[], dict]] = {
    "sigmine": load_sigmine,
    "ana_outorgas": load_ana_outorgas,
    "ana_bho": load_ana_bho,
    "assentamentos": load_assentamentos,
    "quilombolas": load_quilombolas,
    "aneel_usinas": load_aneel_usinas,
    "aneel_linhas": load_aneel_linhas,
    "garantia_safra": load_garantia_safra,
    "ibama_embargos": load_ibama_embargos,
    "ibama_autos_infracao": load_ibama_autos_infracao,
    "ceis": load_ceis,
    "cnep": load_cnep,
}


def run_all() -> list[dict]:
    """Executa todos os loaders em sequência (idempotente)."""
    results: list[dict] = []
    for name, fn in LOADERS.items():
        logger.info("Executando loader: %s", name)
        res = fn()
        results.append(res)
        logger.info("  %s: %s", name, res)
    return results
