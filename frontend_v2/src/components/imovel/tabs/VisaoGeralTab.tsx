"use client";

import useSWR from "swr";
import {
  AlertTriangle,
  CheckCircle2,
  Flame,
  Leaf,
  ShieldAlert,
  TrendingDown,
  TreePalm,
  Trees,
} from "lucide-react";
import { swrFetcher } from "@/lib/api";
import type { PropertyData } from "../PropertyHeader";

type OverlapsData = {
  type: string;
  features: Array<{
    type: string;
    properties: Record<string, unknown>;
    geometry: unknown;
  }>;
  metadata: {
    car_code: string;
    total_features: number;
    layers_found: string[];
    layers_checked: string[];
  };
};

type MapBiomasData = {
  ruralProperty?: {
    propertyCode: string;
    areaHa: number;
    alerts?: Array<{
      alertCode: number;
      detectedAt: string;
      areaHa: number;
      sources: string[];
    }>;
  } | null;
};

export function VisaoGeralTab({ property }: { property: PropertyData }) {
  const { data: overlaps } = useSWR<OverlapsData>(
    `/property/${property.car_code}/overlaps/geojson`,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  const { data: mapbiomas } = useSWR<MapBiomasData>(
    `/mapbiomas/property/${property.car_code}`,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  const layers = overlaps?.metadata.layers_found || [];
  const alertsTempoReal = mapbiomas?.ruralProperty?.alerts || [];

  const risks = computeRisks(layers);
  const score = computeScore(risks, alertsTempoReal.length);

  return (
    <div className="p-6 space-y-6">
      {/* Score de compliance + status rápido */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-1 bg-gradient-to-br from-slate-900/60 to-slate-900/20 border border-slate-800 rounded-xl p-5">
          <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">
            Score de Compliance
          </div>
          <div className="flex items-end gap-2">
            <span
              className={`text-5xl font-bold tabular-nums ${
                score >= 80
                  ? "text-emerald-400"
                  : score >= 50
                  ? "text-amber-400"
                  : "text-red-400"
              }`}
            >
              {score}
            </span>
            <span className="text-lg text-slate-500 mb-2">/100</span>
          </div>
          <div className="mt-3 text-sm text-slate-400">
            {score >= 80
              ? "Baixo risco — apto a crédito e operações"
              : score >= 50
              ? "Risco moderado — exige due diligence"
              : "Alto risco — múltiplos bloqueadores"}
          </div>
        </div>

        <div className="lg:col-span-2 grid grid-cols-2 md:grid-cols-4 gap-3">
          <KpiCard
            icon={Trees}
            label="TI sobreposta"
            value={risks.terra_indigena ? "SIM" : "Não"}
            level={risks.terra_indigena ? "critical" : "ok"}
          />
          <KpiCard
            icon={TreePalm}
            label="UC sobreposta"
            value={risks.unidade_conservacao ? "SIM" : "Não"}
            level={risks.unidade_conservacao ? "high" : "ok"}
          />
          <KpiCard
            icon={ShieldAlert}
            label="Embargo ICMBio"
            value={risks.embargo_icmbio ? "SIM" : "Não"}
            level={risks.embargo_icmbio ? "critical" : "ok"}
          />
          <KpiCard
            icon={Flame}
            label="Alertas tempo real"
            value={alertsTempoReal.length}
            level={alertsTempoReal.length > 0 ? "high" : "ok"}
          />
          <KpiCard
            icon={TrendingDown}
            label="PRODES (desmat.)"
            value={risks.prodes ? "SIM" : "Não"}
            level={risks.prodes ? "high" : "ok"}
          />
          <KpiCard
            icon={AlertTriangle}
            label="DETER"
            value={
              risks.deter_amazonia || risks.deter_cerrado ? "SIM" : "Não"
            }
            level={risks.deter_amazonia || risks.deter_cerrado ? "high" : "ok"}
          />
          <KpiCard
            icon={Leaf}
            label="MapBiomas"
            value={risks.mapbiomas_alerta ? "SIM" : "Não"}
            level={risks.mapbiomas_alerta ? "medium" : "ok"}
          />
          <KpiCard
            icon={CheckCircle2}
            label="SIGEF sobrep."
            value={risks.sigef ? "SIM" : "Não"}
            level={risks.sigef ? "info" : "ok"}
          />
        </div>
      </div>

      {/* Resumo das sobreposições */}
      <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-5">
        <h3 className="text-sm font-semibold text-slate-200 mb-3">
          Camadas verificadas ({overlaps?.metadata.layers_checked.length || 0})
        </h3>
        <div className="flex flex-wrap gap-2">
          {overlaps?.metadata.layers_checked.map((layer) => {
            const found = layers.includes(layer);
            return (
              <span
                key={layer}
                className={`
                  text-xs px-3 py-1.5 rounded-full border
                  ${
                    found
                      ? "bg-red-500/10 border-red-500/30 text-red-300"
                      : "bg-slate-800/50 border-slate-700 text-slate-500"
                  }
                `}
              >
                {found && "⚠ "}
                {layer.replace(/_/g, " ")}
              </span>
            );
          })}
        </div>
      </div>

      {/* Alertas MapBiomas tempo real */}
      {alertsTempoReal.length > 0 && (
        <div className="bg-red-950/20 border border-red-900/40 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-red-300 mb-3 flex items-center gap-2">
            <Flame className="w-4 h-4" />
            Alertas MapBiomas recentes ({alertsTempoReal.length})
          </h3>
          <ul className="space-y-2">
            {alertsTempoReal.slice(0, 5).map((alert) => (
              <li
                key={alert.alertCode}
                className="flex justify-between text-sm bg-slate-900/50 rounded px-3 py-2"
              >
                <span className="text-slate-400 font-mono">
                  #{alert.alertCode}
                </span>
                <span className="text-slate-300">
                  {alert.detectedAt} · {alert.areaHa.toFixed(2)} ha
                </span>
                <span className="text-xs text-slate-500">
                  {alert.sources.join(", ")}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {layers.length === 0 && alertsTempoReal.length === 0 && overlaps && (
        <div className="bg-emerald-950/20 border border-emerald-900/40 rounded-xl p-5 flex items-center gap-3">
          <CheckCircle2 className="w-6 h-6 text-emerald-400 flex-shrink-0" />
          <div>
            <h3 className="text-sm font-semibold text-emerald-300">
              Nenhuma sobreposição crítica detectada
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              O imóvel não se sobrepõe a Terras Indígenas, UCs, embargos, alertas
              PRODES/DETER/MapBiomas ou parcelas SIGEF conflitantes.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

type RiskLevel = "ok" | "info" | "medium" | "high" | "critical";

function KpiCard({
  icon: Icon,
  label,
  value,
  level,
}: {
  icon: typeof AlertTriangle;
  label: string;
  value: string | number;
  level: RiskLevel;
}) {
  const colors: Record<RiskLevel, string> = {
    ok: "border-slate-800 bg-slate-900/40 text-slate-300",
    info: "border-sky-500/30 bg-sky-950/20 text-sky-300",
    medium: "border-amber-500/30 bg-amber-950/20 text-amber-300",
    high: "border-orange-500/30 bg-orange-950/20 text-orange-300",
    critical: "border-red-500/40 bg-red-950/30 text-red-300",
  };
  return (
    <div className={`border rounded-lg p-3 ${colors[level]}`}>
      <div className="flex items-center justify-between mb-1">
        <Icon className="w-4 h-4 opacity-60" />
      </div>
      <div className="text-[10px] uppercase tracking-wider opacity-70">
        {label}
      </div>
      <div className="text-base font-semibold mt-0.5">{value}</div>
    </div>
  );
}

function computeRisks(layers: string[]): Record<string, boolean> {
  return {
    terra_indigena: layers.includes("terras_indigenas"),
    unidade_conservacao: layers.includes("unidades_conservacao"),
    embargo_icmbio: layers.includes("embargos_icmbio"),
    prodes: layers.includes("prodes"),
    deter_amazonia: layers.includes("deter_amazonia"),
    deter_cerrado: layers.includes("deter_cerrado"),
    mapbiomas_alerta: layers.includes("mapbiomas_alertas"),
    sigef: layers.includes("sigef_parcelas"),
  };
}

function computeScore(
  risks: Record<string, boolean>,
  alertsCount: number
): number {
  let score = 100;
  if (risks.terra_indigena) score -= 40;
  if (risks.unidade_conservacao) score -= 25;
  if (risks.embargo_icmbio) score -= 35;
  if (risks.prodes) score -= 15;
  if (risks.deter_amazonia) score -= 15;
  if (risks.deter_cerrado) score -= 10;
  if (risks.mapbiomas_alerta) score -= 10;
  if (alertsCount > 0) score -= Math.min(alertsCount * 5, 20);
  return Math.max(0, score);
}
