"use client";

import { useMemo, useState } from "react";
import { ChevronDown, ChevronUp, BarChart3 } from "lucide-react";
import { getLayer, LAYERS } from "@/lib/layers-catalog";

type FeatureSummary = {
  layerId: string;
  count: number;
};

/**
 * Dashboard inferior estilo MapBiomas: mostra contagens, totais e distribuição
 * das features visíveis no viewport atual. Recolhível.
 */
export function StatsDashboard({
  activeLayers,
  countsByLayer,
  zoom,
  totalFeatures,
}: {
  activeLayers: string[];
  countsByLayer: Record<string, number>;
  zoom: number;
  totalFeatures: number;
}) {
  const [open, setOpen] = useState(true);

  const summaries: FeatureSummary[] = useMemo(
    () =>
      activeLayers
        .map((id) => ({ layerId: id, count: countsByLayer[id] ?? 0 }))
        .sort((a, b) => b.count - a.count),
    [activeLayers, countsByLayer]
  );

  return (
    <div
      className={`absolute bottom-4 left-1/2 -translate-x-1/2 z-[800] rounded-2xl bg-background/92 backdrop-blur-2xl border border-border shadow-[0_-8px_40px_-8px_rgba(0,0,0,0.8)] transition-all duration-300 overflow-hidden ${
        open ? "w-[min(95vw,860px)]" : "w-auto"
      }`}
    >
      {/* Header */}
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between gap-4 px-4 py-2.5 hover:bg-muted/30 transition"
      >
        <div className="flex items-center gap-3">
          <BarChart3 className="h-4 w-4 text-primary" />
          <span className="text-sm font-semibold">Estatísticas</span>
          {!open && (
            <span className="text-[10px] font-mono text-muted-foreground">
              {totalFeatures.toLocaleString("pt-BR")} features em {activeLayers.length} camada(s)
            </span>
          )}
        </div>
        <div className="flex items-center gap-3">
          {open && (
            <span className="text-[10px] font-mono text-muted-foreground">
              Zoom {zoom} · {totalFeatures.toLocaleString("pt-BR")} features
            </span>
          )}
          {open ? (
            <ChevronDown className="h-4 w-4 text-muted-foreground" />
          ) : (
            <ChevronUp className="h-4 w-4 text-muted-foreground" />
          )}
        </div>
      </button>

      {open && (
        <div className="px-4 pb-4 pt-2 border-t border-border/50">
          {summaries.length === 0 ? (
            <div className="text-xs text-muted-foreground py-4 text-center">
              Ative camadas no painel esquerdo para ver estatísticas do viewport.
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 pt-1">
              {summaries.map((s) => {
                const cfg = getLayer(s.layerId);
                if (!cfg) return null;
                return (
                  <div
                    key={s.layerId}
                    className="p-2.5 rounded-lg border border-border/60 bg-card/50 flex items-start gap-2.5"
                  >
                    <div
                      className="w-2.5 h-2.5 mt-1 rounded-sm shrink-0"
                      style={{ backgroundColor: cfg.color }}
                    />
                    <div className="flex-1 min-w-0">
                      <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold truncate">
                        {cfg.name}
                      </div>
                      <div className="text-lg font-heading font-bold leading-tight">
                        {s.count.toLocaleString("pt-BR")}
                      </div>
                      <div className="text-[10px] text-muted-foreground">
                        {cfg.category}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
          <div className="text-[10px] text-muted-foreground mt-3 pt-2 border-t border-border/30">
            Contagens limitadas pelo <span className="font-mono">maxFeatures</span> de cada camada. Para dados completos, use a consulta por CAR no painel superior.
          </div>
        </div>
      )}
    </div>
  );
}
