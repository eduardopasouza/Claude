"use client";

import { useState } from "react";
import { Copy, Download, ExternalLink, FileBarChart2, FileText, Gavel, ScanEye, ShieldAlert, X, Check } from "lucide-react";
import { getLayer } from "@/lib/layers-catalog";

// Camadas que representam imóvel rural — habilita botão "Gerar Dossiê"
const PROPERTY_LAYERS = new Set([
  "sicar_completo",
  "geo_car",
  "sigef_parcelas",
  "snci_imoveis",
  "incra_assentamentos",
  "incra_quilombolas",
]);

export type InspectorPayload = {
  layerId: string;
  properties: Record<string, unknown>;
  /** Opcional: coordenada de origem do clique */
  latlng?: { lat: number; lng: number };
  /** Opcional: geometria do feature em GeoJSON (permite exportar) */
  geometry?: unknown;
};

export function LayerInspector({
  data,
  onClose,
}: {
  data: InspectorPayload | null;
  onClose: () => void;
}) {
  const [copiedWhat, setCopiedWhat] = useState<string | null>(null);

  if (!data) return null;
  const cfg = getLayer(data.layerId);
  if (!cfg) return null;

  const prioritized = cfg.inspectorFields ?? Object.keys(data.properties).slice(0, 10);
  const labels = cfg.fieldLabels ?? {};

  // Ações contextuais
  const actions = buildActions(data);

  function flash(what: string) {
    setCopiedWhat(what);
    setTimeout(() => setCopiedWhat(null), 1500);
  }

  function copyAsText() {
    const lines: string[] = [];
    for (const f of prioritized) {
      const v = data!.properties[f];
      if (v === null || v === undefined || v === "") continue;
      const label = labels[f] ?? formatKey(f);
      lines.push(`${label}: ${formatValue(v)}`);
    }
    if (data!.latlng) {
      lines.push(`Coordenada: ${data!.latlng.lat.toFixed(5)}, ${data!.latlng.lng.toFixed(5)}`);
    }
    navigator.clipboard.writeText(lines.join("\n"));
    flash("text");
  }

  function copyAsJson() {
    navigator.clipboard.writeText(JSON.stringify(data!.properties, null, 2));
    flash("json");
  }

  function downloadGeoJson() {
    if (!data!.geometry) return;
    const fc = {
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          properties: data!.properties,
          geometry: data!.geometry,
        },
      ],
    };
    const blob = new Blob([JSON.stringify(fc, null, 2)], { type: "application/geo+json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${data!.layerId}_${Date.now()}.geojson`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function openDossie() {
    if (!data!.geometry) return;
    // Gera chave única e armazena o request em sessionStorage
    const sk = `${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    const nome =
      (data!.properties.cod_imovel as string) ||
      (data!.properties.nome as string) ||
      cfg!.name;

    // Se for CAR, passa car_code direto (mais rápido + usa geometria do PostGIS)
    const carCode =
      (data!.properties.cod_imovel as string) ||
      (data!.properties.car_code as string);
    const isCarLayer = data!.layerId === "sicar_completo" || data!.layerId === "geo_car";

    const body: Record<string, unknown> = {
      persona: "geral",
      name: `Dossiê · ${nome}`,
    };
    if (isCarLayer && carCode) {
      body.car_code = carCode;
    } else {
      body.geometry = data!.geometry;
    }
    sessionStorage.setItem(`agrojus:dossie:${sk}`, JSON.stringify(body));
    window.open(`/dossie?sk=${sk}`, "_blank");
  }

  function downloadKml() {
    if (!data!.geometry) return;
    const kml = geoJsonToKml(
      { properties: data!.properties, geometry: data!.geometry },
      cfg!.name,
    );
    const blob = new Blob([kml], { type: "application/vnd.google-earth.kml+xml" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${data!.layerId}_${Date.now()}.kml`;
    a.click();
    URL.revokeObjectURL(url);
  }

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

      {/* Dossiê completo — CTA destacada para camadas de imóvel rural */}
      {PROPERTY_LAYERS.has(data.layerId) && Boolean(data.geometry) && (
        <div className="px-4 pt-3">
          <button
            onClick={openDossie}
            className="w-full group flex items-center justify-center gap-2 px-3 py-2.5 rounded-lg bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white text-sm font-semibold border border-emerald-400/40 shadow-lg shadow-emerald-900/30 transition"
            title="Gerar relatório completo sobre esta área — 14 seções, 15+ fontes, persona-adaptado"
          >
            <FileBarChart2 className="h-4 w-4" />
            Gerar Dossiê Completo
            <ExternalLink className="h-3 w-3 opacity-80" />
          </button>
          <p className="text-[10px] text-slate-500 mt-1.5 px-1">
            Relatório com 14 seções em nova aba — fundiário, compliance,
            ambiental, crédito, mercado, logística, valuation, jurídico.
          </p>
        </div>
      )}

      {/* Quick-copy actions */}
      <div className="px-4 pt-3 pb-2 border-t border-border/60 grid grid-cols-2 gap-1.5">
        <button
          onClick={copyAsText}
          className="flex items-center justify-center gap-1.5 px-2 py-1.5 rounded-md bg-muted/50 hover:bg-muted text-xs text-foreground border border-border transition"
          title="Copiar atributos como texto"
        >
          {copiedWhat === "text" ? (
            <>
              <Check className="h-3 w-3 text-primary" /> copiado
            </>
          ) : (
            <>
              <Copy className="h-3 w-3" /> Copiar texto
            </>
          )}
        </button>
        <button
          onClick={copyAsJson}
          className="flex items-center justify-center gap-1.5 px-2 py-1.5 rounded-md bg-muted/50 hover:bg-muted text-xs text-foreground border border-border transition"
          title="Copiar atributos como JSON"
        >
          {copiedWhat === "json" ? (
            <>
              <Check className="h-3 w-3 text-primary" /> copiado
            </>
          ) : (
            <>
              <Copy className="h-3 w-3" /> Copiar JSON
            </>
          )}
        </button>
        {Boolean(data.geometry) && (
          <>
            <button
              onClick={downloadGeoJson}
              className="flex items-center justify-center gap-1.5 px-2 py-1.5 rounded-md bg-muted/50 hover:bg-muted text-xs text-foreground border border-border transition"
              title="Baixar feature em GeoJSON"
            >
              <Download className="h-3 w-3" /> GeoJSON
            </button>
            <button
              onClick={downloadKml}
              className="flex items-center justify-center gap-1.5 px-2 py-1.5 rounded-md bg-muted/50 hover:bg-muted text-xs text-foreground border border-border transition"
              title="Baixar feature em KML (Google Earth)"
            >
              <Download className="h-3 w-3" /> KML
            </button>
          </>
        )}
      </div>

      {/* Actions externas */}
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

// ---------------------------------------------------------------------------
// GeoJSON → KML serialization
// ---------------------------------------------------------------------------
function geoJsonToKml(feature: { properties: Record<string, unknown>; geometry: unknown }, layerName: string): string {
  const esc = (s: unknown) =>
    String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

  const name = esc(
    (feature.properties.nome as string) ||
      (feature.properties.name as string) ||
      (feature.properties.cod_imovel as string) ||
      layerName,
  );
  const desc = Object.entries(feature.properties)
    .filter(([, v]) => v !== null && v !== undefined && v !== "")
    .map(([k, v]) => `<strong>${esc(k)}</strong>: ${esc(v)}`)
    .join("<br/>");

  const g = feature.geometry as { type: string; coordinates: unknown } | null;
  if (!g) return "";

  function coords1(c: number[]): string {
    return `${c[0]},${c[1]}${c[2] !== undefined ? "," + c[2] : ""}`;
  }
  function coords2(arr: number[][]): string {
    return arr.map(coords1).join(" ");
  }

  let geomXml = "";
  if (g.type === "Point") {
    geomXml = `<Point><coordinates>${coords1(g.coordinates as number[])}</coordinates></Point>`;
  } else if (g.type === "LineString") {
    geomXml = `<LineString><coordinates>${coords2(g.coordinates as number[][])}</coordinates></LineString>`;
  } else if (g.type === "MultiLineString") {
    geomXml = `<MultiGeometry>${(g.coordinates as number[][][])
      .map((c) => `<LineString><coordinates>${coords2(c)}</coordinates></LineString>`)
      .join("")}</MultiGeometry>`;
  } else if (g.type === "Polygon") {
    const rings = (g.coordinates as number[][][]).map((r, i) => {
      const tag = i === 0 ? "outerBoundaryIs" : "innerBoundaryIs";
      return `<${tag}><LinearRing><coordinates>${coords2(r)}</coordinates></LinearRing></${tag}>`;
    });
    geomXml = `<Polygon>${rings.join("")}</Polygon>`;
  } else if (g.type === "MultiPolygon") {
    const polys = (g.coordinates as number[][][][]).map((poly) => {
      const rings = poly.map((r, i) => {
        const tag = i === 0 ? "outerBoundaryIs" : "innerBoundaryIs";
        return `<${tag}><LinearRing><coordinates>${coords2(r)}</coordinates></LinearRing></${tag}>`;
      });
      return `<Polygon>${rings.join("")}</Polygon>`;
    });
    geomXml = `<MultiGeometry>${polys.join("")}</MultiGeometry>`;
  }

  return `<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>${esc(layerName)}</name>
    <Placemark>
      <name>${name}</name>
      <description><![CDATA[${desc}]]></description>
      ${geomXml}
    </Placemark>
  </Document>
</kml>`;
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
