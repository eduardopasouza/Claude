"use client";

import { useState } from "react";
import { Shield, AlertTriangle, CheckCircle2, XCircle, MapPin, FileText, Loader2 } from "lucide-react";
import { apiPost } from "@/lib/api";
import { cn } from "@/lib/utils";

interface ComplianceResult {
  status: string;
  risk_level: string;
  checks: Array<{
    source: string;
    status: string;
    detail: string;
  }>;
  summary: string;
}

type AuditType = "mcr29" | "eudr";

export default function CompliancePage() {
  const [auditType, setAuditType] = useState<AuditType>("mcr29");
  const [cpfCnpj, setCpfCnpj] = useState("");
  const [lat, setLat] = useState("-3.1190");
  const [lng, setLng] = useState("-60.0217");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ComplianceResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAudit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    const path =
      auditType === "mcr29"
        ? "/api/v1/compliance/mcr29"
        : "/api/v1/compliance/eudr";

    const body =
      auditType === "mcr29"
        ? { cpf_cnpj: cpfCnpj }
        : { latitude: parseFloat(lat), longitude: parseFloat(lng), cpf_cnpj: cpfCnpj || undefined };

    const { data, error: apiError } = await apiPost<ComplianceResult>(path, body);
    if (apiError) setError(apiError);
    else if (data) setResult(data);
    setLoading(false);
  };

  const riskColor: Record<string, string> = {
    low: "text-risk-low",
    medium: "text-risk-medium",
    high: "text-risk-high",
    critical: "text-risk-critical",
    blocked: "text-risk-critical",
    approved: "text-risk-low",
  };

  const riskBg: Record<string, string> = {
    low: "bg-risk-low/10 border-risk-low/30",
    medium: "bg-risk-medium/10 border-risk-medium/30",
    high: "bg-risk-high/10 border-risk-high/30",
    critical: "bg-risk-critical/10 border-risk-critical/30",
    blocked: "bg-risk-critical/10 border-risk-critical/30",
    approved: "bg-risk-low/10 border-risk-low/30",
  };

  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h2 className="text-2xl font-display font-bold flex items-center gap-2">
          <Shield className="text-agrojus-emerald" size={24} />
          Motor de Compliance
        </h2>
        <p className="text-sm text-[var(--muted-foreground)] mt-1">
          Auditoria MCR 2.9 e EUDR — verificação em tempo real contra bases oficiais
        </p>
      </div>

      {/* Seletor de tipo de auditoria */}
      <div className="flex gap-2">
        <button
          onClick={() => setAuditType("mcr29")}
          className={cn(
            "px-4 py-2 rounded-lg text-sm font-medium transition-all",
            auditType === "mcr29"
              ? "bg-agrojus-emerald text-agrojus-body"
              : "glass text-[var(--muted-foreground)] hover:text-foreground"
          )}
        >
          MCR 2.9 — Crédito Rural
        </button>
        <button
          onClick={() => setAuditType("eudr")}
          className={cn(
            "px-4 py-2 rounded-lg text-sm font-medium transition-all",
            auditType === "eudr"
              ? "bg-agrojus-emerald text-agrojus-body"
              : "glass text-[var(--muted-foreground)] hover:text-foreground"
          )}
        >
          EUDR — Regulamento Europeu
        </button>
      </div>

      {/* Formulário */}
      <div className="glass rounded-xl p-6 space-y-4">
        <div>
          <label className="block text-xs uppercase tracking-wider text-[var(--muted-foreground)] mb-1.5 font-medium">
            CPF ou CNPJ do proprietário
          </label>
          <input
            type="text"
            value={cpfCnpj}
            onChange={(e) => setCpfCnpj(e.target.value)}
            placeholder="00.000.000/0000-00"
            className="w-full bg-agrojus-body border border-[var(--border)] rounded-lg px-4 py-2.5 text-sm text-foreground placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-1 focus:ring-agrojus-emerald"
          />
        </div>

        {auditType === "eudr" && (
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs uppercase tracking-wider text-[var(--muted-foreground)] mb-1.5 font-medium">
                <MapPin size={12} className="inline mr-1" />
                Latitude
              </label>
              <input
                type="text"
                value={lat}
                onChange={(e) => setLat(e.target.value)}
                className="w-full bg-agrojus-body border border-[var(--border)] rounded-lg px-4 py-2.5 text-sm font-mono text-foreground focus:outline-none focus:ring-1 focus:ring-agrojus-emerald"
              />
            </div>
            <div>
              <label className="block text-xs uppercase tracking-wider text-[var(--muted-foreground)] mb-1.5 font-medium">
                Longitude
              </label>
              <input
                type="text"
                value={lng}
                onChange={(e) => setLng(e.target.value)}
                className="w-full bg-agrojus-body border border-[var(--border)] rounded-lg px-4 py-2.5 text-sm font-mono text-foreground focus:outline-none focus:ring-1 focus:ring-agrojus-emerald"
              />
            </div>
          </div>
        )}

        <button
          onClick={handleAudit}
          disabled={loading || !cpfCnpj}
          className={cn(
            "w-full py-3 rounded-lg text-sm font-semibold transition-all flex items-center justify-center gap-2",
            loading
              ? "bg-agrojus-elevated text-[var(--muted-foreground)] cursor-wait"
              : "bg-agrojus-emerald text-agrojus-body hover:opacity-90 glow-hover"
          )}
        >
          {loading ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              Consultando bases oficiais…
            </>
          ) : (
            <>
              <Shield size={16} />
              Executar Auditoria {auditType === "mcr29" ? "MCR 2.9" : "EUDR"}
            </>
          )}
        </button>
      </div>

      {/* Erro */}
      {error && (
        <div className="p-4 rounded-lg bg-risk-critical/10 border border-risk-critical/30 text-risk-critical text-sm flex items-center gap-2">
          <XCircle size={16} />
          {error}
        </div>
      )}

      {/* Resultado */}
      {result && (
        <div className="space-y-4">
          {/* Veredicto */}
          <div
            className={cn(
              "rounded-xl p-6 border",
              riskBg[result.risk_level] || riskBg.medium
            )}
          >
            <div className="flex items-center gap-3 mb-2">
              {result.risk_level === "low" || result.status === "approved" ? (
                <CheckCircle2 size={28} className="text-risk-low" />
              ) : (
                <AlertTriangle size={28} className={riskColor[result.risk_level] || "text-risk-medium"} />
              )}
              <div>
                <h3 className={cn("text-xl font-display font-bold", riskColor[result.risk_level] || "text-foreground")}>
                  {result.status?.toUpperCase() || result.risk_level?.toUpperCase()}
                </h3>
                <p className="text-sm text-[var(--muted-foreground)]">{result.summary}</p>
              </div>
            </div>
          </div>

          {/* Checklist de verificações */}
          {result.checks && result.checks.length > 0 && (
            <div className="glass rounded-xl p-4 space-y-2">
              <h4 className="text-sm font-semibold flex items-center gap-2 mb-3">
                <FileText size={14} className="text-agrojus-emerald" />
                Verificações Realizadas
              </h4>
              {result.checks.map((check, i) => (
                <div
                  key={i}
                  className="flex items-start gap-3 px-3 py-2.5 rounded-lg bg-agrojus-body/50"
                >
                  {check.status === "pass" || check.status === "clear" ? (
                    <CheckCircle2 size={16} className="text-risk-low mt-0.5 shrink-0" />
                  ) : (
                    <XCircle size={16} className="text-risk-critical mt-0.5 shrink-0" />
                  )}
                  <div className="min-w-0">
                    <p className="text-sm font-medium">{check.source}</p>
                    <p className="text-xs text-[var(--muted-foreground)]">{check.detail}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
