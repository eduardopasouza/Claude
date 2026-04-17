"use client";

import useSWR from "swr";
import { FileWarning, Loader2 } from "lucide-react";
import { swrFetcher } from "@/lib/api";
import type { PropertyData } from "../PropertyHeader";

type OverlapFeature = {
  type: "Feature";
  properties: Record<string, string | number | null>;
  geometry: unknown;
};

type OverlapsResponse = {
  type: "FeatureCollection";
  features: OverlapFeature[];
  metadata: {
    car_code: string;
    total_features: number;
    layers_found: string[];
    layers_checked: string[];
  };
};

const LAYER_META: Record<
  string,
  { label: string; icon: string; gravity: string; color: string }
> = {
  terra_indigena: {
    label: "Terra Indígena",
    icon: "🪶",
    gravity: "Crítico — impede operação e crédito",
    color: "border-red-500/40 bg-red-950/30",
  },
  unidade_conservacao: {
    label: "Unidade de Conservação",
    icon: "🌲",
    gravity: "Alto — restringe uso e pode exigir desapropriação",
    color: "border-orange-500/40 bg-orange-950/30",
  },
  embargo_icmbio: {
    label: "Embargo ICMBio",
    icon: "🚫",
    gravity: "Crítico — área embargada judicialmente",
    color: "border-red-500/40 bg-red-950/30",
  },
  prodes: {
    label: "PRODES (desmatamento anual)",
    icon: "🌳",
    gravity: "Alto — desmatamento histórico consolidado",
    color: "border-orange-500/40 bg-orange-950/30",
  },
  deter_amazonia: {
    label: "DETER Amazônia (alerta)",
    icon: "⚠️",
    gravity: "Alto — alerta recente na Amazônia",
    color: "border-amber-500/40 bg-amber-950/30",
  },
  deter_cerrado: {
    label: "DETER Cerrado (alerta)",
    icon: "⚠️",
    gravity: "Alto — alerta recente no Cerrado",
    color: "border-amber-500/40 bg-amber-950/30",
  },
  mapbiomas_alerta: {
    label: "Alerta MapBiomas validado",
    icon: "🛰️",
    gravity: "Médio — cruzamento validado MapBiomas×CAR",
    color: "border-yellow-500/40 bg-yellow-950/30",
  },
  sigef: {
    label: "Parcela SIGEF",
    icon: "📐",
    gravity: "Informativo — sobreposição com parcela certificada INCRA",
    color: "border-sky-500/40 bg-sky-950/30",
  },
};

export function DossieTab({ property }: { property: PropertyData }) {
  const { data, error, isLoading } = useSWR<OverlapsResponse>(
    `/property/${property.car_code}/overlaps/geojson`,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  if (isLoading) {
    return (
      <div className="p-12 flex items-center justify-center text-slate-400">
        <Loader2 className="w-5 h-5 animate-spin mr-2" />
        Consultando 8 camadas PostGIS…
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-red-300">Erro ao carregar sobreposições</div>
    );
  }

  // Group features by layer
  const groups: Record<string, OverlapFeature[]> = {};
  for (const feat of data?.features || []) {
    const layer = String(feat.properties.layer || "outros");
    if (!groups[layer]) groups[layer] = [];
    groups[layer].push(feat);
  }

  const total = data?.features.length || 0;

  return (
    <div className="p-6 space-y-5">
      <div className="flex items-baseline justify-between">
        <h2 className="text-lg font-semibold text-slate-100">
          Dossiê Ambiental & Fundiário
        </h2>
        <span className="text-sm text-slate-400">
          {total} {total === 1 ? "sobreposição" : "sobreposições"} detectadas
        </span>
      </div>

      {total === 0 ? (
        <div className="bg-emerald-950/20 border border-emerald-900/40 rounded-xl p-8 text-center">
          <div className="text-5xl mb-3">✅</div>
          <h3 className="text-emerald-300 font-semibold mb-1">
            Nenhuma sobreposição crítica detectada
          </h3>
          <p className="text-sm text-slate-400">
            Verificadas as 8 camadas de risco: Terras Indígenas, Unidades de
            Conservação, Embargos ICMBio, PRODES, DETER Amazônia/Cerrado,
            MapBiomas e SIGEF.
          </p>
        </div>
      ) : (
        Object.entries(groups).map(([layer, feats]) => {
          const meta =
            LAYER_META[layer] || {
              label: layer,
              icon: "📍",
              gravity: "—",
              color: "border-slate-700 bg-slate-900/30",
            };
          return (
            <section
              key={layer}
              className={`border rounded-xl p-4 ${meta.color}`}
            >
              <header className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{meta.icon}</span>
                  <div>
                    <h3 className="font-semibold text-slate-100">
                      {meta.label}
                    </h3>
                    <p className="text-xs text-slate-400">{meta.gravity}</p>
                  </div>
                </div>
                <span className="text-lg font-bold text-slate-100 tabular-nums">
                  {feats.length}
                </span>
              </header>
              <div className="divide-y divide-slate-800/60">
                {feats.slice(0, 8).map((f, idx) => (
                  <div
                    key={idx}
                    className="py-2 text-sm flex flex-wrap gap-x-4 gap-y-1"
                  >
                    {Object.entries(f.properties)
                      .filter(([k]) => !["layer", "color"].includes(k))
                      .slice(0, 5)
                      .map(([k, v]) => (
                        <span key={k} className="text-slate-300">
                          <span className="text-slate-500">{k}:</span>{" "}
                          <span className="font-medium">{String(v || "—")}</span>
                        </span>
                      ))}
                  </div>
                ))}
                {feats.length > 8 && (
                  <div className="py-2 text-xs text-slate-500">
                    + {feats.length - 8} mais…
                  </div>
                )}
              </div>
            </section>
          );
        })
      )}

      <footer className="text-xs text-slate-500 flex items-center gap-1">
        <FileWarning className="w-3.5 h-3.5" />
        Camadas consultadas: {data?.metadata.layers_checked.join(", ")}
      </footer>
    </div>
  );
}
