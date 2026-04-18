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

export function ComplianceTab({ property }: { property: PropertyData }) {
  const [type, setType] = useState<"mcr29" | "eudr">("mcr29");
  const [result, setResult] = useState<ComplianceResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function run() {
      setLoading(true);
      setError(null);
      try {
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
            onClick={() => setType("mcr29")}
            className={`px-4 py-1.5 text-sm font-medium transition ${
              type === "mcr29"
                ? "bg-emerald-500/20 text-emerald-300"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            MCR 2.9 (Crédito Rural)
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
        className="group block border border-emerald-900/30 bg-gradient-to-r from-emerald-950/20 to-slate-900/40 rounded-lg px-4 py-3 hover:border-emerald-500/40 transition"
      >
        <div className="flex items-center gap-3">
          <ShieldCheck className="w-5 h-5 text-emerald-400 flex-shrink-0" />
          <div className="min-w-0 flex-1">
            <div className="text-sm font-medium text-slate-100">
              Análise completa MCR 2.9 — <span className="text-emerald-400">32 critérios em 5 eixos</span>
            </div>
            <div className="text-xs text-slate-400 mt-0.5">
              Auditoria auditável fundiário · ambiental · trabalhista · jurídico · financeiro com laudo PDF
            </div>
          </div>
          <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-emerald-400 group-hover:translate-x-0.5 transition flex-shrink-0" />
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
    </div>
  );
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
