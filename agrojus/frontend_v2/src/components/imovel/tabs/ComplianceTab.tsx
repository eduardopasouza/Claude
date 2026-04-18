"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  CheckCircle2,
  XCircle,
  AlertCircle,
  Info,
  Loader2,
  ShieldCheck,
  ShieldAlert,
  Shield,
  FileText,
  ArrowRight,
  ChevronDown,
  ChevronRight,
  Clock,
  MinusCircle,
} from "lucide-react";
import { fetchWithAuth } from "@/lib/api";
import type { PropertyData } from "../PropertyHeader";

type CheckStatus = "approved" | "blocked" | "restricted" | "info";

type ComplianceCheck = {
  check: string;
  status: CheckStatus;
  detail: string;
  regulation?: string;
  alerts?: unknown[];
  embargos?: unknown[];
  terras_indigenas?: unknown[];
};

type ComplianceResult = {
  compliance_id: string;
  generated_at: string;
  type: "mcr29" | "eudr";
  overall_status: string;
  checks: ComplianceCheck[];
  risk_level: string;
  recommendation: string;
  sources_consulted: string[];
};

// === MCR 2.9 expandido (32 critérios) ===
type FullStatus = "passed" | "failed" | "pending" | "not_applicable";

type FullCriterion = {
  code: string;
  axis: string;
  title: string;
  description: string;
  regulation: string;
  status: FullStatus;
  passed: boolean | null;
  details: string;
  weight: number;
  evidence: Record<string, unknown>;
};

type FullAxisScore = {
  axis: string;
  label: string;
  total_criteria: number;
  passed: number;
  failed: number;
  pending: number;
  not_applicable: number;
  weighted_score: number;
};

type FullResult = {
  car_code: string | null;
  cpf_cnpj: string | null;
  overall_status: "approved" | "restricted" | "blocked" | "indeterminate";
  overall_score: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  axis_scores: FullAxisScore[];
  criteria: FullCriterion[];
  summary: string;
  recommendation: string;
  sources_consulted: string[];
  pending_sources: string[];
};

const STATUS_META: Record<
  CheckStatus,
  { icon: typeof CheckCircle2; color: string; bg: string }
> = {
  approved: {
    icon: CheckCircle2,
    color: "text-emerald-400",
    bg: "bg-emerald-950/20 border-emerald-900/40",
  },
  blocked: {
    icon: XCircle,
    color: "text-red-400",
    bg: "bg-red-950/30 border-red-900/40",
  },
  restricted: {
    icon: AlertCircle,
    color: "text-amber-400",
    bg: "bg-amber-950/20 border-amber-900/40",
  },
  info: {
    icon: Info,
    color: "text-slate-400",
    bg: "bg-slate-900/40 border-slate-800",
  },
};

type TabMode = "mcr29" | "eudr" | "full";

