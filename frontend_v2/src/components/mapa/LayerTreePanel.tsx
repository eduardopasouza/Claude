"use client";

import { useState, useMemo } from "react";
import {
  ChevronDown,
  ChevronRight,
  Layers as LayersIcon,
  Lock,
  Search,
  X,
  Clock,
  ChevronsLeft,
  ChevronsRight,
} from "lucide-react";
import { LAYERS, THEMES, LayerCategory, LayerConfig } from "@/lib/layers-catalog";

export function LayerTreePanel({
  activeLayers,
  onToggle,
  zoom,
  collapsed: controlledCollapsed,
  onCollapsedChange,
}: {
  activeLayers: string[];
  onToggle: (id: string) => void;
  zoom: number;
  collapsed?: boolean;
  onCollapsedChange?: (v: boolean) => void;
}) {
  const [internalCollapsed, setInternalCollapsed] = useState(false);
  const collapsed = controlledCollapsed ?? internalCollapsed;
  const setCollapsed = (v: boolean) => {
    setInternalCollapsed(v);
    onCollapsedChange?.(v);
  };
  const [openThemes, setOpenThemes] = useState<Record<string, boolean>>({
    fundiario: true,
    ambiental: true,
  });
  const [query, setQuery] = useState("");

  const grouped = useMemo(() => {
    const q = query.trim().toLowerCase();
    const filter = (l: LayerConfig) =>
      !q ||
      l.name.toLowerCase().includes(q) ||
      l.description.toLowerCase().includes(q);
    return THEMES.map((theme) => ({
      theme,
      layers: LAYERS.filter((l) => l.category === theme.id && filter(l)),
    })).filter((g) => g.layers.length > 0);
  }, [query]);

  const activeCount = activeLayers.length;

  // ==== COLAPSADO ====
  if (collapsed) {
    return (
      <button
        onClick={() => setCollapsed(false)}
        className="absolute top-6 left-6 z-[850] rounded-xl bg-background/92 backdrop-blur-2xl border border-border shadow-[0_8px_40px_-10px_rgba(0,0,0,0.8)] hover:border-primary/50 transition group"
        title="Abrir painel de camadas"
      >
        <div className="p-3 flex items-center gap-2">
          <LayersIcon className="h-4 w-4 text-primary" />
          <div className="flex flex-col items-start">
            <span className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
              Camadas
            </span>
            <span className="text-[10px] font-mono text-muted-foreground">
              Z{zoom} {activeCount > 0 && `· ${activeCount} ativa${activeCount > 1 ? "s" : ""}`}
            </span>
          </div>
          <ChevronsRight className="h-3.5 w-3.5 text-muted-foreground group-hover:text-primary transition" />
        </div>
      </button>
    );
  }

  return (
    <div className="absolute top-6 left-6 z-[850] w-[340px] max-h-[calc(100vh-11rem)] flex flex-col rounded-2xl bg-background/92 backdrop-blur-2xl border border-border shadow-[0_8px_40px_-10px_rgba(0,0,0,0.8)]">
      {/* Header */}
      <div className="p-4 border-b border-border/60">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <LayersIcon className="h-4 w-4 text-primary" />
            <h2 className="font-heading font-bold text-sm">Camadas</h2>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-mono text-muted-foreground border border-border rounded px-1.5 py-0.5">
              Z{zoom}
            </span>
            {activeCount > 0 && (
              <span className="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-primary/20 text-primary border border-primary/30">
                {activeCount} ativa{activeCount > 1 ? "s" : ""}
              </span>
            )}
            <button
              onClick={() => setCollapsed(true)}
              className="p-1 rounded hover:bg-muted text-muted-foreground hover:text-foreground transition"
              title="Recolher painel"
            >
              <ChevronsLeft className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar camada..."
            className="w-full bg-input/40 border border-border rounded-lg pl-8 pr-7 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-primary"
          />
          {query && (
            <button
              onClick={() => setQuery("")}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
            >
              <X className="h-3.5 w-3.5" />
            </button>
          )}
        </div>
      </div>

      {/* Tree */}
      <div className="flex-1 overflow-y-auto p-2 space-y-1 custom-scrollbar">
        {grouped.map(({ theme, layers }) => {
          const isOpen = openThemes[theme.id] ?? false;
          const Icon = theme.icon;
          const activeInGroup = layers.filter((l) =>
            activeLayers.includes(l.id)
          ).length;

          return (
            <div key={theme.id}>
              <button
                onClick={() =>
                  setOpenThemes((prev) => ({ ...prev, [theme.id]: !isOpen }))
                }
                className="w-full flex items-center gap-2 px-2 py-2 rounded-lg hover:bg-muted/40 transition text-left"
              >
                {isOpen ? (
                  <ChevronDown className="h-3.5 w-3.5 text-muted-foreground" />
                ) : (
                  <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />
                )}
                <Icon className="h-3.5 w-3.5" style={{ color: theme.color }} />
                <span className="text-xs font-semibold flex-1">{theme.label}</span>
                <span className="text-[10px] text-muted-foreground font-mono">
                  {activeInGroup > 0 ? `${activeInGroup}/` : ""}
                  {layers.length}
                </span>
              </button>

              {isOpen && (
                <div className="ml-4 space-y-0.5 mt-0.5 mb-1">
                  {layers.map((layer) => (
                    <LayerRow
                      key={layer.id}
                      layer={layer}
                      active={activeLayers.includes(layer.id)}
                      zoom={zoom}
                      onToggle={() => onToggle(layer.id)}
                    />
                  ))}
                </div>
              )}
            </div>
          );
        })}

        {grouped.length === 0 && query && (
          <div className="text-xs text-muted-foreground py-6 text-center">
            Nenhuma camada encontrada para &quot;{query}&quot;.
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-3 border-t border-border/60 text-[10px] text-muted-foreground flex items-center justify-between">
        <span>{LAYERS.length} camadas no catálogo</span>
        <span className="font-mono">
          {LAYERS.filter((l) => l.comingSoon).length} em roadmap
        </span>
      </div>
    </div>
  );
}

function LayerRow({
  layer,
  active,
  zoom,
  onToggle,
}: {
  layer: LayerConfig;
  active: boolean;
  zoom: number;
  onToggle: () => void;
}) {
  const locked = zoom < layer.minZoom;
  const disabled = layer.comingSoon;

  return (
    <button
      onClick={onToggle}
      disabled={disabled || locked}
      title={
        disabled
          ? "Em roadmap"
          : locked
          ? `Zoom mínimo Z${layer.minZoom}`
          : layer.description
      }
      className={`w-full flex items-start gap-2 px-2 py-1.5 rounded-md text-left transition group ${
        disabled
          ? "opacity-40 cursor-not-allowed"
          : locked
          ? "opacity-50 cursor-not-allowed"
          : active
          ? "bg-primary/10 hover:bg-primary/20"
          : "hover:bg-muted/40"
      }`}
    >
      <div
        className={`mt-1 w-3 h-3 rounded-sm shrink-0 border transition ${
          active
            ? "border-primary ring-2 ring-primary/30"
            : "border-border"
        }`}
        style={{ backgroundColor: active ? layer.color : "transparent" }}
      />
      <div className="flex-1 min-w-0">
        <div className="text-xs font-medium leading-tight flex items-center gap-1.5">
          <span className="truncate">{layer.name}</span>
          {layer.comingSoon && (
            <Clock className="h-3 w-3 text-muted-foreground shrink-0" />
          )}
          {locked && !disabled && (
            <Lock className="h-3 w-3 text-rose-400 shrink-0" />
          )}
        </div>
        <div className="text-[10px] text-muted-foreground line-clamp-1">
          {layer.description}
        </div>
      </div>
    </button>
  );
}
