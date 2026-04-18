"use client";

import useSWR from "swr";
import { CloudSun, Loader2, Droplets, Thermometer, Wind } from "lucide-react";
import { swrFetcher } from "@/lib/api";
import type { PropertyData } from "../PropertyHeader";

type NasaPowerResponse = {
  location?: { latitude: number; longitude: number };
  data?: Array<{
    date: string;
    temperature?: number;
    temperature_max?: number;
    temperature_min?: number;
    precipitation?: number;
    humidity?: number;
    wind?: number;
  }>;
  summary?: {
    temperature_avg?: number;
    precipitation_total?: number;
    precipitation_avg_daily?: number;
  };
  error?: string;
};

export function ClimaTab({ property }: { property: PropertyData }) {
  const hasCoords = property.centroid?.lat && property.centroid?.lon;

  const endpoint = hasCoords
    ? `/geo/nasa-power?lat=${property.centroid!.lat}&lon=${property.centroid!.lon}&days=30`
    : null;

  const { data, error, isLoading } = useSWR<NasaPowerResponse>(
    endpoint,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  if (!hasCoords) {
    return (
      <div className="p-8 text-sm text-slate-400 text-center">
        Centroide do imóvel não disponível — não é possível consultar clima.
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="p-12 flex items-center justify-center text-slate-400">
        <Loader2 className="w-5 h-5 animate-spin mr-2" />
        Consultando NASA POWER…
      </div>
    );
  }

  if (error || data?.error) {
    return (
      <div className="p-6 text-red-300">
        Erro ao consultar NASA POWER: {data?.error || "timeout"}
      </div>
    );
  }

  const series = data?.data || [];
  const temp = data?.summary?.temperature_avg;
  const precipTotal = data?.summary?.precipitation_total;
  const precipDaily = data?.summary?.precipitation_avg_daily;

  // Agrupa por dia para visualização da chuva
  const maxPrecip = Math.max(1, ...series.map((d) => d.precipitation || 0));

  return (
    <div className="p-6 space-y-5">
      <header className="flex items-baseline justify-between">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <CloudSun className="w-5 h-5 text-emerald-400" />
          Clima (últimos 30 dias)
        </h2>
        <span className="text-xs text-slate-500">
          NASA POWER · {property.centroid!.lat.toFixed(3)},{" "}
          {property.centroid!.lon.toFixed(3)}
        </span>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard
          icon={Thermometer}
          label="Temperatura média"
          value={temp ? `${temp.toFixed(1)} °C` : "—"}
          color="text-orange-400"
        />
        <StatCard
          icon={Droplets}
          label="Precipitação total"
          value={precipTotal ? `${precipTotal.toFixed(1)} mm` : "—"}
          color="text-sky-400"
        />
        <StatCard
          icon={Wind}
          label="Precipitação média/dia"
          value={precipDaily ? `${precipDaily.toFixed(2)} mm` : "—"}
          color="text-cyan-400"
        />
      </div>

      {/* Mini-gráfico de barras da precipitação diária */}
      {series.length > 0 && (
        <section className="bg-slate-900/40 border border-slate-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-slate-200 mb-4">
            Chuva diária (mm)
          </h3>
          <div className="flex items-end gap-0.5 h-32">
            {series.map((d, i) => {
              const pct = ((d.precipitation || 0) / maxPrecip) * 100;
              return (
                <div
                  key={i}
                  className="flex-1 bg-sky-500/30 border-t border-sky-400 rounded-t"
                  style={{ height: `${pct}%`, minHeight: "2px" }}
                  title={`${d.date}: ${(d.precipitation || 0).toFixed(1)} mm`}
                />
              );
            })}
          </div>
          <div className="flex justify-between text-[10px] text-slate-500 mt-1">
            <span>{series[0]?.date || "—"}</span>
            <span>{series[series.length - 1]?.date || "—"}</span>
          </div>
        </section>
      )}

      <footer className="text-xs text-slate-500">
        Próximo: integrar estação INMET mais próxima + alertas CEMADEN + mapas
        de anomalia de SPI/SPEI.
      </footer>
    </div>
  );
}

function StatCard({
  icon: Icon,
  label,
  value,
  color,
}: {
  icon: typeof CloudSun;
  label: string;
  value: string;
  color: string;
}) {
  return (
    <div className="bg-slate-900/40 border border-slate-800 rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs uppercase tracking-wider text-slate-500">
          {label}
        </span>
        <Icon className={`w-4 h-4 ${color}`} />
      </div>
      <div className="text-xl font-semibold text-slate-100 tabular-nums">
        {value}
      </div>
    </div>
  );
}