export function ComplianceTab({ property }: { property: PropertyData }) {
  const [type, setType] = useState<TabMode>("full"); // default: 32 critérios
  const [result, setResult] = useState<ComplianceResult | null>(null);
  const [full, setFull] = useState<FullResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function run() {
      setLoading(true);
      setError(null);
      setResult(null);
      setFull(null);
      try {
        if (type === "full") {
          const res = await fetchWithAuth("/compliance/mcr29/full", {
            method: "POST",
            body: JSON.stringify({ car_code: property.car_code }),
          });
          if (!res.ok) throw new Error(await res.text());
          const data = (await res.json()) as FullResult;
          if (!cancelled) setFull(data);
        } else {
          const body: Record<string, unknown> = {
            car_code: property.car_code,
            radius_km: 5,
          };
          if (property.centroid) {
            body.latitude = property.centroid.lat;
            body.longitude = property.centroid.lon;
          }
          const res = await fetchWithAuth(`/compliance/${type}`, {
            method: "POST",
            body: JSON.stringify(body),
          });
          if (!res.ok) throw new Error(await res.text());
          const data = (await res.json()) as ComplianceResult;
          if (!cancelled) setResult(data);
        }
      } catch (e) {
        if (!cancelled) setError(String(e));
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    run();
    return () => {
      cancelled = true;
    };
  }, [property.car_code, property.centroid, type]);

  return (
    <div className="p-6 space-y-5">
      <header className="flex flex-wrap items-center gap-3 justify-between">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          Compliance
        </h2>
        <div className="flex rounded-lg border border-slate-800 overflow-hidden">
          <button
            onClick={() => setType("full")}
            className={`px-4 py-1.5 text-sm font-medium transition ${
              type === "full"
                ? "bg-emerald-500/20 text-emerald-300"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            MCR 2.9 Completo (32)
          </button>
          <button
            onClick={() => setType("mcr29")}
            className={`px-4 py-1.5 text-sm font-medium transition border-l border-slate-800 ${
              type === "mcr29"
                ? "bg-emerald-500/20 text-emerald-300"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            MCR 2.9 Rápido (6)
          </button>
          <button
            onClick={() => setType("eudr")}
            className={`px-4 py-1.5 text-sm font-medium transition border-l border-slate-800 ${
              type === "eudr"
                ? "bg-emerald-500/20 text-emerald-300"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            EUDR (UE 2023/1115)
          </button>
        </div>
      </header>

      <Link
        href={`/compliance?car=${encodeURIComponent(property.car_code)}`}
        className="group block border border-emerald-900/30 bg-gradient-to-r from-emerald-950/20 to-slate-900/40 rounded-lg px-3 py-2 hover:border-emerald-500/40 transition"
      >
        <div className="flex items-center gap-3">
          <ShieldCheck className="w-4 h-4 text-emerald-400 flex-shrink-0" />
          <div className="min-w-0 flex-1 text-xs text-slate-300">
            Ver análise completa em tela cheia com laudo PDF exportável
          </div>
          <ArrowRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-emerald-400 group-hover:translate-x-0.5 transition flex-shrink-0" />
        </div>
      </Link>

      {loading && (
        <div className="p-12 flex items-center justify-center text-slate-400">
          <Loader2 className="w-5 h-5 animate-spin mr-2" />
          Verificando em 5 fontes oficiais (FUNAI, ICMBio, IBAMA, INPE, MTE)…
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-950/30 border border-red-900/40 rounded text-red-300 text-sm">
          Erro: {error}
        </div>
      )}

      {result && !loading && (
        <>
          <OverallBanner result={result} />

          <div className="space-y-3">
            {result.checks.map((check, i) => (
              <CheckRow key={i} check={check} />
            ))}
          </div>

          {result.sources_consulted.length > 0 && (
            <footer className="text-xs text-slate-500 flex items-center gap-2 pt-3 border-t border-slate-800">
              <FileText className="w-3 h-3" />
              Fontes consultadas: {result.sources_consulted.join(" · ")}
            </footer>
          )}
        </>
      )}

      {full && !loading && <FullResultView full={full} />}
    </div>
  );
}

// =========================================================================
// MCR 2.9 Completo (32 critérios) — embutido
// =========================================================================

const FULL_STATUS: Record<FullStatus, { icon: typeof CheckCircle2; color: string; bg: string; label: string }> = {
  passed: { icon: CheckCircle2, color: "text-emerald-400", bg: "bg-emerald-950/20 border-emerald-900/40", label: "Aprovado" },
  failed: { icon: XCircle, color: "text-red-400", bg: "bg-red-950/30 border-red-900/40", label: "Falha" },
  pending: { icon: Clock, color: "text-amber-400", bg: "bg-amber-950/20 border-amber-900/30", label: "Pendente" },
  not_applicable: { icon: MinusCircle, color: "text-slate-500", bg: "bg-slate-900/40 border-slate-800", label: "N/A" },
};

function FullResultView({ full }: { full: FullResult }) {
  const isBlocked = full.overall_status === "blocked";
  const isRestricted = full.overall_status === "restricted";
  const isIndeterminate = full.overall_status === "indeterminate";

  const colors = isBlocked
    ? "bg-red-950/40 border-red-500/40 text-red-300"
    : isRestricted
    ? "bg-amber-950/30 border-amber-500/40 text-amber-300"
    : isIndeterminate
    ? "bg-slate-900 border-slate-700 text-slate-300"
    : "bg-emerald-950/30 border-emerald-500/40 text-emerald-300";

  const Icon = isBlocked ? XCircle : isRestricted || isIndeterminate ? AlertCircle : ShieldCheck;
  const label = isBlocked
    ? "BLOQUEADO"
    : isRestricted
    ? "RESTRITO"
    : isIndeterminate
    ? "INDETERMINADO"
    : "APTO";

  return (
    <>
      <div className={`border rounded-xl p-5 ${colors}`}>
        <div className="flex items-start gap-3">
          <Icon className="w-8 h-8 flex-shrink-0 mt-0.5" />
          <div className="min-w-0 flex-1">
            <div className="flex items-baseline gap-3 flex-wrap">
              <h3 className="font-semibold text-lg">{label}</h3>
              <span className="text-xs uppercase tracking-wider opacity-70 font-normal">
                Risco {full.risk_level}
              </span>
              <span className="text-xs font-mono opacity-70 ml-auto">
                Score {full.overall_score.toFixed(0)}/1000
              </span>
            </div>
            <p className="text-sm opacity-90 mt-1">{full.summary}</p>
            <p className="text-xs opacity-80 mt-2 leading-relaxed">
              <strong>Recomendação:</strong> {full.recommendation}
            </p>
          </div>
        </div>
      </div>

      {/* Score por eixo em cards compactos */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
        {full.axis_scores.map((a) => {
          const hasFailed = a.failed > 0;
          const allPassed = a.failed === 0 && a.pending === 0 && a.passed > 0;
          const color = hasFailed
            ? "text-red-400"
            : allPassed
            ? "text-emerald-400"
            : "text-amber-400";
          return (
            <div key={a.axis} className="border border-slate-800 bg-slate-900/20 rounded-lg p-3">
              <div className="text-[10px] uppercase tracking-wider text-slate-500 font-semibold">
                {a.label}
              </div>
              <div className={`text-2xl font-bold mt-0.5 ${color}`}>
                {a.weighted_score.toFixed(0)}%
              </div>
              <div className="text-[10px] text-slate-500 mt-0.5">
                {a.passed}✓ · {a.failed}✗ · {a.pending}?
              </div>
            </div>
          );
        })}
      </div>

      {/* Accordions por eixo */}
      <div className="space-y-2">
        {full.axis_scores.map((axis) => (
          <FullAxisAccordion
            key={axis.axis}
            axis={axis}
            criteria={full.criteria.filter((c) => c.axis === axis.axis)}
          />
        ))}
      </div>

      <div className="text-xs text-slate-500 pt-3 border-t border-slate-800 space-y-1">
        {full.sources_consulted.length > 0 && (
          <div>
            <strong className="text-slate-400">Fontes consultadas:</strong>{" "}
            {full.sources_consulted.join(" · ")}
          </div>
        )}
        {full.pending_sources.length > 0 && (
          <div>
            <strong className="text-amber-300">Pendentes de integração:</strong>{" "}
            {full.pending_sources.join(" · ")}
          </div>
        )}
      </div>
    </>
  );
}

function FullAxisAccordion({
  axis,
  criteria,
}: {
  axis: FullAxisScore;
  criteria: FullCriterion[];
}) {
  // Auto-expande se tem falhas
  const [expanded, setExpanded] = useState(axis.failed > 0);
  const hasFailed = axis.failed > 0;

  return (
    <div className="border border-slate-800 rounded-xl overflow-hidden">
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full px-4 py-2.5 flex items-center gap-3 hover:bg-slate-900 transition text-left"
      >
        {expanded ? (
          <ChevronDown className="w-4 h-4 text-slate-500" />
        ) : (
          <ChevronRight className="w-4 h-4 text-slate-500" />
        )}
        <div className="min-w-0 flex-1">
          <div className={`font-medium text-sm ${hasFailed ? "text-red-300" : "text-slate-100"}`}>
            {axis.label}
          </div>
          <div className="text-xs text-slate-500 mt-0.5">
            {axis.total_criteria} critérios · {axis.passed} aprovados · {axis.failed} falhas · {axis.pending} pendentes
          </div>
        </div>
        <div className="text-sm font-mono text-slate-400">
          {axis.weighted_score.toFixed(0)}%
        </div>
      </button>
      {expanded && (
        <div className="border-t border-slate-800 p-2 space-y-1.5 bg-slate-950/40">
          {criteria.map((c) => (
            <FullCriterionRow key={c.code} criterion={c} />
          ))}
        </div>
      )}
    </div>
  );
}

function FullCriterionRow({ criterion }: { criterion: FullCriterion }) {
  const meta = FULL_STATUS[criterion.status];
  const Icon = meta.icon;
  const [showEvidence, setShowEvidence] = useState(false);
  const hasEvidence = criterion.evidence && Object.keys(criterion.evidence).length > 0;

  // Explicação humana do apontamento
  const explicacao = explicarApontamento(criterion);

  return (
    <div className={`border rounded-lg p-3 ${meta.bg}`}>
      <div className="flex items-start gap-2.5">
        <Icon className={`w-4 h-4 flex-shrink-0 mt-0.5 ${meta.color}`} />
        <div className="min-w-0 flex-1">
          <div className="flex items-baseline gap-2 flex-wrap">
            <span className="text-[10px] font-mono text-slate-500">{criterion.code}</span>
            <h4 className="font-medium text-slate-100 text-sm">{criterion.title}</h4>
            <span className={`text-[9px] font-semibold uppercase ${meta.color}`}>
              {meta.label}
            </span>
            <span className="text-[10px] text-slate-500 ml-auto">peso {criterion.weight}</span>
          </div>
          <p className="text-xs text-slate-300 mt-1 leading-relaxed">{criterion.details}</p>
          {explicacao && (
            <p className={`text-xs mt-1.5 leading-relaxed italic ${
              criterion.status === "failed"
                ? "text-red-300/80"
                : criterion.status === "pending"
                ? "text-amber-300/80"
                : "text-slate-400"
            }`}>
              → {explicacao}
            </p>
          )}
          <p className="text-[10px] text-slate-500 mt-1 italic">{criterion.regulation}</p>
          {hasEvidence && (
            <>
              <button
                onClick={() => setShowEvidence((v) => !v)}
                className="text-[10px] text-slate-400 hover:text-slate-200 mt-1 underline decoration-dotted underline-offset-2"
              >
                {showEvidence ? "ocultar" : "ver"} evidência
              </button>
              {showEvidence && (
                <pre className="mt-1.5 p-2 bg-slate-950 border border-slate-800 rounded text-[10px] text-slate-400 overflow-auto max-h-40">
                  {JSON.stringify(criterion.evidence, null, 2)}
                </pre>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// ============ Narrativa dos apontamentos ============
// Explica ao advogado, em português claro, o que significa cada resultado
// e qual a próxima ação necessária.
function explicarApontamento(c: FullCriterion): string {
  const e = c.evidence as Record<string, unknown>;

  if (c.status === "pending") {
    // Item pendente — informa qual fonte falta
    if (c.code === "MCR-F05") return "Fonte SIGMINE/ANM ainda não integrada. Não significa ausência de mineração — verificar manualmente no mapa ANM.";
    if (c.code === "MCR-F06") return "CCIR requer consulta individual no INCRA. Verificar com o proprietário a certidão vigente.";
    if (c.code === "MCR-F07") return "ITR é sigiloso — solicitar a comprovação de quitação diretamente ao tomador.";
    if (c.code === "MCR-F08") return "Sobreposição com terras da União (SPU) ainda não monitorada. Verificar no e-SPU se o imóvel fica em área ribeirinha/fronteira/marinha.";
    if (c.code === "MCR-A06") return "Reserva Legal não está no cadastro simplificado do CAR que carregamos. Verificar percentual no SICAR oficial.";
    if (c.code === "MCR-A07") return "APP não está no cadastro carregado. Verificar no SICAR oficial.";
    if (c.code === "MCR-A08") return "Outorgas ANA ainda não integradas. Verificar no CNARH40 se há conflito com outorgas no imóvel.";
    if (c.code === "MCR-T02") return "CNDT requer consulta individual no portal TST.";
    if (c.code === "MCR-T03" || c.code === "MCR-T04") return "eSocial/CAGED exige certificado digital do empregador — solicitar ao tomador.";
    if (c.code === "MCR-T05") return "NR-31 é declaratória — pedir ao tomador o documento de conformidade assinado pelo responsável técnico.";
    if (c.code === "MCR-T06") return "Só se aplica a imóveis com mais de 50 trabalhadores. Pedir declaração do quadro de funcionários.";
    if (c.code === "MCR-J02") return "DJEN por CPF/CNPJ da parte exige consulta pontual no Comunica.PJe.";
    if (c.code === "MCR-J03") return "Protestos exigem consulta no CENPROT (serviço pago).";
    if (c.code === "MCR-J04") return "Reclamação CNJ não é monitorada ainda.";
    if (c.code === "MCR-FI01") return "SICOR identifica contratos no imóvel, mas inadimplência exige consulta ao BCB.";
    if (c.code === "MCR-FI02" && !e.base_size) return "Execute o ETL CEIS para destravar esta verificação.";
    if (c.code === "MCR-FI03" && !e.base_size) return "Execute o ETL CNEP para destravar esta verificação.";
    if (c.code === "MCR-FI04") return "PIX não tem lista pública de negativação — item informativo apenas.";
    if (c.code === "MCR-FI05") return "CCIR ausente — solicitar cópia ao tomador.";
    if (!c.passed && c.details.includes("não informado")) return "Informe o CPF/CNPJ do proprietário na análise para esta verificação funcionar.";
    return "";
  }

  if (c.status === "failed") {
    if (c.code === "MCR-F01") return "CAR cancelado ou suspenso bloqueia totalmente o crédito rural. Regularizar antes de qualquer proposta bancária.";
    if (c.code === "MCR-F02" && (e.sigef_overlaps as number) > 1) return "Múltiplas parcelas SIGEF sobrepostas indicam possível conflito dominial — checar matrícula dominal e certidões.";
    if (c.code === "MCR-F03") return "Sobreposição com Terra Indígena é BLOQUEANTE por força constitucional (CF art. 231). Crédito negado sine qua non.";
    if (c.code === "MCR-F04") return "Sobreposição com UC de proteção integral bloqueia crédito. Em UCs de uso sustentável, verificar plano de manejo.";
    if (c.code === "MCR-A01") return "Desmatamento PRODES pós-31/07/2019 é corte oficial do MCR 2.9 — crédito bloqueado salvo apresentação de ASV, PRAD ou TAC válido.";
    if (c.code === "MCR-A02") return "DETER nos últimos 12 meses é gatilho de bloqueio imediato. Pode ser desmate recente ou degradação ainda não consolidada no PRODES.";
    if (c.code === "MCR-A03") return "MapBiomas Alerta validado indica desmate confirmado por satélite. Mesma severidade do DETER.";
    if (c.code === "MCR-A04") {
      const embargos = (e.embargos_ibama as number) || 0;
      const icmbio = (e.embargos_icmbio as number) || 0;
      if (embargos + icmbio > 0) {
        return `Embargo ambiental ativo impede qualquer atividade produtiva na área embargada. ${embargos > 0 ? `${embargos} embargo(s) IBAMA` : ""}${embargos > 0 && icmbio > 0 ? " + " : ""}${icmbio > 0 ? `${icmbio} embargo(s) ICMBio` : ""}. Consultar dossiê do imóvel.`;
      }
      return "Embargo ambiental ativo impede crédito. Regularização exige procedimento administrativo específico.";
    }
    if (c.code === "MCR-A05") {
      const sifisc = (e.autos_sifisc as number) || 0;
      const multa = (e.multa_total_rs as number) || 0;
      if (sifisc > 0) {
        return `${sifisc} auto(s) de infração IBAMA vinculados ao CPF/CNPJ do proprietário${multa ? `, totalizando R$ ${multa.toLocaleString("pt-BR", { maximumFractionDigits: 2 })} em multas` : ""}. Verificar situação de pagamento e possível defesa administrativa.`;
      }
      return "Autos de infração IBAMA identificados. Avaliar se estão quitados ou em discussão administrativa/judicial.";
    }
    if (c.code === "MCR-A06") return "Reserva Legal abaixo do mínimo legal — exige regularização via PRAD ou CRA (Cota de Reserva Ambiental).";
    if (c.code === "MCR-T01") return "Nome na Lista Suja do Trabalho Escravo BLOQUEIA o crédito rural por 2 anos (Portaria MTE 1.293/17). Sem exceção.";
    if (c.code === "MCR-J01") return "Execução fiscal ou usucapião pode comprometer a garantia do crédito — solicitar certidão do tribunal.";
    if (c.code === "MCR-J05") return "Execução fiscal em andamento pode gerar penhora. Bancos exigem quitação ou plano aprovado.";
    if (c.code === "MCR-FI01") return "Inadimplência SICOR inviabiliza novo crédito rural até regularização.";
    if (c.code === "MCR-FI02") {
      const n = (e.ceis_matches as number) || 0;
      return `Constam ${n} registro(s) no CEIS (empresa inidônea). BLOQUEANTE para contratos com recursos públicos (Lei 12.846/13).`;
    }
    if (c.code === "MCR-FI03") {
      const n = (e.cnep_matches as number) || 0;
      return `${n} sanção(ões) ativa(s) no CNEP. BLOQUEANTE sobretudo para crédito oficial.`;
    }
    return "";
  }

  return "";
}

function OverallBanner({ result }: { result: ComplianceResult }) {
  const isBlocked = ["blocked", "non_compliant"].includes(result.overall_status);
  const isRestricted = result.overall_status === "restricted";
  const Icon = isBlocked ? XCircle : isRestricted ? AlertCircle : ShieldCheck;

  const colors = isBlocked
    ? "bg-red-950/40 border-red-500/40 text-red-300"
    : isRestricted
    ? "bg-amber-950/30 border-amber-500/40 text-amber-300"
    : "bg-emerald-950/30 border-emerald-500/40 text-emerald-300";

  return (
    <div className={`border rounded-xl p-5 ${colors}`}>
      <div className="flex items-start gap-3">
        <Icon className="w-8 h-8 flex-shrink-0 mt-0.5" />
        <div className="min-w-0 flex-1">
          <h3 className="font-semibold text-lg mb-1 flex items-center gap-2">
            {isBlocked
              ? "BLOQUEADO"
              : isRestricted
              ? "RESTRITO"
              : "APTO"}
            <span className="text-xs uppercase tracking-wider opacity-70 font-normal">
              · Risco {result.risk_level}
            </span>
          </h3>
          <p className="text-sm opacity-90">{result.recommendation}</p>
        </div>
      </div>
    </div>
  );
}

function CheckRow({ check }: { check: ComplianceCheck }) {
  const meta = STATUS_META[check.status];
  const Icon = meta.icon;

  return (
    <div className={`border rounded-lg p-4 ${meta.bg}`}>
      <div className="flex items-start gap-3">
        <Icon className={`w-5 h-5 flex-shrink-0 mt-0.5 ${meta.color}`} />
        <div className="min-w-0 flex-1">
          <h4 className="font-semibold text-slate-100 mb-1">{check.check}</h4>
          <p className="text-sm text-slate-300 leading-relaxed">
            {check.detail}
          </p>
          {check.regulation && (
            <p className="text-xs text-slate-500 mt-2 italic">
              {check.regulation}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
