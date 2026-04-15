"""
PostGIS Spatial Analyzer — Motor de cruzamento espacial.

Recebe um codigo CAR, busca a geometria na tabela geo_car,
e cruza com todas as camadas espaciais via ST_Intersects.

Camadas cruzadas:
- geo_terras_indigenas (FUNAI)
- geo_unidades_conservacao (ICMBio)
- geo_embargos_icmbio (ICMBio)
- geo_autos_icmbio (ICMBio)
- geo_prodes (INPE — desmatamento anual)
- geo_deter_amazonia (INPE — alertas tempo real)
- geo_deter_cerrado (INPE — alertas tempo real)
- geo_mapbiomas_alertas (MapBiomas)
- environmental_alerts (IBAMA embargos)
- mapbiomas_credito_rural (credito rural georreferenciado)
- Infraestrutura: armazens, frigorificos, rodovias, ferrovias, portos
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from sqlalchemy import text

from app.models.database import get_engine

logger = logging.getLogger("agrojus.postgis")


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------

@dataclass
class PropertyGeometry:
    """Dados basicos do imovel extraidos de geo_car."""
    car_code: str
    municipio: str = ""
    uf: str = ""
    area_ha: float = 0.0
    status: str = ""
    tipo_imovel: str = ""
    modulos_fiscais: float = 0.0
    cod_municipio_ibge: int = 0
    geometry_wkt: str = ""
    geometry_geojson: str = ""


@dataclass
class SpatialHit:
    """Um unico resultado de cruzamento espacial."""
    layer: str
    name: str = ""
    details: dict = field(default_factory=dict)
    overlap_area_ha: float = 0.0
    distance_km: float = 0.0
    date: Optional[str] = None


@dataclass
class SpatialAnalysisResult:
    """Resultado consolidado de todos os cruzamentos."""
    car_code: str
    property_info: Optional[PropertyGeometry] = None

    # Cruzamentos espaciais
    terras_indigenas: list[SpatialHit] = field(default_factory=list)
    unidades_conservacao: list[SpatialHit] = field(default_factory=list)
    embargos_icmbio: list[SpatialHit] = field(default_factory=list)
    autos_icmbio: list[SpatialHit] = field(default_factory=list)
    prodes_desmatamento: list[SpatialHit] = field(default_factory=list)
    deter_alertas: list[SpatialHit] = field(default_factory=list)
    mapbiomas_alertas: list[SpatialHit] = field(default_factory=list)
    embargos_ibama: list[SpatialHit] = field(default_factory=list)
    credito_rural: list[SpatialHit] = field(default_factory=list)

    # Infraestrutura proxima
    armazens_proximos: list[SpatialHit] = field(default_factory=list)
    frigorificos_proximos: list[SpatialHit] = field(default_factory=list)
    rodovias_proximas: list[SpatialHit] = field(default_factory=list)
    portos_proximos: list[SpatialHit] = field(default_factory=list)

    # Flags para compliance
    has_prodes_post_2019: bool = False
    has_prodes_post_2020: bool = False
    has_embargo_ativo: bool = False
    has_terra_indigena: bool = False
    has_uc_protecao_integral: bool = False

    # Metadados
    layers_checked: int = 0
    layers_with_hits: int = 0
    query_time_ms: float = 0.0
    errors: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Analyzer
# ---------------------------------------------------------------------------

class PostGISAnalyzer:
    """Executa cruzamentos espaciais contra o PostGIS."""

    def __init__(self):
        self.engine = get_engine()

    def analyze(self, car_code: str) -> SpatialAnalysisResult:
        """
        Analise completa: busca geometria e cruza com todas as camadas.

        Args:
            car_code: Codigo CAR (ex: MA-2102101-XXXX)

        Returns:
            SpatialAnalysisResult com todos os cruzamentos
        """
        import time
        start = time.time()
        result = SpatialAnalysisResult(car_code=car_code)

        # 1. Buscar geometria do imovel
        prop = self._get_property_geometry(car_code)
        if not prop:
            result.errors.append(f"CAR {car_code} nao encontrado em geo_car")
            return result
        result.property_info = prop

        # 2. Executar todos os cruzamentos
        checks = [
            ("terras_indigenas", self._check_terras_indigenas),
            ("unidades_conservacao", self._check_unidades_conservacao),
            ("embargos_icmbio", self._check_embargos_icmbio),
            ("autos_icmbio", self._check_autos_icmbio),
            ("prodes_desmatamento", self._check_prodes),
            ("deter_alertas", self._check_deter),
            ("mapbiomas_alertas", self._check_mapbiomas_alertas),
            ("embargos_ibama", self._check_embargos_ibama),
            ("credito_rural", self._check_credito_rural),
            ("armazens_proximos", self._check_armazens),
            ("frigorificos_proximos", self._check_frigorificos),
            ("rodovias_proximas", self._check_rodovias),
            ("portos_proximos", self._check_portos),
        ]

        for attr, fn in checks:
            result.layers_checked += 1
            try:
                hits = fn(car_code)
                setattr(result, attr, hits)
                if hits:
                    result.layers_with_hits += 1
            except Exception as e:
                logger.warning("Erro no cruzamento %s: %s", attr, e)
                result.errors.append(f"{attr}: {e}")

        # 3. Setar flags de compliance
        result.has_prodes_post_2019 = any(
            h.details.get("year", 0) >= 2019 for h in result.prodes_desmatamento
        )
        result.has_prodes_post_2020 = any(
            h.details.get("year", 0) >= 2020 for h in result.prodes_desmatamento
        )
        result.has_embargo_ativo = bool(result.embargos_icmbio or result.embargos_ibama)
        result.has_terra_indigena = bool(result.terras_indigenas)
        result.has_uc_protecao_integral = any(
            h.details.get("grupo") == "Proteção Integral"
            for h in result.unidades_conservacao
        )

        elapsed = (time.time() - start) * 1000
        result.query_time_ms = round(elapsed, 1)
        logger.info(
            "Analise CAR %s: %d camadas, %d com hits, %.0fms",
            car_code, result.layers_checked, result.layers_with_hits, elapsed,
        )
        return result

    # ------------------------------------------------------------------
    # Busca de geometria do imovel
    # ------------------------------------------------------------------

    def _get_property_geometry(self, car_code: str) -> Optional[PropertyGeometry]:
        """Busca geometria e dados basicos do CAR.

        Prioridade: sicar_completo (BigQuery, 79M registros) > geo_car (WFS, 135k registros).
        """
        # Tentar sicar_completo primeiro (dados mais recentes e completos)
        sql_sicar = text("""
            SELECT
                cod_imovel,
                '' as municipio,
                uf,
                area,
                COALESCE(status_imovel, '') as status,
                COALESCE(tipo_imovel, '') as tipo,
                COALESCE(m_fiscal, 0) as m_fiscal,
                COALESCE(cod_municipio_ibge, '0')::int as cod_ibge,
                ST_AsText(geometry) as wkt,
                ST_AsGeoJSON(geometry) as geojson
            FROM sicar_completo
            WHERE cod_imovel = :car_code
              AND geometry IS NOT NULL
            LIMIT 1
        """)
        with self.engine.connect() as conn:
            try:
                row = conn.execute(sql_sicar, {"car_code": car_code}).mappings().first()
                if row:
                    return self._row_to_property(row)
            except Exception:
                pass  # tabela pode nao existir ainda

        # Fallback: geo_car (WFS)
        sql = text("""
            SELECT
                cod_imovel,
                municipio,
                uf,
                area,
                COALESCE(status_imovel, '') as status,
                COALESCE(tipo_imovel, '') as tipo,
                COALESCE(m_fiscal, 0) as m_fiscal,
                COALESCE(cod_municipio_ibge, 0) as cod_ibge,
                ST_AsText(geometry) as wkt,
                ST_AsGeoJSON(geometry) as geojson
            FROM geo_car
            WHERE cod_imovel = :car_code
              AND geometry IS NOT NULL
            LIMIT 1
        """)
        with self.engine.connect() as conn:
            row = conn.execute(sql, {"car_code": car_code}).mappings().first()
            if not row:
                return None
            return self._row_to_property(row)

    @staticmethod
    def _row_to_property(row) -> PropertyGeometry:
        return PropertyGeometry(
            car_code=row["cod_imovel"],
            municipio=row["municipio"] or "",
            uf=row["uf"] or "",
            area_ha=row["area"] or 0.0,
            status=row["status"],
            tipo_imovel=row["tipo"],
            modulos_fiscais=row["m_fiscal"],
            cod_municipio_ibge=row["cod_ibge"],
            geometry_wkt=row["wkt"],
            geometry_geojson=row["geojson"],
        )

    # ------------------------------------------------------------------
    # Helper: executa ST_Intersects e retorna rows
    # ------------------------------------------------------------------

    def _intersect_query(self, sql: str, car_code: str) -> list[dict]:
        """Executa query de cruzamento espacial e retorna lista de dicts."""
        with self.engine.connect() as conn:
            rows = conn.execute(text(sql), {"car_code": car_code}).mappings().all()
            return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Cruzamentos individuais
    # ------------------------------------------------------------------

    def _check_terras_indigenas(self, car_code: str) -> list[SpatialHit]:
        sql = """
            SELECT
                ti.terrai_nom AS nome,
                ti.etnia_nome AS etnia,
                ti.fase_ti AS fase,
                ti.superficie AS superficie_ha,
                ti.uf_sigla AS uf,
                ROUND((ST_Area(ST_Intersection(
                    c.geometry::geography, ti.geometry::geography
                )) / 10000)::numeric, 2) AS overlap_ha
            FROM geo_car c
            JOIN geo_terras_indigenas ti
              ON ST_Intersects(c.geometry, ti.geometry)
            WHERE c.cod_imovel = :car_code
        """
        rows = self._intersect_query(sql, car_code)
        return [
            SpatialHit(
                layer="terras_indigenas",
                name=r["nome"] or "Desconhecida",
                overlap_area_ha=r.get("overlap_ha", 0) or 0,
                details={
                    "etnia": r.get("etnia", ""),
                    "fase": r.get("fase", ""),
                    "superficie_ha": r.get("superficie_ha", 0),
                    "uf": r.get("uf", ""),
                },
            )
            for r in rows
        ]

    def _check_unidades_conservacao(self, car_code: str) -> list[SpatialHit]:
        sql = """
            SELECT
                uc.nomeuc AS nome,
                uc.siglacateg AS categoria,
                uc.grupouc AS grupo,
                uc.esferaadm AS esfera,
                uc.areahaalb AS area_uc_ha,
                uc.biomas AS bioma,
                ROUND((ST_Area(ST_Intersection(
                    c.geometry::geography, uc.geometry::geography
                )) / 10000)::numeric, 2) AS overlap_ha
            FROM geo_car c
            JOIN geo_unidades_conservacao uc
              ON ST_Intersects(c.geometry, uc.geometry)
            WHERE c.cod_imovel = :car_code
        """
        rows = self._intersect_query(sql, car_code)
        return [
            SpatialHit(
                layer="unidades_conservacao",
                name=r["nome"] or "Desconhecida",
                overlap_area_ha=r.get("overlap_ha", 0) or 0,
                details={
                    "categoria": r.get("categoria", ""),
                    "grupo": r.get("grupo", ""),
                    "esfera": r.get("esfera", ""),
                    "area_uc_ha": r.get("area_uc_ha", 0),
                    "bioma": r.get("bioma", ""),
                },
            )
            for r in rows
        ]

    def _check_embargos_icmbio(self, car_code: str) -> list[SpatialHit]:
        sql = """
            SELECT
                e.autuado AS nome,
                e.numero_emb AS numero_embargo,
                e.numero_ai AS auto_infracao,
                e.desc_infra AS descricao,
                e.desc_sanc AS sancao,
                e.municipio,
                e.uf,
                e.data AS data_embargo,
                e.cpf_cnpj,
                e.nome_uc
            FROM geo_car c
            JOIN geo_embargos_icmbio e
              ON ST_Intersects(c.geometry, e.geometry)
            WHERE c.cod_imovel = :car_code
        """
        rows = self._intersect_query(sql, car_code)
        return [
            SpatialHit(
                layer="embargos_icmbio",
                name=r.get("nome") or r.get("autuado") or "N/A",
                date=r.get("data_embargo"),
                details={
                    "numero_embargo": r.get("numero_embargo", ""),
                    "auto_infracao": r.get("auto_infracao", ""),
                    "descricao": r.get("descricao", ""),
                    "sancao": r.get("sancao", ""),
                    "municipio": r.get("municipio", ""),
                    "uf": r.get("uf", ""),
                    "cpf_cnpj": r.get("cpf_cnpj", ""),
                    "nome_uc": r.get("nome_uc", ""),
                },
            )
            for r in rows
        ]

    def _check_autos_icmbio(self, car_code: str) -> list[SpatialHit]:
        sql = """
            SELECT
                a.autuado AS nome,
                a.numero_ai AS auto_infracao,
                a.desc_ai AS descricao,
                a.desc_sanc AS sancao,
                a.tipo_infra,
                a.valor_mult,
                a.municipio,
                a.uf,
                a.data AS data_auto,
                a.cpf_cnpj,
                a.nome_uc
            FROM geo_car c
            JOIN geo_autos_icmbio a
              ON ST_Intersects(c.geometry, a.geometry)
            WHERE c.cod_imovel = :car_code
        """
        rows = self._intersect_query(sql, car_code)
        return [
            SpatialHit(
                layer="autos_icmbio",
                name=r.get("nome") or "N/A",
                date=r.get("data_auto"),
                details={
                    "auto_infracao": r.get("auto_infracao", ""),
                    "descricao": r.get("descricao", ""),
                    "sancao": r.get("sancao", ""),
                    "tipo_infracao": r.get("tipo_infra", ""),
                    "valor_multa": r.get("valor_mult", ""),
                    "municipio": r.get("municipio", ""),
                    "uf": r.get("uf", ""),
                    "cpf_cnpj": r.get("cpf_cnpj", ""),
                    "nome_uc": r.get("nome_uc", ""),
                },
            )
            for r in rows
        ]

    def _check_prodes(self, car_code: str) -> list[SpatialHit]:
        sql = """
            SELECT
                p.year,
                p.class_name,
                p.area_km,
                p.state,
                p.satellite,
                ROUND((ST_Area(ST_Intersection(
                    c.geometry::geography, p.geometry::geography
                )) / 10000)::numeric, 2) AS overlap_ha
            FROM geo_car c
            JOIN geo_prodes p
              ON ST_Intersects(c.geometry, p.geometry)
            WHERE c.cod_imovel = :car_code
            ORDER BY p.year DESC
        """
        rows = self._intersect_query(sql, car_code)
        return [
            SpatialHit(
                layer="prodes",
                name=f"Desmatamento {r.get('year', '?')}",
                overlap_area_ha=r.get("overlap_ha", 0) or 0,
                date=str(r.get("year", "")),
                details={
                    "year": r.get("year", 0),
                    "class": r.get("class_name", ""),
                    "area_km": r.get("area_km", 0),
                    "satellite": r.get("satellite", ""),
                },
            )
            for r in rows
        ]

    def _check_deter(self, car_code: str) -> list[SpatialHit]:
        hits = []
        # Amazonia
        sql_amz = """
            SELECT
                d.classname,
                d.view_date,
                d.areauckm,
                d.municipali AS municipio,
                d.uf,
                d.satellite,
                ROUND((ST_Area(ST_Intersection(
                    c.geometry::geography, d.geometry::geography
                )) / 10000)::numeric, 2) AS overlap_ha
            FROM geo_car c
            JOIN geo_deter_amazonia d
              ON ST_Intersects(c.geometry, d.geometry)
            WHERE c.cod_imovel = :car_code
            ORDER BY d.view_date DESC
        """
        rows = self._intersect_query(sql_amz, car_code)
        for r in rows:
            vd = r.get("view_date")
            hits.append(SpatialHit(
                layer="deter_amazonia",
                name=f"DETER Amazonia - {r.get('classname', '')}",
                overlap_area_ha=r.get("overlap_ha", 0) or 0,
                date=vd.isoformat() if isinstance(vd, datetime) else str(vd or ""),
                details={
                    "classe": r.get("classname", ""),
                    "municipio": r.get("municipio", ""),
                    "uf": r.get("uf", ""),
                    "bioma": "Amazonia",
                },
            ))

        # Cerrado
        sql_cer = """
            SELECT
                d.classname,
                d.view_date,
                d.areauckm,
                d.municipality AS municipio,
                d.uf,
                ROUND((ST_Area(ST_Intersection(
                    c.geometry::geography, d.geometry::geography
                )) / 10000)::numeric, 2) AS overlap_ha
            FROM geo_car c
            JOIN geo_deter_cerrado d
              ON ST_Intersects(c.geometry, d.geometry)
            WHERE c.cod_imovel = :car_code
            ORDER BY d.view_date DESC
        """
        rows = self._intersect_query(sql_cer, car_code)
        for r in rows:
            vd = r.get("view_date")
            hits.append(SpatialHit(
                layer="deter_cerrado",
                name=f"DETER Cerrado - {r.get('classname', '')}",
                overlap_area_ha=r.get("overlap_ha", 0) or 0,
                date=vd.isoformat() if isinstance(vd, datetime) else str(vd or ""),
                details={
                    "classe": r.get("classname", ""),
                    "municipio": r.get("municipio", ""),
                    "uf": r.get("uf", ""),
                    "bioma": "Cerrado",
                },
            ))
        return hits

    def _check_mapbiomas_alertas(self, car_code: str) -> list[SpatialHit]:
        sql = """
            SELECT
                m."CODEALERTA" AS codigo,
                m."FONTE" AS fonte,
                m."BIOMA" AS bioma,
                m."ESTADO" AS estado,
                m."MUNICIPIO" AS municipio,
                m."AREAHA" AS area_alerta_ha,
                m."ANODETEC" AS ano,
                m."DATADETEC" AS data_detec,
                m."VPRESSAO" AS vetor_pressao,
                ROUND((ST_Area(ST_Intersection(
                    c.geometry::geography, m.geometry::geography
                )) / 10000)::numeric, 2) AS overlap_ha
            FROM geo_car c
            JOIN geo_mapbiomas_alertas m
              ON ST_Intersects(c.geometry, m.geometry)
            WHERE c.cod_imovel = :car_code
            ORDER BY m."ANODETEC" DESC
        """
        rows = self._intersect_query(sql, car_code)
        return [
            SpatialHit(
                layer="mapbiomas_alertas",
                name=f"Alerta {int(r.get('ano', 0))} - {r.get('bioma', '')}",
                overlap_area_ha=r.get("overlap_ha", 0) or 0,
                date=str(int(r.get("ano", 0))) if r.get("ano") else "",
                details={
                    "codigo": r.get("codigo"),
                    "fonte": r.get("fonte", ""),
                    "bioma": r.get("bioma", ""),
                    "municipio": r.get("municipio", ""),
                    "area_alerta_ha": r.get("area_alerta_ha", 0),
                    "vetor_pressao": r.get("vetor_pressao", ""),
                    "year": int(r.get("ano", 0)) if r.get("ano") else 0,
                },
            )
            for r in rows
        ]

    def _check_embargos_ibama(self, car_code: str) -> list[SpatialHit]:
        sql = """
            SELECT
                ea.alert_type,
                ea.source,
                ea.description,
                ea.area_ha,
                ea.date_detected,
                ea.cpf_cnpj,
                ea.property_car_code
            FROM geo_car c
            JOIN environmental_alerts ea
              ON ST_Intersects(c.geometry, ea.geometry)
            WHERE c.cod_imovel = :car_code
              AND ea.geometry IS NOT NULL
        """
        rows = self._intersect_query(sql, car_code)
        return [
            SpatialHit(
                layer="embargos_ibama",
                name=r.get("description") or r.get("alert_type") or "Embargo IBAMA",
                date=r["date_detected"].isoformat() if r.get("date_detected") else None,
                details={
                    "tipo": r.get("alert_type", ""),
                    "fonte": r.get("source", ""),
                    "area_ha": r.get("area_ha", 0),
                    "cpf_cnpj": r.get("cpf_cnpj", ""),
                    "car_vinculado": r.get("property_car_code", ""),
                },
            )
            for r in rows
        ]

    def _check_credito_rural(self, car_code: str) -> list[SpatialHit]:
        # mapbiomas_credito_rural usa SRID 4674, precisamos transformar
        sql = """
            SELECT
                cr.cd_programa,
                cr.vl_parc_credito,
                cr.ref_bacen,
                cr.municipality_id,
                cr.state_id,
                cr.dt_emissao,
                cr.year,
                cr.vl_area_financ,
                cr.car_code AS car_vinculado
            FROM geo_car c
            JOIN mapbiomas_credito_rural cr
              ON ST_Intersects(
                  ST_Transform(c.geometry, 4674),
                  cr.geom
              )
            WHERE c.cod_imovel = :car_code
            ORDER BY cr.year DESC
            LIMIT 50
        """
        rows = self._intersect_query(sql, car_code)
        return [
            SpatialHit(
                layer="credito_rural",
                name=f"Credito {r.get('cd_programa', '')} ({r.get('year', '')})",
                date=str(r.get("dt_emissao", "")),
                details={
                    "programa": r.get("cd_programa", ""),
                    "valor": r.get("vl_parc_credito", 0),
                    "ref_bacen": r.get("ref_bacen", ""),
                    "ano": r.get("year", 0),
                    "area_financiada_ha": r.get("vl_area_financ", 0),
                    "car_vinculado": r.get("car_vinculado", ""),
                },
            )
            for r in rows
        ]

    # ------------------------------------------------------------------
    # Infraestrutura proxima (raio de 50km)
    # ------------------------------------------------------------------

    def _check_armazens(self, car_code: str) -> list[SpatialHit]:
        sql = """
            SELECT
                COALESCE(a.name, a.armazenado, 'Armazem') AS nome,
                a.municipio,
                a.uf,
                a.capacidade,
                ROUND((ST_Distance(
                    ST_Centroid(c.geometry)::geography,
                    a.geometry::geography
                ) / 1000)::numeric, 1) AS distancia_km
            FROM geo_car c, geo_armazens_silos a
            WHERE c.cod_imovel = :car_code
              AND ST_DWithin(
                  ST_Centroid(c.geometry)::geography,
                  a.geometry::geography,
                  50000
              )
            ORDER BY distancia_km
            LIMIT 5
        """
        rows = self._intersect_query(sql, car_code)
        return [
            SpatialHit(
                layer="armazens",
                name=r.get("nome") or "Armazem",
                distance_km=float(r.get("distancia_km", 0)),
                details={
                    "municipio": r.get("municipio", ""),
                    "uf": r.get("uf", ""),
                    "capacidade": r.get("capacidade", ""),
                },
            )
            for r in rows
        ]

    def _check_frigorificos(self, car_code: str) -> list[SpatialHit]:
        sql = """
            SELECT
                COALESCE(f.razao_soci, f.nome_fanta, 'Frigorifico') AS nome,
                f.municipio,
                f.uf,
                f.sif,
                ROUND((ST_Distance(
                    ST_Centroid(c.geometry)::geography,
                    f.geometry::geography
                ) / 1000)::numeric, 1) AS distancia_km
            FROM geo_car c, geo_frigorificos f
            WHERE c.cod_imovel = :car_code
              AND ST_DWithin(
                  ST_Centroid(c.geometry)::geography,
                  f.geometry::geography,
                  100000
              )
            ORDER BY distancia_km
            LIMIT 5
        """
        rows = self._intersect_query(sql, car_code)
        return [
            SpatialHit(
                layer="frigorificos",
                name=r.get("nome") or "Frigorifico",
                distance_km=float(r.get("distancia_km", 0)),
                details={
                    "municipio": r.get("municipio", ""),
                    "uf": r.get("uf", ""),
                    "sif": r.get("sif", ""),
                },
            )
            for r in rows
        ]

    def _check_rodovias(self, car_code: str) -> list[SpatialHit]:
        sql = """
            SELECT
                r.sigla AS rodovia,
                r.tipovia AS tipo,
                ROUND((ST_Distance(
                    ST_Centroid(c.geometry)::geography,
                    r.geometry::geography
                ) / 1000)::numeric, 1) AS distancia_km
            FROM geo_car c, geo_rodovias_federais r
            WHERE c.cod_imovel = :car_code
              AND ST_DWithin(
                  ST_Centroid(c.geometry)::geography,
                  r.geometry::geography,
                  50000
              )
            ORDER BY distancia_km
            LIMIT 3
        """
        rows = self._intersect_query(sql, car_code)
        return [
            SpatialHit(
                layer="rodovias",
                name=r.get("rodovia") or "Rodovia Federal",
                distance_km=float(r.get("distancia_km", 0)),
                details={"tipo": r.get("tipo", "")},
            )
            for r in rows
        ]

    def _check_portos(self, car_code: str) -> list[SpatialHit]:
        sql = """
            SELECT
                p.nome,
                p.cidade AS municipio,
                p.estado AS uf,
                ROUND((ST_Distance(
                    ST_Centroid(c.geometry)::geography,
                    p.geometry::geography
                ) / 1000)::numeric, 1) AS distancia_km
            FROM geo_car c, geo_portos p
            WHERE c.cod_imovel = :car_code
              AND ST_DWithin(
                  ST_Centroid(c.geometry)::geography,
                  p.geometry::geography,
                  300000
              )
            ORDER BY distancia_km
            LIMIT 3
        """
        rows = self._intersect_query(sql, car_code)
        return [
            SpatialHit(
                layer="portos",
                name=r.get("nome") or "Porto",
                distance_km=float(r.get("distancia_km", 0)),
                details={
                    "municipio": r.get("municipio", ""),
                    "uf": r.get("uf", ""),
                },
            )
            for r in rows
        ]
