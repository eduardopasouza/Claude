"use client";

import { useMemo, useState } from "react";
import {
  ChevronDown,
  ChevronUp,
  BarChart3,
  EyeOff,
  PieChart,
} from "lucide-react";
import { getLayer, THEMES } from "@/lib/layers-catalog";

/**
 * Dashboard inferior estilo MapBiomas:
 * - barras horizontais proporcionais com cor da camada
 * - total geral + dropdown com agregação por tema
 * - cada linha é interativa (hover destaca, X desativa a camada)
 * - altura fixa com scroll interno quando muitas camadas
 */
export function StatsDashboard({
  activeLayers,
  countsByLayer,
  zoom,
  totalFeatures,
  onToggleLayer,
}: {
  activeLayers: string[];
  countsByLayer: Record<string, number>;
  zoom: number;
  totalFeatures: number;
  onToggleLayer?: (id: string) => void;
}) {
  const [open, setOpen] = useState(true);
  const [groupBy, setGroupBy] = useState<"camada" | "tema">("camada");

  const { byLayer, byTheme, maxCount } = useMemo(() => {
    const byLayer = activeLayers
      .map((id) => {
        const cfg = getLayer(id);
        return {
          id,
          cfg,
          count: countsByLayer[id] ?? 0,
        };
      })
      .filter((x) => x.cfg)
      .sort((a, b) => b.count - a.count);

    const byTheme = new Map<string, { count: number; layers: string[]; color: string; label: string }>();
    for (const r of byLayer) {
      if (!r.cfg) continue;
      const t = THEMES.find((t) => t.id === r.cfg!.category);
      const key = r.cfg.category;
      const cur = byTheme.get(key) || {
        count: 0,
        layers: [],
        color: t?.color || "#64748b",
        label: t?.label || key,
      };
      cur.count += r.count;
      cur.layers.push(r.id);
      byTheme.set(key, cur);
    }

    const maxCount = Math.max(1, ...byLayer.map((r) => r.count));
    return { byLayer, byTheme, maxCount };
  }, [activeLayers, countsByLayer]);

  const themeRows = useMemo(
    () =>
      Array.from(byTheme.entries())
        .map(([id, v]) => ({ id, ...v }))
        .sort((a, b) => b.count - a.count),
    [byTheme],
  );

  const maxThemeCount = Math.max(1, ...themeRows.map((r) => r.count));

  return (
    <div
      className={`absolute bottom-4 left-1/2 -translate-x-1/2 z-[800] rounded-2xl bg-background/94 backdrop-blur-2xl border border-border shadow-[0_-8px_40px_-8px_rgba(0,0,0,0.8)] transition-all duration-300 overflow-hidden ${
        open ? "w-[min(96vw,920px)]" : "w-auto"
      }`}
    >
      {/* Header compacto */}
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between gap-4 px-4 py-2 hover:bg-muted/30 transition"
      >
        <div className="flex items-center gap-2.5">
          <BarChart3 className="h-4 w-4 text-primary" />
          <span className="text-sm font-semibold">Estatísticas do viewport</span>
          <span className="text-[10px] font-mono text-muted-foreground border border-border rounded px-1.5 py-0.5">
            Z{zoom}
          </span>
          {!open && activeLayers.length > 0 && (
            <span className="text-[10px] font-mono text-muted-foreground">
              {totalFeatures.toLocaleString("pt-BR")} features · {activeLayers.length} camada{activeLayers.length > 1 ? "s" : ""}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {open && (
            <span className="text-[10px] font-mono font-bold text-primary">
              {totalFeatures.toLocaleString("pt-BR")} features
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
        <div className="border-t border-border/50">
          {/* Tabs group-by */}
          {byLayer.length > 0 && (
            <div className="px-4 pt-2 pb-1 flex items-center gap-2">
              <div className="flex rounded-md border border-border overflow-hidden text-[10px] uppercase tracking-wider font-semibold">
                <button
                  onClick={() => setGroupBy("camada")}
                  className={`px-2.5 py-1 transition ${
                    groupBy === "camada"
                      ? "bg-primary/20 text-primary"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  Por camada
                </button>
                <button
                  onClick={() => setGroupBy("tema")}
                  className={`px-2.5 py-1 transition border-l border-border ${
                    groupBy === "tema"
                      ? "bg-primary/20 text-primary"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  Por tema
                </button>
              </div>
              {groupBy === "camada" && (
                <span className="text-[10px] text-muted-foreground ml-auto">
                  {byLayer.length} camada{byLayer.length > 1 ? "s" : ""} ativa{byLayer.length > 1 ? "s" : ""}
                </span>
              )}
              {groupBy === "tema" && (
                <span className="text-[10px] text-muted-foreground ml-auto">
                  {themeRows.length} tema{themeRows.length > 1 ? "s" : ""}
                </span>
              )}
            </div>
          )}

          {/* Body com barras proporcionais */}
          <div className="px-3 pb-3 pt-1.5 max-h-[40vh] overflow-y-auto custom-scrollbar">
            {byLayer.length === 0 ? (
              <div className="text-xs text-muted-foreground py-6 text-center flex items-center justify-center gap-2">
                <PieChart className="h-4 w-4" />
                Ative camadas no painel esquerdo para ver distribuição no viewport.
              </div>
            ) : groupBy === "camada" ? (
              <div className="space-y-1">
                {byLayer.map((r) => {
                  if (!r.cfg) return null;
                  const pct = (r.count / maxCount) * 100;
                  const pctTotal = totalFeatures
                    ? (r.count / totalFeatures) * 100
                    : 0;
                  return (
                    <div
                      key={r.id}
                      className="group flex items-center gap-2.5 py-1 px-2 rounded hover:bg-muted/30 transition"
                    >
                      <div
                        className="w-2.5 h-2.5 rounded-sm shrink-0"
                        style={{ backgroundColor: r.cfg.color }}
                      />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-baseline justify-between gap-2 mb-1">
                          <span className="text-xs font-medium truncate">
                            {r.cfg.name}
                          </span>
                          <span className="text-xs font-mono tabular-nums shrink-0">
                            {r.count.toLocaleString("pt-BR")}
                            <span className="text-[10px] text-muted-foreground ml-1.5">
                              {pctTotal.toFixed(1)}%
                            </span>
                          </span>
                        </div>
                        {/* Barra proporcional */}
                        <div className="h-1 bg-muted/40 rounded overflow-hidden">
                          <div
                            className="h-full rounded transition-all duration-500"
                            style={{
                              width: `${pct}%`,
                              backgroundColor: r.cfg.color,
                              opacity: r.count > 0 ? 0.85 : 0,
                            }}
                          />
                        </div>
                      </div>
                      {onToggleLayer && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onToggleLayer(r.id);
                          }}
                          className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-muted text-muted-foreground hover:text-foreground transition"
                          title="Desativar camada"
                        >
                          <EyeOff className="h-3 w-3" />
                        </button>
                      )}
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="space-y-1">
                {themeRows.map((r) => {
                  const pct = (r.count / maxThemeCount) * 100;
                  const pctTotal = totalFeatures
                    ? (r.count / totalFeatures) * 100
                    : 0;
                  return (
                    <div
                      key={r.id}
                      className="flex items-center gap-2.5 py-1 px-2 rounded hover:bg-muted/30 transition"
                    >
                      <div
                        className="w-2.5 h-2.5 rounded-sm shrink-0"
                        style={{ backgroundColor: r.color }}
                      />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-baseline justify-between gap-2 mb-1">
                          <span className="text-xs font-medium truncate">
                            {r.label}
                            <span className="text-[10px] text-muted-foreground ml-1.5 font-mono">
                              {r.layers.length} camada{r.layers.length > 1 ? "s" : ""}
                            </span>
                          </span>
                          <span className="text-xs font-mono tabular-nums shrink-0">
                            {r.count.toLocaleString("pt-BR")}
                            <span className="text-[10px] text-muted-foreground ml-1.5">
                              {pctTotal.toFixed(1)}%
                            </span>
                          </span>
                        </div>
                        <div className="h-1 bg-muted/40 rounded overflow-hidden">
                          <div
                            className="h-full rounded transition-all duration-500"
                            style={{
                              width: `${pct}%`,
                              backgroundColor: r.color,
                              opacity: 0.85,
                            }}
                          />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Footer */}
          {byLayer.length > 0 && (
            <div className="px-4 py-1.5 border-t border-border/30 text-[10px] text-muted-foreground flex items-center justify-between">
              <span>
                Contagem limitada pelo <code className="font-mono">maxFeatures</code> por camada
              </span>
              <span className="font-mono tabular-nums">
                Total: {totalFeatures.toLocaleString("pt-BR")}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
