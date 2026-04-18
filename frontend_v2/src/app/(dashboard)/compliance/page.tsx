"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import {
  ShieldCheck,
  Search,
  Download,
  Loader2,
  CheckCircle2,
  XCircle,
  Clock,
  MinusCircle,
  AlertCircle,
  ChevronDown,
  ChevronRight,
  Shield,
  ShieldAlert,
  ShieldX,
  Sprout,
  Scale,
  Users,
  Gavel,
  Coins,
} from "lucide-react";
import { fetchWithAuth } from "@/lib/api";

type Status = "passed" | "failed" | "pending" | "not_applicable";

type Criterion = {
  code: string;
  axis: string;
  title: string;
  description: string;
  regulation: string;
  status: Status;
  passed: boolean | null;
  details: string;
  weight: number;
  evidence: Record<string, unknown>;
};

type AxisScore = {
  axis: string;
  label: string;
  total_criteria: number;
  passed: number;
  failed: number;
  pending: number;
  not_applicable: number;
  weighted_score: number;
};

type MCR29FullResult = {
  car_code: string | null;
  cpf_cnpj: string | null;
  generated_at: string;
  overall_status: "approved" | "restricted" | "blocked" | "indeterminate";
  overall_score: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  axis_scores: AxisScore[];
  criteria: Criterion[];
  summary: string;
  recommendation: string;
  sources_consulted: string[];
  pending_sources: string[];
};

const STATUS_META: Record<
  Status,
  { icon: typeof CheckCircle2; color: string; bg: string; label: string }
> = {
  passed: {
    icon: CheckCircle2,
    color: "text-emerald-400",
    bg: "bg-emerald-950/20 border-emerald-900/40",
    label: "Aprovado",
  },
  failed: {
    icon: XCircle,
    color: "text-red-400",
    bg: "bg-red-950/30 border-red-900/40",
    label: "Falha",
  },
  pending: {
    icon: Clock,
    color: "text-amber-400",
    bg: "bg-amber-950/20 border-amber-900/30",
    label: "Pendente",
  },
  not_applicable: {
    icon: MinusCircle,
    color: "text-slate-500",
    bg: "bg-slate-900/40 border-slate-800",
    label: "N/A",
  },
};

const AXIS_ICON: Record<string, typeof ShieldCheck> = {
  fundiario: Scale,
  ambiental: Sprout,
  trabalhista: Users,
  juridico: Gavel,
  financeiro: Coins,
};

