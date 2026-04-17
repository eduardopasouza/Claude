"use client";

import useSWR from "swr";
import { Loader2, History, ExternalLink } from "lucide-react";
import { swrFetcher } from "@/lib/api";
import type { PropertyData } from "../PropertyHeader";

type MapBiomasProperty = {
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

export function HistoricoTab({ property }: { property: PropertyData }) {
  const { data, isLoading, error } = useSWR<MapBiomasProperty>(
    `/mapbiomas/property/${property.car_code}`,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  if (isLoading) {
    return (
      <div className="p-12 flex items-center justify-center text-slate-400">
        <Loader2 className="w-5 h-5 animate-spin mr-2" />
        Consultando API MapBiomas Alerta…
      </div>
    );
  }

  if (error) {
    return <div className="p-6 text-red-300">Erro ao consultar MapBiomas</div>;
  }

  const alerts = data?.ruralProperty?.alerts || [];
  const prop = data?.ruralProperty;

  // Group by year-month
  const byYearMonth: Record<string, typeof alerts> = {};
  for (const a of alerts) {
    const ym = a.detectedAt.slice(0, 7); // YYYY-MM
    (byYearMonth[ym] ||= []).push(a);
  }
  const sortedMonths = Object.keys(byYearMonth).sort().reverse();
  const totalArea = alerts.reduce((s, a) => s + (a.areaHa || 0), 0);

  return (
    <div className="p-6 space-y-5">
      <header className="flex items-baseline justify-between">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <History className="w-5 h-5 text-emerald-400" />
          Histórico MapBiomas Alerta
        </h2>
        <a
          href={`https://plataforma.alerta.mapbiomas.org/alertas?propertyCode=${property.car_code}`}
          target="_blank"
          rel="noreferrer"
          className="text-xs text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
        >
          Ver na plataforma oficial <ExternalLink className="w-3 h-3" />
        </a>
      </header>

      {prop && (
        <div className="grid grid-cols-3 gap-4 bg-slate-900/40 border border-slate-800 rounded-xl p-4">
          <StatMini label="Total de alertas" value={alerts.length.toString()} />
          <StatMini label="Área afetada" value={`${totalArea.toFixed(2)} ha`} />
          <StatMini
            label="% do imóvel afetado"
            value={
              prop.areaHa
                ? `${((totalArea / prop.areaHa) * 100).toFixed(1)}%`
                : "—"
            }
          />
        </div>
      )}

      {alerts.length === 0 ? (
        <div className="bg-emerald-950/20 border border-emerald-900/40 rounded-xl p-8 text-center">
          <div className="text-5xl mb-3">🌱</div>
          <h3 className="text-emerald-300 font-semibold mb-1">
            Sem alertas no MapBiomas Alerta
          </h3>
          <p className="text-sm text-slate-400">
            Nenhum alerta de desmatamento (SAD, DETER, GLAD, SIRAD-X) foi
            publicado para este CAR.
          </p>
        </div>
      ) : (
        <ol className="relative border-l border-slate-700 ml-3 space-y-4">
          {sortedMonths.map((ym) => {
            const monthAlerts = byYearMonth[ym];
            const monthArea = monthAlerts.reduce(
              (s, a) => s + (a.areaHa || 0),
              0
            );
            return (
              <li key={ym} className="ml-6">
                <span className="absolute -left-1.5 w-3 h-3 bg-emerald-500 rounded-full border-2 border-slate-950" />
                <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
                  <div className="flex items-baseline justify-between mb-2">
                    <h3 className="font-semibold text-slate-200">
                      {formatMonth(ym)}
                    </h3>
                    <span className="text-sm text-slate-400">
                      {monthAlerts.length} alerta(s) · {monthArea.toFixed(2)} ha
                    </span>
                  </div>
                  <ul className="space-y-1 text-sm">
                    {monthAlerts.map((a) => (
                      <li
                        key={a.alertCode}
                        className="flex items-center justify-between py-1 border-t border-slate-800 first:border-0"
                      >
                        <span className="font-mono text-xs text-slate-500">
                          #{a.alertCode}
                        </span>
                        <span className="text-slate-300">
                          {a.detectedAt} · {a.areaHa.toFixed(3)} ha
                        </span>
                        <span className="text-xs text-slate-500">
                          {a.sources.join(" · ")}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              </li>
            );
          })}
        </ol>
      )}
    </div>
  );
}

function StatMini({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">
        {label}
      </div>
      <div className="text-lg font-semibold text-slate-100 tabular-nums">
        {value}
      </div>
    </div>
  );
}

function formatMonth(ym: string): string {
  const [y, m] = ym.split("-");
  const months = [
    "jan",
    "fev",
    "mar",
    "abr",
    "mai",
    "jun",
    "jul",
    "ago",
    "set",
    "out",
    "nov",
    "dez",
  ];
  return `${months[parseInt(m) - 1]}/${y}`;
}
