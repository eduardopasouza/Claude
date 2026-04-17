"use client";

import { ExternalLink, FileText, Gavel, ScanEye, ShieldAlert, X } from "lucide-react";
import { getLayer } from "@/lib/layers-catalog";

export type InspectorPayload = {
  layerId: string;
  properties: Record<string, unknown>;
  /** Opcional: coordenada de origem do clique */
  latlng?: { lat: number; lng: number };
};

export function LayerInspector({
  data,
  onClose,
}: {
  data: InspectorPayload | null;
  onClose: () => void;
}) {
  if (!data) return null;
  const cfg = getLayer(data.layerId);
  if (!cfg) return null;

  const prioritized = cfg.inspectorFields ?? Object.keys(data.properties).slice(0, 10);
  const labels = cfg.fieldLabels ?? {};

  // Ações contextuais
  const actions = buildActions(data);

  return (
    <div className="absolute top-6 right-6 z-[900] w-[380px] max-h-[calc(100vh-7rem)] overflow-hidden flex flex-col rounded-2xl bg-background/92 backdrop-blur-2xl border border-border shadow-[0_8px_60px_-10px_rgba(0,0,0,0.85)] animate-in slide-in-from-right fade-in duration-300">
      {/* Header */}
      <div className="p-4 border-b border-border/60 flex items-start gap-3">
        <div
          className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
          style={{ backgroundColor: cfg.color + "20", border: `1px solid ${cfg.color}50` }}
        >
          <ScanEye className="h-4 w-4" style={{ color: cfg.color }} />
        </div>
        <div className="flex-1 min-w-0">
          <div className="text-[10px] uppercase tracking-widest text-muted-foreground font-semibold">
            Inspector
          </div>
          <div className="font-heading font-bold text-sm leading-tight truncate">
            {cfg.name}
          </div>
        </div>
        <button
          aria-label="Fechar inspector"
          onClick={onClose}
          className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Attributes */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2 custom-scrollbar">
        {prioritized.length === 0 && (
          <div className="text-xs text-muted-foreground">Sem atributos disponíveis.</div>
        )}
        {prioritized.map((field) => {
          const raw = data.properties[field];
          if (raw === null || raw === undefined || raw === "") return null;
          const label = labels[field] ?? formatKey(field);
          const value = formatValue(raw);
          return (
            <div key={field} className="flex flex-col gap-0.5 py-1.5 border-b border-border/30 last:border-0">
              <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
                {label}
              </div>
              <div className="text-sm font-mono break-words">{value}</div>
            </div>
          );
        })}

        {data.latlng && (
          <div className="flex flex-col gap-0.5 py-1.5 border-t border-border/30 mt-3 pt-3">
            <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
              Clique em
            </div>
            <div className="text-xs font-mono">
              {data.latlng.lat.toFixed(5)}, {data.latlng.lng.toFixed(5)}
            </div>
          </div>
        )}
      </div>

      {/* Actions */}
      {actions.length > 0 && (
        <div className="p-4 border-t border-border/60 space-y-2">
          {actions.map((a) => (
            <a
              key={a.label}
              href={a.href}
              target={a.external ? "_blank" : undefined}
              rel={a.external ? "noopener noreferrer" : undefined}
              className="flex items-center justify-between gap-2 px-3 py-2 rounded-lg bg-primary/10 text-primary border border-primary/30 hover:bg-primary/20 transition text-xs font-semibold"
            >
              <span className="flex items-center gap-2">
                <a.icon className="h-3.5 w-3.5" />
                {a.label}
              </span>
              <ExternalLink className="h-3 w-3 opacity-60" />
            </a>
          ))}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function formatKey(key: string): string {
  return key
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatValue(v: unknown): string {
  if (v === null || v === undefined) return "—";
  if (typeof v === "number") {
    // Grandes números ganham separador de milhar
    if (Math.abs(v) >= 1000) return v.toLocaleString("pt-BR");
    return String(v);
  }
  if (typeof v === "object") return JSON.stringify(v);
  return String(v);
}

type Action = {
  label: string;
  href: string;
  icon: typeof Gavel;
  external?: boolean;
};

function buildActions(data: InspectorPayload): Action[] {
  const { layerId, properties } = data;
  const out: Action[] = [];

  // CAR → análise completa
  const carCode =
    (properties.cod_imovel as string) ||
    (properties._id as string) ||
    (properties.car_code as string);
  if (
    (layerId === "sicar_completo" || layerId === "geo_car") &&
    carCode
  ) {
    out.push({
      label: "Due diligence completa",
      href: `/consulta?q=${encodeURIComponent(carCode)}`,
      icon: ShieldAlert,
    });
  }

  // Autos ICMBio → ver no consulta
  if (layerId === "autos_icmbio" && properties.auto_no) {
    out.push({
      label: "Pesquisar autuado (DeepSearch)",
      href: `/consulta?q=${encodeURIComponent(String(properties.infrator || ""))}`,
      icon: Gavel,
    });
  }

  // Publicações DJEN (se viermos a ter no mapa)
  if (properties.numero_processo) {
    out.push({
      label: "Ver processo no DataJud",
      href: `/processos?q=${properties.numero_processo}`,
      icon: FileText,
    });
  }

  return out;
}