export default function CompliancePage() {
  const searchParams = useSearchParams();
  const urlCar = searchParams.get("car") || "";
  const urlCpf = searchParams.get("cpf") || "";
  const autoRun = searchParams.get("auto") === "true" || Boolean(urlCar || urlCpf);

  const [carCode, setCarCode] = useState(urlCar);
  const [cpfCnpj, setCpfCnpj] = useState(urlCpf);
  const [result, setResult] = useState<MCR29FullResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pdfLoading, setPdfLoading] = useState(false);

  async function runWith(car: string, cpf: string) {
    if (!car && !cpf) {
      setError("Informe ao menos um CAR ou CPF/CNPJ");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetchWithAuth("/compliance/mcr29/full", {
        method: "POST",
        body: JSON.stringify({
          car_code: car || null,
          cpf_cnpj: cpf || null,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      setResult((await res.json()) as MCR29FullResult);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  async function run() {
    return runWith(carCode, cpfCnpj);
  }

  // Auto-run se vier CAR/CPF via query string
  useEffect(() => {
    if (autoRun && (urlCar || urlCpf)) {
      runWith(urlCar, urlCpf);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function downloadPDF() {
    setPdfLoading(true);
    try {
      const res = await fetchWithAuth("/compliance/mcr29/full/pdf", {
        method: "POST",
        body: JSON.stringify({
          car_code: carCode || null,
          cpf_cnpj: cpfCnpj || null,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `mcr29_${carCode || cpfCnpj}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      alert(String(e));
    } finally {
      setPdfLoading(false);
    }
  }

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
          <ShieldCheck className="h-8 w-8 text-emerald-400" />
          MCR 2.9 Expandido · 32 critérios auditáveis
        </h1>
        <p className="text-slate-400 max-w-3xl">
          Avaliação completa de compliance para crédito rural conforme
          Resolução CMN 5.193/2024 e normas correlatas, em 5 eixos:
          fundiário, ambiental, trabalhista, jurídico e financeiro.
        </p>
      </header>

      {/* Form */}
      <section className="border border-slate-800 bg-slate-900/20 rounded-xl p-5 space-y-4">
        <div className="grid gap-3 md:grid-cols-2">
          <label className="flex flex-col gap-1">
            <span className="text-xs text-slate-400 font-medium">
              Código CAR (recomendado)
            </span>
            <input
              value={carCode}
              onChange={(e) => setCarCode(e.target.value)}
              placeholder="MA-2100055-0013026E975B48D9B4F045D7352A1CB9"
              className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100 font-mono"
            />
          </label>
          <label className="flex flex-col gap-1">
            <span className="text-xs text-slate-400 font-medium">
              CPF/CNPJ do proprietário
            </span>
            <input
              value={cpfCnpj}
              onChange={(e) => setCpfCnpj(e.target.value)}
              placeholder="000.000.000-00 ou 00.000.000/0000-00"
              className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100 font-mono"
            />
          </label>
        </div>

        <div className="flex gap-2 items-center flex-wrap">
          <button
            onClick={run}
            disabled={loading || (!carCode && !cpfCnpj)}
            className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm rounded-lg transition"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" /> Avaliando 32
                critérios…
              </>
            ) : (
              <>
                <Search className="w-4 h-4" /> Avaliar compliance
              </>
            )}
          </button>
          {result && (
            <button
              onClick={downloadPDF}
              disabled={pdfLoading}
              className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-100 text-sm rounded-lg transition disabled:opacity-50"
            >
              {pdfLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" /> Gerando…
                </>
              ) : (
                <>
                  <Download className="w-4 h-4" /> Exportar laudo PDF
                </>
              )}
            </button>
          )}
        </div>

        {error && (
          <div className="p-3 bg-red-950/30 border border-red-900/40 rounded text-red-300 text-sm flex items-start gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
            {error}
          </div>
        )}
      </section>

      {result && <ResultView result={result} />}

      {!result && !loading && <CriteriaOverview />}
    </div>
  );
}

// --------------------------------------------------------------------------
// Resultado
// --------------------------------------------------------------------------

function ResultView({ result }: { result: MCR29FullResult }) {
  return (
    <div className="space-y-5">
      <OverallBanner result={result} />

      {/* Score por eixo */}
      <section className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {result.axis_scores.map((a) => (
          <AxisCard key={a.axis} axis={a} />
        ))}
      </section>

      {/* Critérios agrupados por eixo */}
      <section className="space-y-3">
        {result.axis_scores.map((axis) => (
          <AxisAccordion
            key={axis.axis}
            axis={axis}
            criteria={result.criteria.filter((c) => c.axis === axis.axis)}
          />
        ))}
      </section>

      {/* Fontes */}
      {(result.sources_consulted.length > 0 || result.pending_sources.length > 0) && (
        <footer className="border border-slate-800 rounded-xl p-4 text-xs text-slate-400 space-y-2">
          {result.sources_consulted.length > 0 && (
            <div>
              <strong className="text-slate-300">Fontes consultadas:</strong>{" "}
              {result.sources_consulted.join(" · ")}
            </div>
          )}
          {result.pending_sources.length > 0 && (
            <div>
              <strong className="text-amber-300">Fontes pendentes de integração:</strong>{" "}
              {result.pending_sources.join(" · ")}
            </div>
          )}
        </footer>
      )}
    </div>
  );
}

function OverallBanner({ result }: { result: MCR29FullResult }) {
  const isBlocked = result.overall_status === "blocked";
  const isRestricted = result.overall_status === "restricted";
  const isIndeterminate = result.overall_status === "indeterminate";

  const Icon = isBlocked ? ShieldX : isRestricted || isIndeterminate ? ShieldAlert : Shield;
  const label = isBlocked
    ? "BLOQUEADO"
    : isRestricted
    ? "RESTRITO"
    : isIndeterminate
    ? "INDETERMINADO"
    : "APTO";

  const colors = isBlocked
    ? "bg-red-950/40 border-red-500/40 text-red-300"
    : isRestricted
    ? "bg-amber-950/30 border-amber-500/40 text-amber-300"
    : isIndeterminate
    ? "bg-slate-900 border-slate-700 text-slate-300"
    : "bg-emerald-950/30 border-emerald-500/40 text-emerald-300";

  return (
    <div className={`border rounded-xl p-6 ${colors}`}>
      <div className="flex items-start gap-4">
        <Icon className="w-10 h-10 flex-shrink-0 mt-1" />
        <div className="min-w-0 flex-1">
          <div className="flex items-baseline gap-3 flex-wrap">
            <h2 className="font-bold text-xl">{label}</h2>
            <span className="text-sm font-medium opacity-80">
              Risco {result.risk_level}
            </span>
            <span className="text-sm font-mono opacity-80 ml-auto">
              Score {result.overall_score.toFixed(0)}/1000
            </span>
          </div>
          <p className="text-sm mt-2 opacity-90">{result.summary}</p>
          <p className="text-sm mt-3 opacity-80 leading-relaxed">
            <strong>Recomendação:</strong> {result.recommendation}
          </p>
        </div>
      </div>
    </div>
  );
}

function AxisCard({ axis }: { axis: AxisScore }) {
  const Icon = AXIS_ICON[axis.axis] || ShieldCheck;
  const hasFailed = axis.failed > 0;
  const allPassed = axis.failed === 0 && axis.pending === 0 && axis.passed > 0;
  const color = hasFailed
    ? "text-red-400"
    : allPassed
    ? "text-emerald-400"
    : "text-amber-400";

  return (
    <div className="border border-slate-800 bg-slate-900/20 rounded-lg p-3">
      <div className="flex items-center gap-2 mb-2">
        <Icon className={`w-4 h-4 ${color}`} />
        <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
          {axis.label}
        </span>
      </div>
      <div className={`text-2xl font-bold ${color}`}>
        {axis.weighted_score.toFixed(0)}%
      </div>
      <div className="text-[10px] text-slate-500 mt-1 space-y-0.5">
        <div>
          <span className="text-emerald-400">{axis.passed} ok</span> ·{" "}
          <span className="text-red-400">{axis.failed} falha</span>
        </div>
        <div>
          <span className="text-amber-400">{axis.pending} pend.</span> ·{" "}
          <span className="text-slate-500">{axis.not_applicable} n/a</span>
        </div>
      </div>
    </div>
  );
}

function AxisAccordion({
  axis,
  criteria,
}: {
  axis: AxisScore;
  criteria: Criterion[];
}) {
  const [expanded, setExpanded] = useState(axis.failed > 0);
  const Icon = AXIS_ICON[axis.axis] || ShieldCheck;

  const hasFailed = axis.failed > 0;

  return (
    <div className="border border-slate-800 rounded-xl overflow-hidden">
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full px-4 py-3 flex items-center gap-3 hover:bg-slate-900 transition text-left"
      >
        {expanded ? (
          <ChevronDown className="w-4 h-4 text-slate-500" />
        ) : (
          <ChevronRight className="w-4 h-4 text-slate-500" />
        )}
        <Icon className={`w-5 h-5 ${hasFailed ? "text-red-400" : "text-emerald-400"}`} />
        <div className="min-w-0 flex-1">
          <div className="font-medium text-slate-100">{axis.label}</div>
          <div className="text-xs text-slate-500">
            {axis.total_criteria} critérios · {axis.passed} aprovados ·{" "}
            {axis.failed} falhas · {axis.pending} pendentes
          </div>
        </div>
        <div className="text-sm font-mono text-slate-400">
          {axis.weighted_score.toFixed(0)}%
        </div>
      </button>
      {expanded && (
        <div className="border-t border-slate-800 p-3 space-y-2 bg-slate-950/40">
          {criteria.map((c) => (
            <CriterionRow key={c.code} criterion={c} />
          ))}
        </div>
      )}
    </div>
  );
}

function CriterionRow({ criterion }: { criterion: Criterion }) {
  const meta = STATUS_META[criterion.status];
  const Icon = meta.icon;
  const [showEvidence, setShowEvidence] = useState(false);
  const hasEvidence =
    criterion.evidence && Object.keys(criterion.evidence).length > 0;

  return (
    <div className={`border rounded-lg p-3 ${meta.bg}`}>
      <div className="flex items-start gap-3">
        <Icon className={`w-4 h-4 flex-shrink-0 mt-0.5 ${meta.color}`} />
        <div className="min-w-0 flex-1">
          <div className="flex items-baseline gap-2 flex-wrap">
            <span className="text-xs font-mono text-slate-500">{criterion.code}</span>
            <h4 className="font-medium text-slate-100 text-sm">
              {criterion.title}
            </h4>
            <span className={`text-[10px] font-semibold uppercase ${meta.color}`}>
              {meta.label}
            </span>
            <span className="text-[10px] text-slate-500 ml-auto">
              peso {criterion.weight}
            </span>
          </div>
          <p className="text-xs text-slate-300 mt-1 leading-relaxed">
            {criterion.details}
          </p>
          <p className="text-[10px] text-slate-500 mt-1 italic">
            {criterion.regulation}
          </p>
          {hasEvidence && (
            <button
              onClick={() => setShowEvidence((v) => !v)}
              className="text-[10px] text-slate-400 hover:text-slate-200 mt-1"
            >
              {showEvidence ? "ocultar" : "ver"} evidência
            </button>
          )}
          {showEvidence && hasEvidence && (
            <pre className="mt-1.5 p-2 bg-slate-950 border border-slate-800 rounded text-[10px] text-slate-400 overflow-auto max-h-40">
              {JSON.stringify(criterion.evidence, null, 2)}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
}

// --------------------------------------------------------------------------
// Overview dos critérios (tela inicial)
// --------------------------------------------------------------------------

function CriteriaOverview() {
  const axes = [
    { key: "fundiario", label: "Fundiário", count: 8, icon: Scale, desc: "CAR, SIGEF, TI, UC, SIGMINE, CCIR, ITR, SPU" },
    { key: "ambiental", label: "Ambiental", count: 8, icon: Sprout, desc: "PRODES, DETER, MapBiomas, embargos IBAMA, autos, RL, APP, ANA" },
    { key: "trabalhista", label: "Trabalhista", count: 6, icon: Users, desc: "Lista Suja, CNDT, CAGED, eSocial, NR-31, CIPATR" },
    { key: "juridico", label: "Jurídico", count: 5, icon: Gavel, desc: "DataJud, DJEN, protestos, CNJ, execução fiscal" },
    { key: "financeiro", label: "Financeiro", count: 5, icon: Coins, desc: "SICOR, CEIS, CNEP, PIX, CCIR" },
  ];
  return (
    <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
      {axes.map((a) => {
        const Icon = a.icon;
        return (
          <div key={a.key} className="border border-slate-800 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <Icon className="w-5 h-5 text-emerald-400" />
              <h3 className="font-semibold text-slate-100">
                {a.label}{" "}
                <span className="text-xs text-slate-500 font-normal">
                  {a.count} critérios
                </span>
              </h3>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">{a.desc}</p>
          </div>
        );
      })}
    </section>
  );
}
