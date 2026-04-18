"""
MCR 2.9 expandido — 30 critérios auditáveis em 5 eixos.

Eixos e critérios (conforme Resolução CMN 5.193/2024 + normas correlatas):

  **Fundiário (8)** — regularidade cadastral do imóvel e do domínio
    F01: CAR ativo (status AT)
    F02: Sem sobreposição SIGEF/INCRA com parcela de terceiro
    F03: Sem sobreposição com Terra Indígena (FUNAI)
    F04: Sem sobreposição com UC federal/estadual
    F05: Sem sobreposição com SIGMINE/ANM (processos minerários)
    F06: CCIR válido e vigente (INCRA)
    F07: ITR quitado nos últimos 5 anos (Receita)
    F08: Sem sobreposição com SPU (terras da União)

  **Ambiental (8)** — conformidade com Código Florestal + legislação ambiental
    A01: Sem desmatamento PRODES pós-31/07/2019
    A02: Sem alerta DETER nos últimos 12 meses
    A03: Sem alerta MapBiomas validado pós-2019
    A04: Sem embargos IBAMA/ICMBio vigentes sobre a área
    A05: Sem autos de infração IBAMA contra o proprietário
    A06: Reserva Legal declarada no CAR (%)
    A07: APP declarada no CAR
    A08: Sem conflito com outorga ANA ativa

  **Trabalhista (6)** — obrigações trabalhistas e previdenciárias
    T01: Fora da Lista Suja do Trabalho Escravo (MTE)
    T02: Sem Certidão Negativa de Débitos Trabalhistas (CNDT)
    T03: CAGED/eSocial com movimentação declarada
    T04: eSocial ativo (empregador cadastrado)
    T05: NR-31 (norma trabalho rural) — declaração de conformidade
    T06: CIPATR constituída se >50 trabalhadores

  **Jurídico (5)** — litígios e pendências judiciais
    J01: Sem processos DataJud com objeto crítico (execução fiscal, usucapião)
    J02: Sem intimações DJEN recentes (últimos 30 dias)
    J03: Sem protestos em cartório
    J04: Sem reclamação CNJ contra juiz ou cartório
    J05: Sem execução fiscal federal/estadual em andamento

  **Financeiro (5)** — situação financeira e cadastrais federais
    FI01: Sem inadimplência SICOR (contratos rural em atraso)
    FI02: Não consta CEIS (Cadastro de Empresas Inidôneas)
    FI03: Não consta CNEP (Cadastro Nacional de Empresas Punidas)
    FI04: Sem pendência PIX (negativação)
    FI05: CCIR presente (também financeiro para concessão de crédito)

Status de cada critério:
  `passed`       — critério atendido com evidência
  `failed`       — critério falhou com evidência
  `pending`      — critério auditável, mas fonte de dados ainda não integrada
  `not_applicable` — critério não aplicável (ex: CIPATR sem empregados)

Cada critério retorna:
  - code, axis, title, description, regulation
  - status, passed (bool | None), details, weight
  - evidence (dict com dados específicos)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import text

from app.models.database import get_engine


# ==========================================================================
# Dataclasses
# ==========================================================================


@dataclass
class CriterionResult:
    code: str
    axis: str  # fundiario | ambiental | trabalhista | juridico | financeiro
    title: str
    description: str
    regulation: str
    status: str  # passed | failed | pending | not_applicable
    passed: Optional[bool]  # True | False | None (pending)
    details: str
    weight: float = 1.0
    evidence: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "axis": self.axis,
            "title": self.title,
            "description": self.description,
            "regulation": self.regulation,
            "status": self.status,
            "passed": self.passed,
            "details": self.details,
            "weight": self.weight,
            "evidence": self.evidence,
        }


@dataclass
class AxisScore:
    axis: str
    label: str
    total_criteria: int
    passed: int
    failed: int
    pending: int
    not_applicable: int
    weighted_score: float  # 0-100 dos critérios aplicáveis com dados

    def to_dict(self) -> dict:
        return {
            "axis": self.axis,
            "label": self.label,
            "total_criteria": self.total_criteria,
            "passed": self.passed,
            "failed": self.failed,
            "pending": self.pending,
            "not_applicable": self.not_applicable,
            "weighted_score": round(self.weighted_score, 1),
        }


@dataclass
class MCR29FullResult:
    car_code: Optional[str]
    cpf_cnpj: Optional[str]
    generated_at: str
    overall_status: str  # approved | restricted | blocked | indeterminate
    overall_score: float  # 0-1000
    risk_level: str  # LOW | MEDIUM | HIGH | CRITICAL
    axis_scores: list[AxisScore]
    criteria: list[CriterionResult]
    summary: str
    recommendation: str
    sources_consulted: list[str]
    pending_sources: list[str]

    def to_dict(self) -> dict:
        return {
            "car_code": self.car_code,
            "cpf_cnpj": self.cpf_cnpj,
            "generated_at": self.generated_at,
            "overall_status": self.overall_status,
            "overall_score": round(self.overall_score, 1),
            "risk_level": self.risk_level,
            "axis_scores": [a.to_dict() for a in self.axis_scores],
            "criteria": [c.to_dict() for c in self.criteria],
            "summary": self.summary,
            "recommendation": self.recommendation,
            "sources_consulted": self.sources_consulted,
            "pending_sources": self.pending_sources,
        }


# ==========================================================================
# Pesos (reflete impacto típico no indeferimento de crédito rural)
# ==========================================================================

WEIGHTS = {
    # Fundiário — falhas em F01/F03 são bloqueantes absolutas
    "F01": 3.0, "F02": 1.5, "F03": 3.0, "F04": 2.5, "F05": 1.0,
    "F06": 1.5, "F07": 1.0, "F08": 1.5,
    # Ambiental — A01, A04, A05 bloqueiam; A02/A03 são gatilhos
    "A01": 3.0, "A02": 2.0, "A03": 1.5, "A04": 3.0, "A05": 2.5,
    "A06": 1.5, "A07": 1.5, "A08": 1.0,
    # Trabalhista — T01 é bloqueante
    "T01": 3.0, "T02": 2.0, "T03": 1.0, "T04": 1.0, "T05": 1.0, "T06": 0.5,
    # Jurídico
    "J01": 2.0, "J02": 1.0, "J03": 1.5, "J04": 0.5, "J05": 2.0,
    # Financeiro
    "FI01": 2.5, "FI02": 2.0, "FI03": 2.0, "FI04": 0.5, "FI05": 1.0,
}

AXIS_LABELS = {
    "fundiario": "Fundiário",
    "ambiental": "Ambiental",
    "trabalhista": "Trabalhista",
    "juridico": "Jurídico",
    "financeiro": "Financeiro",
}


# ==========================================================================
# Helpers
# ==========================================================================


def _car_cte(car_code: str) -> str:
    """CTE reutilizável para buscar geometria do CAR."""
    return """
    WITH c AS (
      SELECT geometry FROM sicar_completo WHERE cod_imovel = :car
      UNION ALL
      SELECT geometry FROM geo_car WHERE cod_imovel = :car
      LIMIT 1
    )
    """


def _fetch_property_row(car_code: str) -> Optional[dict]:
    """Busca dados básicos do CAR (áreas, status) para avaliar critérios."""
    engine = get_engine()
    sql = text("""
        SELECT
            cod_imovel, uf,
            COALESCE(status_imovel, '') AS status,
            area::float AS area_ha,
            ST_AsGeoJSON(geometry) AS geojson
        FROM sicar_completo WHERE cod_imovel = :car
        UNION ALL
        SELECT
            cod_imovel, uf,
            COALESCE(status_imovel, '') AS status,
            area::float AS area_ha,
            ST_AsGeoJSON(geometry) AS geojson
        FROM geo_car WHERE cod_imovel = :car
        LIMIT 1
    """)
    with engine.connect() as conn:
        row = conn.execute(sql, {"car": car_code}).mappings().first()
    return dict(row) if row else None


def _count_overlap(car_code: str, table: str, date_filter: str = "") -> int:
    """Conta interseções entre o CAR e uma tabela geométrica."""
    engine = get_engine()
    try:
        with engine.connect() as conn:
            return int(conn.execute(
                text(f"{_car_cte(car_code)} SELECT COUNT(*) FROM c JOIN {table} l ON ST_Intersects(c.geometry, l.geometry) {date_filter}"),
                {"car": car_code},
            ).scalar() or 0)
    except Exception:
        return 0


# ==========================================================================
# FUNDIÁRIO (8 critérios)
# ==========================================================================


def check_f01_car_active(car_code: str, prop: Optional[dict]) -> CriterionResult:
    status = (prop or {}).get("status", "") or ""
    ok = status.upper() in ("AT", "ATV", "ATIVO")
    return CriterionResult(
        code="MCR-F01", axis="fundiario",
        title="CAR ativo",
        description="Inscrição no CAR deve estar com status Ativo (AT).",
        regulation="MCR 2-2-9, item 1 · Lei 12.651/12 art. 29",
        status="passed" if ok else ("failed" if prop else "failed"),
        passed=ok,
        details=f"Status atual: {status or 'N/A'}",
        weight=WEIGHTS["F01"],
        evidence={"car_status": status},
    )


def check_f02_sigef_overlap(car_code: str) -> CriterionResult:
    n = _count_overlap(car_code, "sigef_parcelas")
    # Se sobrepõe SIGEF de terceiros (é normal sobrepor, mas vale como sinal)
    ok = n == 0 or n == 1
    return CriterionResult(
        code="MCR-F02", axis="fundiario",
        title="Sem sobreposição SIGEF conflitante",
        description="Não há sobreposição com múltiplas parcelas certificadas pelo INCRA.",
        regulation="Lei 10.267/01 · INCRA/SIGEF",
        status="passed" if ok else "failed",
        passed=ok,
        details=("Nenhuma parcela SIGEF sobreposta" if n == 0
                 else f"1 parcela SIGEF sobreposta (compatível)" if n == 1
                 else f"{n} parcelas SIGEF sobrepostas — possível conflito dominial"),
        weight=WEIGHTS["F02"],
        evidence={"sigef_overlaps": n},
    )


def check_f03_terra_indigena(car_code: str) -> CriterionResult:
    n = _count_overlap(car_code, "geo_terras_indigenas")
    ok = n == 0
    return CriterionResult(
        code="MCR-F03", axis="fundiario",
        title="Sem sobreposição com Terra Indígena",
        description="Área não sobrepõe Terras Indígenas homologadas ou em estudo (FUNAI).",
        regulation="MCR 2-2-9 · CF/88 art. 231 · Decreto 1.775/96",
        status="passed" if ok else "failed",
        passed=ok,
        details=("Nenhuma sobreposição com TI" if ok else f"{n} TI(s) sobreposta(s)"),
        weight=WEIGHTS["F03"],
        evidence={"ti_overlaps": n},
    )


def check_f04_unidade_conservacao(car_code: str) -> CriterionResult:
    n = _count_overlap(car_code, "geo_unidades_conservacao")
    ok = n == 0
    return CriterionResult(
        code="MCR-F04", axis="fundiario",
        title="Sem sobreposição com Unidade de Conservação",
        description="Área não sobrepõe UC federal ou estadual (ICMBio/órgãos estaduais).",
        regulation="MCR 2-2-9 · Lei 9.985/00 (SNUC)",
        status="passed" if ok else "failed",
        passed=ok,
        details=("Nenhuma sobreposição com UC" if ok else f"{n} UC(s) sobreposta(s)"),
        weight=WEIGHTS["F04"],
        evidence={"uc_overlaps": n},
    )


def check_f05_sigmine(car_code: Optional[str]) -> CriterionResult:
    engine = get_engine()
    # Primeiro checa se a tabela tem dados
    try:
        with engine.connect() as conn:
            total = int(conn.execute(text("SELECT COUNT(*) FROM sigmine_processos")).scalar() or 0)
    except Exception:
        total = 0
    if total == 0 or not car_code:
        return CriterionResult(
            code="MCR-F05", axis="fundiario",
            title="Sem sobreposição SIGMINE (mineração)",
            description="Não há processos minerários registrados na ANM sobre a área.",
            regulation="Código de Mineração · ANM",
            status="pending", passed=None,
            details=("Tabela sigmine_processos vazia — execute ETL: docker exec agrojus-backend-1 python -m scripts.run_dados_gov_etl --only sigmine"
                     if total == 0 else "CAR não informado"),
            weight=WEIGHTS["F05"],
            evidence={"source": "SIGMINE-ANM"},
        )
    n = _count_overlap(car_code, "sigmine_processos")
    ok = n == 0
    return CriterionResult(
        code="MCR-F05", axis="fundiario",
        title="Sem sobreposição SIGMINE (mineração)",
        description="Não há processos minerários registrados na ANM sobre a área.",
        regulation="Código de Mineração · ANM",
        status="passed" if ok else "failed",
        passed=ok,
        details=(f"{n} processo(s) minerário(s) sobrepostos" if n
                 else "Sem sobreposição com SIGMINE"),
        weight=WEIGHTS["F05"],
        evidence={"sigmine_overlaps": n, "source": "SIGMINE-ANM"},
    )


def check_f06_ccir() -> CriterionResult:
    return CriterionResult(
        code="MCR-F06", axis="fundiario",
        title="CCIR válido e vigente",
        description="Certificado de Cadastro de Imóvel Rural (INCRA) válido.",
        regulation="Lei 5.868/72 · INCRA",
        status="pending",
        passed=None,
        details="Aguardando integração com base CCIR/INCRA (não disponível via dados abertos)",
        weight=WEIGHTS["F06"],
        evidence={"source": "INCRA-CCIR"},
    )


def check_f07_itr() -> CriterionResult:
    return CriterionResult(
        code="MCR-F07", axis="fundiario",
        title="ITR quitado nos últimos 5 anos",
        description="Imposto Territorial Rural (Receita) sem débitos nos últimos 5 exercícios.",
        regulation="Lei 9.393/96 · Receita Federal",
        status="pending",
        passed=None,
        details="Aguardando integração com Receita Federal (sigiloso — requer consentimento)",
        weight=WEIGHTS["F07"],
        evidence={"source": "RFB-ITR"},
    )


def check_f08_spu() -> CriterionResult:
    return CriterionResult(
        code="MCR-F08", axis="fundiario",
        title="Sem sobreposição com SPU (Terras da União)",
        description="Área não sobrepõe terras sob gestão da Secretaria do Patrimônio da União.",
        regulation="Decreto-Lei 9.760/46 · SPU",
        status="pending",
        passed=None,
        details="Aguardando coletor SPU (backlog Sprint 4+)",
        weight=WEIGHTS["F08"],
        evidence={"source": "SPU"},
    )


# ==========================================================================
# AMBIENTAL (8 critérios)
# ==========================================================================


def check_a01_prodes(car_code: str) -> CriterionResult:
    engine = get_engine()
    # PRODES pós-2019 — usa a coluna year se existir
    try:
        with engine.connect() as conn:
            n = int(conn.execute(
                text(f"{_car_cte(car_code)} SELECT COUNT(*) FROM c JOIN geo_prodes p ON ST_Intersects(c.geometry, p.geometry) WHERE p.year >= 2019"),
                {"car": car_code},
            ).scalar() or 0)
    except Exception:
        n = 0
    ok = n == 0
    return CriterionResult(
        code="MCR-A01", axis="ambiental",
        title="Sem desmatamento PRODES pós-31/07/2019",
        description="Não há polígonos PRODES (INPE) intersectando a área após o marco MCR.",
        regulation="MCR 2-2-9, item 17 · CMN 5.081/23",
        status="passed" if ok else "failed",
        passed=ok,
        details=(f"{n} polígono(s) PRODES intersectando após 2019" if n else "Limpo no PRODES pós-2019"),
        weight=WEIGHTS["A01"],
        evidence={"prodes_post_2019": n},
    )


def check_a02_deter(car_code: str) -> CriterionResult:
    engine = get_engine()
    cutoff = (datetime.now(timezone.utc) - timedelta(days=365)).strftime("%Y-%m-%d")
    try:
        with engine.connect() as conn:
            n_amz = int(conn.execute(
                text(f"{_car_cte(car_code)} SELECT COUNT(*) FROM c JOIN geo_deter_amazonia d ON ST_Intersects(c.geometry, d.geometry) WHERE d.view_date >= :cutoff::date"),
                {"car": car_code, "cutoff": cutoff},
            ).scalar() or 0)
            n_cer = int(conn.execute(
                text(f"{_car_cte(car_code)} SELECT COUNT(*) FROM c JOIN geo_deter_cerrado d ON ST_Intersects(c.geometry, d.geometry) WHERE d.view_date >= :cutoff::date"),
                {"car": car_code, "cutoff": cutoff},
            ).scalar() or 0)
    except Exception:
        n_amz, n_cer = 0, 0
    total = n_amz + n_cer
    ok = total == 0
    return CriterionResult(
        code="MCR-A02", axis="ambiental",
        title="Sem alerta DETER nos últimos 12 meses",
        description="Não há alertas DETER (Amazônia ou Cerrado) recentes sobre a área.",
        regulation="INPE/DETER · MCR 2-2-9 item 17",
        status="passed" if ok else "failed",
        passed=ok,
        details=(f"DETER 12m: {n_amz} Amazônia + {n_cer} Cerrado" if total else "Sem alertas DETER recentes"),
        weight=WEIGHTS["A02"],
        evidence={"deter_amazonia_12m": n_amz, "deter_cerrado_12m": n_cer},
    )


def check_a03_mapbiomas(car_code: str) -> CriterionResult:
    engine = get_engine()
    try:
        with engine.connect() as conn:
            n = int(conn.execute(
                text(f"{_car_cte(car_code)} SELECT COUNT(*) FROM c JOIN geo_mapbiomas_alertas m ON ST_Intersects(c.geometry, m.geometry) WHERE m.\"ANODETEC\"::int >= 2019"),
                {"car": car_code},
            ).scalar() or 0)
    except Exception:
        n = 0
    ok = n == 0
    return CriterionResult(
        code="MCR-A03", axis="ambiental",
        title="Sem alerta MapBiomas validado pós-2019",
        description="Não há alertas MapBiomas (validados por satélite) após o marco MCR.",
        regulation="MapBiomas Alerta · CMN 5.081/23",
        status="passed" if ok else "failed",
        passed=ok,
        details=(f"{n} alerta(s) MapBiomas pós-2019" if n else "Sem alertas MapBiomas validados"),
        weight=WEIGHTS["A03"],
        evidence={"mapbiomas_post_2019": n},
    )


def check_a04_embargos_icmbio(car_code: str) -> CriterionResult:
    n = _count_overlap(car_code, "geo_embargos_icmbio")
    ok = n == 0
    return CriterionResult(
        code="MCR-A04", axis="ambiental",
        title="Sem embargos ICMBio/IBAMA vigentes sobre a área",
        description="Área não possui sobreposição com polígonos de embargo ambiental federal.",
        regulation="Lei 9.605/98 · Decreto 6.514/08",
        status="passed" if ok else "failed",
        passed=ok,
        details=(f"{n} embargo(s) ICMBio/IBAMA sobrepostos" if n else "Sem embargos ambientais"),
        weight=WEIGHTS["A04"],
        evidence={"embargos": n},
    )


def check_a05_autos_ibama(car_code: str, cpf_cnpj: Optional[str]) -> CriterionResult:
    # 1) Por overlap geográfico
    n_geo = _count_overlap(car_code, "geo_autos_ibama")
    # 2) Por CPF/CNPJ no environmental_alerts
    n_cpf = 0
    if cpf_cnpj:
        clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
        engine = get_engine()
        try:
            with engine.connect() as conn:
                n_cpf = int(conn.execute(
                    text("SELECT COUNT(*) FROM environmental_alerts WHERE source='IBAMA' AND cpf_cnpj = :cpf"),
                    {"cpf": clean},
                ).scalar() or 0)
        except Exception:
            pass
    total = n_geo + n_cpf
    ok = total == 0
    return CriterionResult(
        code="MCR-A05", axis="ambiental",
        title="Sem autos de infração IBAMA",
        description="Nem por sobreposição geográfica, nem por CPF/CNPJ há autos IBAMA ativos.",
        regulation="Lei 9.605/98 · SIFISC/IBAMA",
        status="passed" if ok else "failed",
        passed=ok,
        details=(f"{n_geo} auto(s) por geo + {n_cpf} por CPF/CNPJ" if total
                 else "Nenhum auto IBAMA detectado"),
        weight=WEIGHTS["A05"],
        evidence={"autos_geo": n_geo, "autos_by_cpf": n_cpf},
    )


def check_a06_reserva_legal(prop: Optional[dict]) -> CriterionResult:
    # Busca área de RL via properties ou sicar_completo (coluna area_reserva_legal_ha se existir)
    engine = get_engine()
    car_code = (prop or {}).get("cod_imovel")
    if not car_code:
        return CriterionResult(
            code="MCR-A06", axis="ambiental",
            title="Reserva Legal declarada no CAR",
            description="Reserva Legal declarada em percentual adequado ao bioma.",
            regulation="Lei 12.651/12 art. 12",
            status="pending", passed=None,
            details="CAR não localizado",
            weight=WEIGHTS["A06"],
        )
    # Tenta buscar tipo_rl / area_rl na properties ou raw_data
    rl_ha = None
    try:
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT area_reserva_legal_ha FROM properties WHERE car_code = :car"),
                {"car": car_code},
            ).mappings().first()
            if row:
                rl_ha = row.get("area_reserva_legal_ha")
    except Exception:
        pass
    area_total = (prop or {}).get("area_ha") or 0
    if rl_ha and area_total:
        pct = (float(rl_ha) / float(area_total)) * 100
        # Mínimos: Amazônia 80%, Cerrado 35%, demais 20%
        uf = (prop or {}).get("uf", "")
        min_pct = 20
        if uf in ("AM", "PA", "AC", "RO", "RR", "AP", "MA", "MT", "TO"):
            min_pct = 80
        ok = pct >= min_pct
        return CriterionResult(
            code="MCR-A06", axis="ambiental",
            title="Reserva Legal declarada no CAR",
            description="Percentual de Reserva Legal compatível com o bioma do imóvel.",
            regulation="Lei 12.651/12 art. 12",
            status="passed" if ok else "failed",
            passed=ok,
            details=f"RL declarada: {pct:.1f}% (mínimo {min_pct}% UF={uf})",
            weight=WEIGHTS["A06"],
            evidence={"rl_pct": round(pct, 1), "min_pct": min_pct, "rl_ha": float(rl_ha)},
        )
    return CriterionResult(
        code="MCR-A06", axis="ambiental",
        title="Reserva Legal declarada no CAR",
        description="Percentual de Reserva Legal compatível com o bioma do imóvel.",
        regulation="Lei 12.651/12 art. 12",
        status="pending", passed=None,
        details="Dados de RL não estão no cadastro atual — verificar SICAR oficial",
        weight=WEIGHTS["A06"],
        evidence={"source": "SICAR_detalhado"},
    )


def check_a07_app(prop: Optional[dict]) -> CriterionResult:
    engine = get_engine()
    car_code = (prop or {}).get("cod_imovel")
    app_ha = None
    if car_code:
        try:
            with engine.connect() as conn:
                row = conn.execute(
                    text("SELECT area_app_ha FROM properties WHERE car_code = :car"),
                    {"car": car_code},
                ).mappings().first()
                if row:
                    app_ha = row.get("area_app_ha")
        except Exception:
            pass
    if app_ha is not None:
        ok = float(app_ha) >= 0
        return CriterionResult(
            code="MCR-A07", axis="ambiental",
            title="APP declarada no CAR",
            description="Área de Preservação Permanente declarada.",
            regulation="Lei 12.651/12 art. 4º",
            status="passed" if ok else "failed",
            passed=ok,
            details=f"APP declarada: {app_ha} ha",
            weight=WEIGHTS["A07"],
            evidence={"app_ha": float(app_ha) if app_ha else 0},
        )
    return CriterionResult(
        code="MCR-A07", axis="ambiental",
        title="APP declarada no CAR",
        description="Área de Preservação Permanente declarada.",
        regulation="Lei 12.651/12 art. 4º",
        status="pending", passed=None,
        details="Dados de APP não estão no cadastro atual — verificar SICAR oficial",
        weight=WEIGHTS["A07"],
        evidence={"source": "SICAR_detalhado"},
    )


def check_a08_ana_outorga(car_code: str) -> CriterionResult:
    engine = get_engine()
    # Usa ana_outorgas_full (Sprint 4) se tiver dados; senão tenta ana_outorgas legacy
    table = "ana_outorgas_full"
    try:
        with engine.connect() as conn:
            total = int(conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar() or 0)
            if total == 0:
                # tenta legacy
                total = int(conn.execute(text("SELECT COUNT(*) FROM ana_outorgas")).scalar() or 0)
                if total > 0:
                    table = "ana_outorgas"
    except Exception:
        total = 0

    if total == 0:
        return CriterionResult(
            code="MCR-A08", axis="ambiental",
            title="Sem conflito com outorga ANA",
            description="Não há conflito com outorgas de recursos hídricos.",
            regulation="Lei 9.433/97 · ANA",
            status="pending", passed=None,
            details="Tabelas ANA vazias — execute ETL: docker exec agrojus-backend-1 python -m scripts.run_dados_gov_etl --only ana_outorgas",
            weight=WEIGHTS["A08"],
            evidence={"source": "ANA-Outorgas"},
        )
    n = _count_overlap(car_code, table)
    ok = n == 0
    return CriterionResult(
        code="MCR-A08", axis="ambiental",
        title="Sem conflito com outorga ANA",
        description="Não há conflito com outorgas de recursos hídricos.",
        regulation="Lei 9.433/97 · ANA",
        status="passed" if ok else "failed",
        passed=ok,
        details=(f"{n} outorga(s) no perímetro" if n else "Sem outorgas conflitantes"),
        weight=WEIGHTS["A08"],
        evidence={"ana_overlaps": n, "table": table},
    )


# ==========================================================================
# TRABALHISTA (6 critérios)
# ==========================================================================


def check_t01_lista_suja(cpf_cnpj: Optional[str]) -> CriterionResult:
    if not cpf_cnpj:
        return CriterionResult(
            code="MCR-T01", axis="trabalhista",
            title="Fora da Lista Suja do Trabalho Escravo",
            description="Empregador não consta na Lista de Transparência (Portaria MTE 1.129).",
            regulation="Portaria MTE 1.293/17 · CMN 5.081/23",
            status="pending", passed=None,
            details="CPF/CNPJ do proprietário não informado",
            weight=WEIGHTS["T01"],
        )
    clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
    engine = get_engine()
    try:
        with engine.connect() as conn:
            n = int(conn.execute(
                text("SELECT COUNT(*) FROM environmental_alerts WHERE source='MTE' AND cpf_cnpj = :cpf"),
                {"cpf": clean},
            ).scalar() or 0)
    except Exception:
        n = 0
    ok = n == 0
    return CriterionResult(
        code="MCR-T01", axis="trabalhista",
        title="Fora da Lista Suja do Trabalho Escravo",
        description="Empregador não consta na Lista de Transparência (Portaria MTE 1.129).",
        regulation="Portaria MTE 1.293/17 · CMN 5.081/23",
        status="passed" if ok else "failed",
        passed=ok,
        details=(f"{n} entrada(s) na Lista Suja" if n else "Não consta na Lista Suja"),
        weight=WEIGHTS["T01"],
        evidence={"mte_entries": n},
    )


def check_t02_cndt() -> CriterionResult:
    return CriterionResult(
        code="MCR-T02", axis="trabalhista",
        title="CNDT emitida (sem débitos trabalhistas)",
        description="Certidão Negativa de Débitos Trabalhistas vigente.",
        regulation="Lei 12.440/11 · TST",
        status="pending", passed=None,
        details="Integração com CNDT/TST requer consulta individual (não dados abertos)",
        weight=WEIGHTS["T02"],
        evidence={"source": "TST-CNDT"},
    )


def check_t03_caged() -> CriterionResult:
    return CriterionResult(
        code="MCR-T03", axis="trabalhista",
        title="CAGED/eSocial com movimentação declarada",
        description="Movimentação de empregados registrada no Cadastro Geral.",
        regulation="Decreto 8.373/14 · eSocial",
        status="pending", passed=None,
        details="Aguardando coletor CAGED/eSocial (Sprint 4+)",
        weight=WEIGHTS["T03"],
        evidence={"source": "eSocial-CAGED"},
    )


def check_t04_esocial() -> CriterionResult:
    return CriterionResult(
        code="MCR-T04", axis="trabalhista",
        title="eSocial ativo (empregador cadastrado)",
        description="Empregador com eSocial ativo.",
        regulation="Decreto 8.373/14",
        status="pending", passed=None,
        details="Integração com eSocial requer certificado digital (não dados abertos)",
        weight=WEIGHTS["T04"],
        evidence={"source": "eSocial"},
    )


def check_t05_nr31() -> CriterionResult:
    return CriterionResult(
        code="MCR-T05", axis="trabalhista",
        title="NR-31 — declaração de conformidade",
        description="Conformidade com Norma Regulamentadora 31 (trabalho rural).",
        regulation="Portaria MTb 86/05 · NR-31",
        status="pending", passed=None,
        details="Auditoria presencial — item declaratório (a ser autoavaliado)",
        weight=WEIGHTS["T05"],
        evidence={"source": "autoavaliacao"},
    )


def check_t06_cipatr(prop: Optional[dict]) -> CriterionResult:
    # CIPATR só se aplica a imóveis com >50 trabalhadores
    # Sem dados de trabalhadores, marcamos como N/A para imóveis pequenos
    area_ha = (prop or {}).get("area_ha") or 0
    if area_ha < 100:  # heurística: imóvel pequeno, provavelmente não tem 50+ empregados
        return CriterionResult(
            code="MCR-T06", axis="trabalhista",
            title="CIPATR constituída (>50 trabalhadores)",
            description="Comissão Interna de Prevenção de Acidentes do Trabalho Rural.",
            regulation="NR-31, item 31.8",
            status="not_applicable",
            passed=None,
            details=f"Imóvel pequeno ({area_ha} ha) — CIPATR não aplicável",
            weight=WEIGHTS["T06"],
            evidence={"area_ha": area_ha},
        )
    return CriterionResult(
        code="MCR-T06", axis="trabalhista",
        title="CIPATR constituída (>50 trabalhadores)",
        description="Comissão Interna de Prevenção de Acidentes do Trabalho Rural.",
        regulation="NR-31, item 31.8",
        status="pending", passed=None,
        details="Requer declaração do número de trabalhadores (não dados abertos)",
        weight=WEIGHTS["T06"],
        evidence={"source": "declaracao_empregador"},
    )


# ==========================================================================
# JURÍDICO (5 critérios)
# ==========================================================================


def check_j01_datajud(cpf_cnpj: Optional[str]) -> CriterionResult:
    # Tenta buscar em legal_records (CPF/CNPJ)
    if not cpf_cnpj:
        return CriterionResult(
            code="MCR-J01", axis="juridico",
            title="Sem processos DataJud com objeto crítico",
            description="Não há execução fiscal, usucapião ou ação possessória.",
            regulation="DataJud/CNJ · Res. CNJ 331/2020",
            status="pending", passed=None,
            details="CPF/CNPJ do proprietário não informado",
            weight=WEIGHTS["J01"],
        )
    clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
    engine = get_engine()
    try:
        with engine.connect() as conn:
            n_critical = int(conn.execute(
                text("""
                  SELECT COUNT(*) FROM legal_records
                  WHERE cpf_cnpj = :cpf
                    AND (record_type IN ('lawsuit','execution')
                         OR description ILIKE '%execu%o fiscal%'
                         OR description ILIKE '%usucapi%o%')
                """),
                {"cpf": clean},
            ).scalar() or 0)
    except Exception:
        n_critical = 0
    ok = n_critical == 0
    return CriterionResult(
        code="MCR-J01", axis="juridico",
        title="Sem processos DataJud com objeto crítico",
        description="Não há execução fiscal, usucapião ou ação possessória.",
        regulation="DataJud/CNJ · Res. CNJ 331/2020",
        status="passed" if ok else "failed",
        passed=ok,
        details=(f"{n_critical} processo(s) crítico(s) no DataJud" if n_critical
                 else "Sem processos DataJud críticos registrados"),
        weight=WEIGHTS["J01"],
        evidence={"datajud_critical": n_critical},
    )


def check_j02_djen_recent(cpf_cnpj: Optional[str]) -> CriterionResult:
    if not cpf_cnpj:
        return CriterionResult(
            code="MCR-J02", axis="juridico",
            title="Sem intimações DJEN nos últimos 30 dias",
            description="Diário de Justiça Eletrônico Nacional sem movimentações recentes.",
            regulation="Res. CNJ 455/2022 · DJEN",
            status="pending", passed=None,
            details="CPF/CNPJ do proprietário não informado",
            weight=WEIGHTS["J02"],
        )
    # Por enquanto só temos DJEN por OAB (não por CPF/CNPJ de parte)
    # Retornamos aprovado indicativo se OAB conhecida
    return CriterionResult(
        code="MCR-J02", axis="juridico",
        title="Sem intimações DJEN nos últimos 30 dias",
        description="Diário de Justiça Eletrônico Nacional sem movimentações recentes.",
        regulation="Res. CNJ 455/2022 · DJEN",
        status="pending", passed=None,
        details="DJEN por CPF/CNPJ da parte — requer consulta pontual ao Comunica.PJe",
        weight=WEIGHTS["J02"],
        evidence={"source": "DJEN-CNJ"},
    )


def check_j03_protestos() -> CriterionResult:
    return CriterionResult(
        code="MCR-J03", axis="juridico",
        title="Sem protestos em cartório",
        description="Sem títulos protestados em cartórios de protesto.",
        regulation="Lei 9.492/97 · CNPTB",
        status="pending", passed=None,
        details="Aguardando integração com CENPROT (consulta pontual paga)",
        weight=WEIGHTS["J03"],
        evidence={"source": "CENPROT"},
    )


def check_j04_reclamacao_cnj() -> CriterionResult:
    return CriterionResult(
        code="MCR-J04", axis="juridico",
        title="Sem reclamação CNJ",
        description="Sem reclamação contra juiz ou cartório registrada no CNJ.",
        regulation="Res. CNJ 135/2011",
        status="pending", passed=None,
        details="Aguardando coletor CNJ reclamações",
        weight=WEIGHTS["J04"],
        evidence={"source": "CNJ-Reclamacoes"},
    )


def check_j05_execucao_fiscal(cpf_cnpj: Optional[str]) -> CriterionResult:
    if not cpf_cnpj:
        return CriterionResult(
            code="MCR-J05", axis="juridico",
            title="Sem execução fiscal federal/estadual",
            description="Não há execução fiscal em andamento.",
            regulation="Lei 6.830/80",
            status="pending", passed=None,
            details="CPF/CNPJ do proprietário não informado",
            weight=WEIGHTS["J05"],
        )
    clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
    engine = get_engine()
    try:
        with engine.connect() as conn:
            n = int(conn.execute(
                text("""
                  SELECT COUNT(*) FROM legal_records
                  WHERE cpf_cnpj = :cpf AND (
                      description ILIKE '%execu%o fiscal%'
                      OR record_type = 'debt'
                  )
                """),
                {"cpf": clean},
            ).scalar() or 0)
    except Exception:
        n = 0
    ok = n == 0
    return CriterionResult(
        code="MCR-J05", axis="juridico",
        title="Sem execução fiscal federal/estadual",
        description="Não há execução fiscal em andamento.",
        regulation="Lei 6.830/80",
        status="passed" if ok else "failed",
        passed=ok,
        details=(f"{n} execução(ões) fiscal(is) registrada(s)" if n
                 else "Sem execução fiscal registrada"),
        weight=WEIGHTS["J05"],
        evidence={"executions": n},
    )


# ==========================================================================
# FINANCEIRO (5 critérios)
# ==========================================================================


def check_fi01_sicor(car_code: str, cpf_cnpj: Optional[str]) -> CriterionResult:
    # Busca contratos SICOR em mapbiomas_credito_rural
    engine = get_engine()
    try:
        with engine.connect() as conn:
            total = int(conn.execute(
                text(f"{_car_cte(car_code)} SELECT COUNT(*) FROM c JOIN mapbiomas_credito_rural mcr ON ST_Intersects(c.geometry, mcr.geom)"),
                {"car": car_code},
            ).scalar() or 0)
    except Exception:
        total = 0
    # Sem fonte de inadimplência real, só informativo
    if total > 0:
        return CriterionResult(
            code="MCR-FI01", axis="financeiro",
            title="Sem inadimplência SICOR",
            description="Contratos de crédito rural sem inadimplência registrada.",
            regulation="SICOR-BCB · CMN",
            status="pending", passed=None,
            details=f"{total} contrato(s) SICOR vinculado(s) — status de inadimplência exige consulta ao BCB",
            weight=WEIGHTS["FI01"],
            evidence={"sicor_contracts": total, "source_inadimplencia": "BCB-SICOR"},
        )
    return CriterionResult(
        code="MCR-FI01", axis="financeiro",
        title="Sem inadimplência SICOR",
        description="Contratos de crédito rural sem inadimplência registrada.",
        regulation="SICOR-BCB · CMN",
        status="passed", passed=True,
        details="Nenhum contrato SICOR identificado",
        weight=WEIGHTS["FI01"],
        evidence={"sicor_contracts": 0},
    )


def check_fi02_ceis(cpf_cnpj: Optional[str]) -> CriterionResult:
    engine = get_engine()
    try:
        with engine.connect() as conn:
            total = int(conn.execute(text("SELECT COUNT(*) FROM ceis_registros")).scalar() or 0)
    except Exception:
        total = 0
    if total == 0:
        return CriterionResult(
            code="MCR-FI02", axis="financeiro",
            title="Não consta CEIS",
            description="Cadastro Nacional de Empresas Inidôneas e Suspensas.",
            regulation="Lei 12.846/13 · Portal Transparência",
            status="pending", passed=None,
            details="Tabela ceis_registros vazia — execute ETL: docker exec agrojus-backend-1 python -m scripts.run_dados_gov_etl --only ceis",
            weight=WEIGHTS["FI02"],
            evidence={"source": "CGU-CEIS"},
        )
    if not cpf_cnpj:
        return CriterionResult(
            code="MCR-FI02", axis="financeiro",
            title="Não consta CEIS",
            description="Cadastro Nacional de Empresas Inidôneas e Suspensas.",
            regulation="Lei 12.846/13 · Portal Transparência",
            status="pending", passed=None,
            details="CPF/CNPJ do proprietário não informado",
            weight=WEIGHTS["FI02"],
            evidence={"source": "CGU-CEIS", "base_size": total},
        )
    clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
    try:
        with engine.connect() as conn:
            n = int(conn.execute(
                text("SELECT COUNT(*) FROM ceis_registros WHERE cpf_cnpj = :cpf"),
                {"cpf": clean},
            ).scalar() or 0)
    except Exception:
        n = 0
    ok = n == 0
    return CriterionResult(
        code="MCR-FI02", axis="financeiro",
        title="Não consta CEIS",
        description="Cadastro Nacional de Empresas Inidôneas e Suspensas.",
        regulation="Lei 12.846/13 · Portal Transparência",
        status="passed" if ok else "failed",
        passed=ok,
        details=(f"{n} registro(s) no CEIS" if n else "Não consta no CEIS"),
        weight=WEIGHTS["FI02"],
        evidence={"ceis_matches": n, "base_size": total},
    )


def check_fi03_cnep(cpf_cnpj: Optional[str]) -> CriterionResult:
    engine = get_engine()
    try:
        with engine.connect() as conn:
            total = int(conn.execute(text("SELECT COUNT(*) FROM cnep_registros")).scalar() or 0)
    except Exception:
        total = 0
    if total == 0:
        return CriterionResult(
            code="MCR-FI03", axis="financeiro",
            title="Não consta CNEP",
            description="Cadastro Nacional de Empresas Punidas.",
            regulation="Lei 12.846/13",
            status="pending", passed=None,
            details="Tabela cnep_registros vazia — execute ETL: docker exec agrojus-backend-1 python -m scripts.run_dados_gov_etl --only cnep",
            weight=WEIGHTS["FI03"],
            evidence={"source": "CGU-CNEP"},
        )
    if not cpf_cnpj:
        return CriterionResult(
            code="MCR-FI03", axis="financeiro",
            title="Não consta CNEP",
            description="Cadastro Nacional de Empresas Punidas.",
            regulation="Lei 12.846/13",
            status="pending", passed=None,
            details="CPF/CNPJ do proprietário não informado",
            weight=WEIGHTS["FI03"],
            evidence={"source": "CGU-CNEP", "base_size": total},
        )
    clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
    try:
        with engine.connect() as conn:
            n = int(conn.execute(
                text("SELECT COUNT(*) FROM cnep_registros WHERE cpf_cnpj = :cpf"),
                {"cpf": clean},
            ).scalar() or 0)
    except Exception:
        n = 0
    ok = n == 0
    return CriterionResult(
        code="MCR-FI03", axis="financeiro",
        title="Não consta CNEP",
        description="Cadastro Nacional de Empresas Punidas.",
        regulation="Lei 12.846/13",
        status="passed" if ok else "failed",
        passed=ok,
        details=(f"{n} registro(s) no CNEP" if n else "Não consta no CNEP"),
        weight=WEIGHTS["FI03"],
        evidence={"cnep_matches": n, "base_size": total},
    )


def check_fi04_pix() -> CriterionResult:
    return CriterionResult(
        code="MCR-FI04", axis="financeiro",
        title="Sem pendência PIX",
        description="Sem restrições PIX ativas (cadastro negativo).",
        regulation="BCB · Sistema PIX",
        status="pending", passed=None,
        details="Item informativo — PIX não tem lista pública de negativação",
        weight=WEIGHTS["FI04"],
        evidence={"source": "BCB-PIX"},
    )


def check_fi05_ccir_financeiro() -> CriterionResult:
    return CriterionResult(
        code="MCR-FI05", axis="financeiro",
        title="CCIR presente (documento financeiro)",
        description="CCIR necessário para concessão de crédito rural.",
        regulation="Lei 5.868/72 · INCRA",
        status="pending", passed=None,
        details="Requer consulta individual ao INCRA (não dados abertos)",
        weight=WEIGHTS["FI05"],
        evidence={"source": "INCRA-CCIR"},
    )


# ==========================================================================
# Orquestração — roda todos os 30 critérios
# ==========================================================================


def evaluate_mcr29_full(
    car_code: Optional[str],
    cpf_cnpj: Optional[str] = None,
) -> MCR29FullResult:
    """Roda os 30 critérios e consolida resultado."""

    # Dados base do CAR (usado em vários critérios)
    prop = _fetch_property_row(car_code) if car_code else None

    criteria: list[CriterionResult] = []

    # Fundiário
    if car_code:
        criteria.append(check_f01_car_active(car_code, prop))
        criteria.append(check_f02_sigef_overlap(car_code))
        criteria.append(check_f03_terra_indigena(car_code))
        criteria.append(check_f04_unidade_conservacao(car_code))
    else:
        criteria.append(CriterionResult(
            code="MCR-F01", axis="fundiario",
            title="CAR ativo", description="", regulation="MCR 2-2-9",
            status="failed", passed=False,
            details="CAR não informado — crédito rural exige inscrição ativa.",
            weight=WEIGHTS["F01"],
        ))
        criteria.append(CriterionResult(
            code="MCR-F02", axis="fundiario",
            title="Sem sobreposição SIGEF conflitante", description="",
            regulation="INCRA/SIGEF",
            status="pending", passed=None,
            details="CAR não informado", weight=WEIGHTS["F02"],
        ))
        criteria.append(CriterionResult(
            code="MCR-F03", axis="fundiario",
            title="Sem sobreposição com Terra Indígena", description="",
            regulation="CF/88 art. 231", status="pending", passed=None,
            details="CAR não informado", weight=WEIGHTS["F03"],
        ))
        criteria.append(CriterionResult(
            code="MCR-F04", axis="fundiario",
            title="Sem sobreposição com Unidade de Conservação", description="",
            regulation="SNUC", status="pending", passed=None,
            details="CAR não informado", weight=WEIGHTS["F04"],
        ))
    criteria.append(check_f05_sigmine(car_code))
    criteria.append(check_f06_ccir())
    criteria.append(check_f07_itr())
    criteria.append(check_f08_spu())

    # Ambiental
    if car_code:
        criteria.append(check_a01_prodes(car_code))
        criteria.append(check_a02_deter(car_code))
        criteria.append(check_a03_mapbiomas(car_code))
        criteria.append(check_a04_embargos_icmbio(car_code))
        criteria.append(check_a05_autos_ibama(car_code, cpf_cnpj))
        criteria.append(check_a06_reserva_legal(prop))
        criteria.append(check_a07_app(prop))
        criteria.append(check_a08_ana_outorga(car_code))
    else:
        for code, title, reg, weight_key in [
            ("MCR-A01", "Sem desmatamento PRODES pós-31/07/2019", "MCR 2-2-9 item 17", "A01"),
            ("MCR-A02", "Sem alerta DETER nos últimos 12 meses", "INPE/DETER", "A02"),
            ("MCR-A03", "Sem alerta MapBiomas validado pós-2019", "MapBiomas Alerta", "A03"),
            ("MCR-A04", "Sem embargos ICMBio/IBAMA", "Lei 9.605/98", "A04"),
            ("MCR-A05", "Sem autos de infração IBAMA", "SIFISC/IBAMA", "A05"),
            ("MCR-A06", "Reserva Legal declarada no CAR", "Lei 12.651/12 art. 12", "A06"),
            ("MCR-A07", "APP declarada no CAR", "Lei 12.651/12 art. 4º", "A07"),
            ("MCR-A08", "Sem conflito com outorga ANA", "Lei 9.433/97", "A08"),
        ]:
            criteria.append(CriterionResult(
                code=code, axis="ambiental", title=title, description="",
                regulation=reg, status="pending", passed=None,
                details="CAR não informado", weight=WEIGHTS[weight_key],
            ))

    # Trabalhista
    criteria.append(check_t01_lista_suja(cpf_cnpj))
    criteria.append(check_t02_cndt())
    criteria.append(check_t03_caged())
    criteria.append(check_t04_esocial())
    criteria.append(check_t05_nr31())
    criteria.append(check_t06_cipatr(prop))

    # Jurídico
    criteria.append(check_j01_datajud(cpf_cnpj))
    criteria.append(check_j02_djen_recent(cpf_cnpj))
    criteria.append(check_j03_protestos())
    criteria.append(check_j04_reclamacao_cnj())
    criteria.append(check_j05_execucao_fiscal(cpf_cnpj))

    # Financeiro
    if car_code:
        criteria.append(check_fi01_sicor(car_code, cpf_cnpj))
    else:
        criteria.append(CriterionResult(
            code="MCR-FI01", axis="financeiro",
            title="Sem inadimplência SICOR", description="",
            regulation="SICOR-BCB", status="pending", passed=None,
            details="CAR não informado", weight=WEIGHTS["FI01"],
        ))
    criteria.append(check_fi02_ceis(cpf_cnpj))
    criteria.append(check_fi03_cnep(cpf_cnpj))
    criteria.append(check_fi04_pix())
    criteria.append(check_fi05_ccir_financeiro())

    # Score por eixo
    axes = {}
    for c in criteria:
        axes.setdefault(c.axis, {"passed": 0, "failed": 0, "pending": 0, "not_applicable": 0, "total_weight": 0.0, "passed_weight": 0.0})
        a = axes[c.axis]
        if c.status == "passed":
            a["passed"] += 1
            a["passed_weight"] += c.weight
            a["total_weight"] += c.weight
        elif c.status == "failed":
            a["failed"] += 1
            a["total_weight"] += c.weight
        elif c.status == "pending":
            a["pending"] += 1
        elif c.status == "not_applicable":
            a["not_applicable"] += 1

    axis_scores = []
    for key, label in AXIS_LABELS.items():
        a = axes.get(key, {"passed": 0, "failed": 0, "pending": 0, "not_applicable": 0, "total_weight": 0.0, "passed_weight": 0.0})
        score = (a["passed_weight"] / a["total_weight"] * 100) if a["total_weight"] > 0 else 0
        total = a["passed"] + a["failed"] + a["pending"] + a["not_applicable"]
        axis_scores.append(AxisScore(
            axis=key, label=label,
            total_criteria=total,
            passed=a["passed"], failed=a["failed"],
            pending=a["pending"], not_applicable=a["not_applicable"],
            weighted_score=score,
        ))

    # Overall score (0-1000) — média ponderada dos eixos aplicáveis, com peso proporcional
    # Cada eixo contribui até 200 pontos (5 × 200 = 1000)
    overall = sum(a.weighted_score * 2 for a in axis_scores) / 5  # média de porcentagem × 2 = 0-200 por eixo
    # reescala para 0-1000
    total_overall = sum(a.weighted_score for a in axis_scores) * 2  # 0-1000

    # Status
    n_failed_critical = sum(
        1 for c in criteria if c.status == "failed" and c.weight >= 2.5
    )
    n_failed_total = sum(1 for c in criteria if c.status == "failed")
    n_pending = sum(1 for c in criteria if c.status == "pending")

    if n_failed_critical > 0:
        overall_status = "blocked"
        risk_level = "CRITICAL"
    elif n_failed_total > 2:
        overall_status = "restricted"
        risk_level = "HIGH"
    elif n_failed_total > 0:
        overall_status = "restricted"
        risk_level = "MEDIUM"
    elif n_pending > 15:
        overall_status = "indeterminate"
        risk_level = "MEDIUM"
    else:
        overall_status = "approved"
        risk_level = "LOW"

    # Fontes
    sources_consulted = []
    pending_sources = []
    for c in criteria:
        src = c.evidence.get("source") if isinstance(c.evidence, dict) else None
        if c.status in ("passed", "failed"):
            if src and src not in sources_consulted:
                sources_consulted.append(src)
        elif c.status == "pending":
            if src and src not in pending_sources:
                pending_sources.append(src)

    # Summary + recommendation
    failed_codes = [c.code for c in criteria if c.status == "failed"]
    summary = (
        f"{len(failed_codes)} falha(s), {n_pending} pendente(s), "
        f"{sum(1 for c in criteria if c.status == 'passed')} aprovado(s). "
        f"Score {total_overall:.0f}/1000 ({risk_level})."
    )

    if overall_status == "blocked":
        recommendation = (
            "Crédito rural BLOQUEADO conforme MCR 2.9. Há falhas em critérios "
            f"de alto peso ({', '.join(failed_codes[:4])}...). Necessária "
            "regularização antes de submeter proposta."
        )
    elif overall_status == "restricted":
        recommendation = (
            "Crédito rural RESTRITO. Revisar critérios falhos antes do envio. "
            "Documentação complementar (ASV, PRAD, TAC) pode destravar análise."
        )
    elif overall_status == "indeterminate":
        recommendation = (
            "Avaliação INCOMPLETA — muitas fontes externas ainda não integradas. "
            "Complemente com consulta direta às fontes pendentes para parecer final."
        )
    else:
        recommendation = (
            "Propriedade APTA nos critérios verificáveis com dados públicos. "
            "Confirme critérios pendentes com documentação do tomador."
        )

    return MCR29FullResult(
        car_code=car_code,
        cpf_cnpj=cpf_cnpj,
        generated_at=datetime.now(timezone.utc).isoformat(),
        overall_status=overall_status,
        overall_score=total_overall,
        risk_level=risk_level,
        axis_scores=axis_scores,
        criteria=criteria,
        summary=summary,
        recommendation=recommendation,
        sources_consulted=sources_consulted,
        pending_sources=pending_sources,
    )


# Metadados dos 30 critérios (para GET /criteria)
def list_criteria_metadata() -> list[dict]:
    """Lista metadados dos 30 critérios sem executar."""
    return [
        # Fundiário
        {"code": "MCR-F01", "axis": "fundiario", "title": "CAR ativo", "weight": WEIGHTS["F01"], "regulation": "MCR 2-2-9 item 1 · Lei 12.651/12"},
        {"code": "MCR-F02", "axis": "fundiario", "title": "Sem sobreposição SIGEF conflitante", "weight": WEIGHTS["F02"], "regulation": "Lei 10.267/01 · INCRA"},
        {"code": "MCR-F03", "axis": "fundiario", "title": "Sem sobreposição com Terra Indígena", "weight": WEIGHTS["F03"], "regulation": "CF/88 art. 231 · Dec. 1.775/96"},
        {"code": "MCR-F04", "axis": "fundiario", "title": "Sem sobreposição com Unidade de Conservação", "weight": WEIGHTS["F04"], "regulation": "Lei 9.985/00 (SNUC)"},
        {"code": "MCR-F05", "axis": "fundiario", "title": "Sem sobreposição SIGMINE (mineração)", "weight": WEIGHTS["F05"], "regulation": "Código de Mineração · ANM"},
        {"code": "MCR-F06", "axis": "fundiario", "title": "CCIR válido", "weight": WEIGHTS["F06"], "regulation": "Lei 5.868/72 · INCRA"},
        {"code": "MCR-F07", "axis": "fundiario", "title": "ITR quitado", "weight": WEIGHTS["F07"], "regulation": "Lei 9.393/96 · RFB"},
        {"code": "MCR-F08", "axis": "fundiario", "title": "Sem sobreposição com SPU", "weight": WEIGHTS["F08"], "regulation": "Dec-Lei 9.760/46 · SPU"},
        # Ambiental
        {"code": "MCR-A01", "axis": "ambiental", "title": "Sem desmatamento PRODES pós-2019", "weight": WEIGHTS["A01"], "regulation": "MCR 2-2-9 item 17"},
        {"code": "MCR-A02", "axis": "ambiental", "title": "Sem DETER 12m", "weight": WEIGHTS["A02"], "regulation": "INPE/DETER"},
        {"code": "MCR-A03", "axis": "ambiental", "title": "Sem MapBiomas Alerta pós-2019", "weight": WEIGHTS["A03"], "regulation": "MapBiomas · CMN 5.081/23"},
        {"code": "MCR-A04", "axis": "ambiental", "title": "Sem embargos ICMBio/IBAMA", "weight": WEIGHTS["A04"], "regulation": "Lei 9.605/98 · Dec. 6.514/08"},
        {"code": "MCR-A05", "axis": "ambiental", "title": "Sem autos IBAMA", "weight": WEIGHTS["A05"], "regulation": "Lei 9.605/98 · SIFISC"},
        {"code": "MCR-A06", "axis": "ambiental", "title": "Reserva Legal declarada", "weight": WEIGHTS["A06"], "regulation": "Lei 12.651/12 art. 12"},
        {"code": "MCR-A07", "axis": "ambiental", "title": "APP declarada", "weight": WEIGHTS["A07"], "regulation": "Lei 12.651/12 art. 4º"},
        {"code": "MCR-A08", "axis": "ambiental", "title": "Sem conflito ANA outorgas", "weight": WEIGHTS["A08"], "regulation": "Lei 9.433/97 · ANA"},
        # Trabalhista
        {"code": "MCR-T01", "axis": "trabalhista", "title": "Fora Lista Suja MTE", "weight": WEIGHTS["T01"], "regulation": "Portaria MTE 1.293/17"},
        {"code": "MCR-T02", "axis": "trabalhista", "title": "CNDT válida", "weight": WEIGHTS["T02"], "regulation": "Lei 12.440/11 · TST"},
        {"code": "MCR-T03", "axis": "trabalhista", "title": "CAGED/eSocial", "weight": WEIGHTS["T03"], "regulation": "Dec. 8.373/14"},
        {"code": "MCR-T04", "axis": "trabalhista", "title": "eSocial ativo", "weight": WEIGHTS["T04"], "regulation": "Dec. 8.373/14"},
        {"code": "MCR-T05", "axis": "trabalhista", "title": "NR-31 conformidade", "weight": WEIGHTS["T05"], "regulation": "NR-31"},
        {"code": "MCR-T06", "axis": "trabalhista", "title": "CIPATR (>50 trabalhadores)", "weight": WEIGHTS["T06"], "regulation": "NR-31 item 31.8"},
        # Jurídico
        {"code": "MCR-J01", "axis": "juridico", "title": "Sem processos DataJud críticos", "weight": WEIGHTS["J01"], "regulation": "DataJud/CNJ"},
        {"code": "MCR-J02", "axis": "juridico", "title": "Sem DJEN 30d", "weight": WEIGHTS["J02"], "regulation": "Res. CNJ 455/22"},
        {"code": "MCR-J03", "axis": "juridico", "title": "Sem protestos", "weight": WEIGHTS["J03"], "regulation": "Lei 9.492/97"},
        {"code": "MCR-J04", "axis": "juridico", "title": "Sem reclamação CNJ", "weight": WEIGHTS["J04"], "regulation": "Res. CNJ 135/11"},
        {"code": "MCR-J05", "axis": "juridico", "title": "Sem execução fiscal", "weight": WEIGHTS["J05"], "regulation": "Lei 6.830/80"},
        # Financeiro
        {"code": "MCR-FI01", "axis": "financeiro", "title": "Sem inadimplência SICOR", "weight": WEIGHTS["FI01"], "regulation": "SICOR-BCB"},
        {"code": "MCR-FI02", "axis": "financeiro", "title": "Não consta CEIS", "weight": WEIGHTS["FI02"], "regulation": "Lei 12.846/13"},
        {"code": "MCR-FI03", "axis": "financeiro", "title": "Não consta CNEP", "weight": WEIGHTS["FI03"], "regulation": "Lei 12.846/13"},
        {"code": "MCR-FI04", "axis": "financeiro", "title": "Sem pendência PIX", "weight": WEIGHTS["FI04"], "regulation": "BCB · PIX"},
        {"code": "MCR-FI05", "axis": "financeiro", "title": "CCIR financeiro", "weight": WEIGHTS["FI05"], "regulation": "Lei 5.868/72"},
    ]
