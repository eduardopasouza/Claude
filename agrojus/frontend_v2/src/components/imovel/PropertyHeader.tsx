"use client";

import { Copy, MapPin, FileText, Loader2, AlertTriangle } from "lucide-react";
import { useState } from "react";

export type PropertyData = {
  car_code: string;
  municipio?: string;
  uf?: string;
  area_ha?: number;
  status?: string;
  tipo?: string;
  modulos_fiscais?: number;
  cod_municipio_ibge?: string;
  centroid?: { lat: number; lon: number };
};

type Props = {
  property: PropertyData | null;
  loading: boolean;
  error?: string | null;
};

const STATUS_META: Record<string, { label: string; color: string }> = {
  AT: { label: "Ativo", color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30" },
  PE: { label: "Pendente", color: "text-amber-400 bg-amber-500/10 border-amber-500/30" },
  CA: { label: "Cancelado", color: "text-red-400 bg-red-500/10 border-red-500/30" },
  SU: { label: "Suspenso", color: "text-orange-400 bg-orange-500/10 border-orange-500/30" },
};

export function PropertyHeader({ property, loading, error }: Props) {
  const [copied, setCopied] = useState(false);

  function copyCode() {
    if (!property?.car_code) return;
    navigator.clipboard.writeText(property.car_code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  if (loading) {
    return (
      <div className="flex items-center gap-3 px-6 py-5 bg-slate-900/50 border-b border-slate-800">
        <Loader2 className="w-5 h-5 animate-spin text-emerald-400" />
        <span className="text-slate-400">Carregando imóvel…</span>
      </div>
    );
  }

  if (error || !property) {
    return (
      <div className="flex items-center gap-3 px-6 py-5 bg-red-950/30 border-b border-red-900/40">
        <AlertTriangle className="w-5 h-5 text-red-400" />
        <span className="text-red-300">{error || "Imóvel não encontrado"}</span>
      </div>
    );
  }

  const status = STATUS_META[property.status || "AT"] || STATUS_META["AT"];

  return (
    <header className="px-6 py-5 bg-gradient-to-b from-slate-900/60 to-slate-900/20 border-b border-slate-800">
      <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
            <FileText className="w-3.5 h-3.5" />
            <span>CADASTRO AMBIENTAL RURAL</span>
            <span className={`px-2 py-0.5 rounded border text-[10px] font-medium tracking-wide ${status.color}`}>
              {status.label}
            </span>
            {property.tipo && (
              <span className="px-2 py-0.5 rounded border border-slate-700 text-slate-400 text-[10px]">
                {property.tipo}
              </span>
            )}
          </div>

          <h1 className="text-xl font-semibold text-slate-100 font-mono break-all flex items-center gap-2 group">
            {property.car_code}
            <button
              onClick={copyCode}
              className="opacity-0 group-hover:opacity-100 transition p-1 rounded hover:bg-slate-700/50 text-slate-400 hover:text-emerald-400"
              title="Copiar código CAR"
            >
              <Copy className="w-4 h-4" />
            </button>
            {copied && <span className="text-xs text-emerald-400">copiado!</span>}
          </h1>

          <div className="flex flex-wrap items-center gap-4 mt-3 text-sm text-slate-400">
            {property.municipio && (
              <span className="flex items-center gap-1.5">
                <MapPin className="w-4 h-4" />
                {property.municipio}
                {property.uf && ` — ${property.uf}`}
              </span>
            )}
            {!property.municipio && property.uf && (
              <span className="flex items-center gap-1.5">
                <MapPin className="w-4 h-4" />
                {property.uf}
              </span>
            )}
            {property.cod_municipio_ibge && (
              <span className="text-xs text-slate-500 font-mono">
                IBGE {property.cod_municipio_ibge}
              </span>
            )}
          </div>
        </div>

        <div className="flex gap-6 lg:gap-8">
          <MetricCard label="Área" value={formatArea(property.area_ha)} />
          <MetricCard
            label="Módulos Fiscais"
            value={(property.modulos_fiscais || 0).toFixed(2)}
          />
          <MetricCard
            label="Classificação"
            value={classifyArea(property.area_ha, property.modulos_fiscais)}
          />
        </div>
      </div>
    </header>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="text-right">
      <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">{label}</div>
      <div className="text-lg font-semibold text-slate-100 tabular-nums">{value}</div>
    </div>
  );
}

function formatArea(ha?: number): string {
  if (!ha) return "—";
  if (ha >= 10000) return `${(ha / 10000).toFixed(1)} mil ha`;
  if (ha < 1) return `${(ha * 10000).toFixed(0)} m²`;
  return `${ha.toFixed(2)} ha`;
}

function classifyArea(ha?: number, mf?: number): string {
  if (!mf) return "—";
  if (mf <= 1) return "Minifúndio";
  if (mf <= 4) return "Pequena";
  if (mf <= 15) return "Média";
  return "Grande";
}
