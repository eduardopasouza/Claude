"use client";

import { useState, useRef } from "react";
import {
  Crosshair,
  Pencil,
  Upload,
  X,
  Check,
  AlertCircle,
  Loader2,
  Download,
  FileBarChart2,
} from "lucide-react";
import { fetchWithAuth } from "@/lib/api";

export type ToolMode = "none" | "point" | "draw" | "upload";

export type DrawnPolygon = {
  type: "Feature";
  geometry: {
    type: "Polygon";
    coordinates: number[][][];
  };
  properties: {
    name: string;
    source: "drawn" | "uploaded";
  };
};

export type PointAnalysis = {
  coordinates: { lat: number; lon: number; radius_km: number };
  municipio?: { nome: string; uf: string; estado: string };
  overall_risk: string;
  risk_flags: string[];
  overlaps: Array<{ type: string; name?: string; severity: string }>;
  summary: Record<string, number>;
};

export type AOIAnalysis = {
  name: string;
  area_ha: number;
  centroid: { lat: number; lon: number };
  overlaps: Record<string, number>;
  total_overlaps: number;
  compliance_score: number;
  risk_level: string;
};

type Props = {
  mode: ToolMode;
  onModeChange: (m: ToolMode) => void;
  onUpload: (features: DrawnPolygon[]) => void;
  drawPoints: [number, number][];
  onDrawCancel: () => void;
  onDrawFinish: () => void;
  pendingAnalysis: AOIAnalysis | null;
  pendingPointAnalysis: PointAnalysis | null;
  onClearAnalysis: () => void;
  /** Geometria GeoJSON do AOI atualmente analisado — permite export */
  pendingAoiGeometry?: DrawnPolygon | null;
};

export function MapTools({
  mode,
  onModeChange,
  onUpload,
  drawPoints,
  onDrawCancel,
  onDrawFinish,
  pendingAnalysis,
  pendingPointAnalysis,
  onClearAnalysis,
  pendingAoiGeometry,
}: Props) {
  const fileInput = useRef<HTMLInputElement>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [uploadLoading, setUploadLoading] = useState(false);

  async function handleFile(file: File) {
    setUploadError(null);
    setUploadLoading(true);
    try {
      const text = await file.text();
      const features = parseFile(file.name, text);
      if (features.length === 0) {
        throw new Error("Nenhum polígono encontrado no arquivo");
      }
      onUpload(features);
      onModeChange("none");
    } catch (e) {
      setUploadError(String(e instanceof Error ? e.message : e));
    } finally {
      setUploadLoading(false);
    }
  }

  return (
    <>
      {/* Toolbar flutuante */}
      <div className="absolute top-4 right-4 z-[1000] flex flex-col gap-2">
        <ToolButton
          icon={Crosshair}
          label="Analisar ponto"
          active={mode === "point"}
          onClick={() => onModeChange(mode === "point" ? "none" : "point")}
        />
        <ToolButton
          icon={Pencil}
          label="Desenhar polígono"
          active={mode === "draw"}
          onClick={() => onModeChange(mode === "draw" ? "none" : "draw")}
        />
        <ToolButton
          icon={Upload}
          label="Upload GeoJSON/KML"
          active={mode === "upload"}
          onClick={() => fileInput.current?.click()}
          loading={uploadLoading}
        />
        <input
          ref={fileInput}
          type="file"
          accept=".geojson,.json,.kml,.gml"
          className="hidden"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) handleFile(f);
            e.target.value = ""; // permite re-upload do mesmo arquivo
          }}
        />
      </div>

      {/* Banner de modo ativo */}
      {mode === "point" && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-[1000] bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 px-4 py-2 rounded-lg text-sm font-medium backdrop-blur-md">
          Modo análise: clique em qualquer ponto do mapa
        </div>
      )}

      {mode === "draw" && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-[1000] flex items-center gap-3 bg-amber-500/20 border border-amber-500/40 text-amber-200 px-4 py-2 rounded-lg text-sm font-medium backdrop-blur-md">
          <span>
            Clique para adicionar vértices ({drawPoints.length})
            {drawPoints.length >= 3 && " · pronto para fechar"}
          </span>
          <button
            onClick={onDrawFinish}
            disabled={drawPoints.length < 3}
            className="flex items-center gap-1 px-2 py-1 bg-emerald-500/40 rounded text-emerald-100 disabled:opacity-40 text-xs"
          >
            <Check className="w-3 h-3" /> Fechar
          </button>
          <button
            onClick={onDrawCancel}
            className="flex items-center gap-1 px-2 py-1 bg-red-500/30 rounded text-red-200 text-xs"
          >
            <X className="w-3 h-3" /> Cancelar
          </button>
        </div>
      )}

      {uploadError && (
        <div className="absolute top-16 left-1/2 -translate-x-1/2 z-[1000] bg-red-500/20 border border-red-500/40 text-red-300 px-4 py-2 rounded-lg text-sm backdrop-blur-md flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          {uploadError}
          <button
            onClick={() => setUploadError(null)}
            className="ml-2 hover:bg-red-500/20 rounded p-0.5"
          >
            <X className="w-3 h-3" />
          </button>
        </div>
      )}

      {/* Drawer de análise (ponto ou AOI) */}
      {(pendingAnalysis || pendingPointAnalysis) && (
        <AnalysisDrawer
          aoi={pendingAnalysis}
          point={pendingPointAnalysis}
          aoiGeometry={pendingAoiGeometry ?? null}
          onClose={onClearAnalysis}
        />
      )}
    </>
  );
}

// ---------------------------------------------------------------------------
// Export helpers (KML/GeoJSON)
// ---------------------------------------------------------------------------
function downloadAOIAsGeoJSON(feature: DrawnPolygon, analysisName: string) {
  const fc = {
    type: "FeatureCollection",
    features: [feature],
    metadata: {
      generator: "AgroJus",
      generated_at: new Date().toISOString(),
      analysis_name: analysisName,
    },
  };
  const blob = new Blob([JSON.stringify(fc, null, 2)], { type: "application/geo+json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `aoi_${safeFilename(analysisName)}.geojson`;
  a.click();
  URL.revokeObjectURL(url);
}

function downloadAOIAsKML(feature: DrawnPolygon, analysisName: string) {
  const esc = (s: unknown) =>
    String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  const coords = (feature.geometry.coordinates[0] || [])
    .map((c) => `${c[0]},${c[1]}`)
    .join(" ");
  const kml = `<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>${esc(analysisName)}</name>
    <Style id="agrojus">
      <LineStyle><color>ff00ff00</color><width>2</width></LineStyle>
      <PolyStyle><color>2200ff00</color></PolyStyle>
    </Style>
    <Placemark>
      <name>${esc(analysisName)}</name>
      <description><![CDATA[AgroJus — Área de Interesse (AOI) desenhada/importada em ${new Date().toLocaleString("pt-BR")}]]></description>
      <styleUrl>#agrojus</styleUrl>
      <Polygon>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>${coords}</coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>
  </Document>
</kml>`;
  const blob = new Blob([kml], { type: "application/vnd.google-earth.kml+xml" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `aoi_${safeFilename(analysisName)}.kml`;
  a.click();
  URL.revokeObjectURL(url);
}

function safeFilename(s: string): string {
  return s.replace(/[^\w.-]+/g, "_").slice(0, 80) || "aoi";
}

function openDossieForAOI(feature: DrawnPolygon, name: string) {
  const sk = `${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  sessionStorage.setItem(
    `agrojus:dossie:${sk}`,
    JSON.stringify({
      geometry: feature.geometry,
      persona: "geral",
      name: `Dossiê · ${name}`,
    }),
  );
  window.open(`/dossie?sk=${sk}`, "_blank");
}

function ToolButton({
  icon: Icon,
  label,
  active,
  onClick,
  loading,
}: {
  icon: typeof Crosshair;
  label: string;
  active: boolean;
  onClick: () => void;
  loading?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      title={label}
      className={`
        w-10 h-10 rounded-lg flex items-center justify-center
        backdrop-blur-md border transition-all
        ${
          active
            ? "bg-emerald-500/30 border-emerald-400/60 text-emerald-200 shadow-lg shadow-emerald-500/20"
            : "bg-slate-950/70 border-slate-700 text-slate-400 hover:text-slate-100 hover:border-slate-500"
        }
      `}
    >
      {loading ? (
        <Loader2 className="w-4 h-4 animate-spin" />
      ) : (
        <Icon className="w-4 h-4" />
      )}
    </button>
  );
}

function AnalysisDrawer({
  aoi,
  point,
  aoiGeometry,
  onClose,
}: {
  aoi: AOIAnalysis | null;
  point: PointAnalysis | null;
  aoiGeometry: DrawnPolygon | null;
  onClose: () => void;
}) {
  return (
    <div className="absolute bottom-4 left-4 z-[1000] bg-slate-950/95 backdrop-blur-lg border border-slate-700 rounded-xl shadow-2xl w-96 max-h-[60vh] overflow-auto">
      <header className="flex items-center justify-between px-4 py-3 border-b border-slate-800 sticky top-0 bg-slate-950/95 gap-2">
        <h3 className="font-semibold text-slate-100 text-sm truncate">
          {aoi ? `📐 ${aoi.name}` : `📍 Análise de Ponto`}
        </h3>
        <div className="flex items-center gap-1 flex-shrink-0">
          {aoi && aoiGeometry && (
            <>
              <button
                onClick={() => downloadAOIAsGeoJSON(aoiGeometry, aoi.name)}
                className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-emerald-300 transition"
                title="Baixar GeoJSON"
              >
                <Download className="w-3.5 h-3.5" />
                <span className="sr-only">GeoJSON</span>
              </button>
              <button
                onClick={() => downloadAOIAsKML(aoiGeometry, aoi.name)}
                className="px-2 py-1 text-[10px] rounded bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-700/40 transition font-semibold uppercase tracking-wider"
                title="Baixar KML (Google Earth / QGIS)"
              >
                KML
              </button>
            </>
          )}
          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-slate-100"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </header>

      {aoi && aoiGeometry && (
        <div className="px-4 pt-3">
          <button
            onClick={() => openDossieForAOI(aoiGeometry, aoi.name)}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white text-xs font-semibold border border-emerald-400/40 shadow-md shadow-emerald-900/30 transition"
            title="Gerar dossiê completo desta área (14 seções)"
          >
            <FileBarChart2 className="w-3.5 h-3.5" />
            Gerar Dossiê desta área
          </button>
        </div>
      )}

      <div className="p-4 space-y-3 text-sm">
        {aoi && (
          <>
            <div className="flex justify-between">
              <span className="text-slate-400">Área</span>
              <span className="text-slate-100 font-semibold tabular-nums">
                {aoi.area_ha.toFixed(2)} ha
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Centróide</span>
              <span className="text-xs text-slate-500 font-mono">
                {aoi.centroid.lat.toFixed(3)}, {aoi.centroid.lon.toFixed(3)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Score de compliance</span>
              <span
                className={`font-bold text-lg tabular-nums ${
                  aoi.compliance_score >= 80
                    ? "text-emerald-400"
                    : aoi.compliance_score >= 50
                    ? "text-amber-400"
                    : "text-red-400"
                }`}
              >
                {aoi.compliance_score}/100
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Risco</span>
              <span
                className={`uppercase text-xs font-semibold px-2 py-0.5 rounded ${
                  aoi.risk_level === "critical"
                    ? "bg-red-500/20 text-red-300"
                    : aoi.risk_level === "high"
                    ? "bg-orange-500/20 text-orange-300"
                    : aoi.risk_level === "medium"
                    ? "bg-amber-500/20 text-amber-300"
                    : "bg-emerald-500/20 text-emerald-300"
                }`}
              >
                {aoi.risk_level}
              </span>
            </div>

            <div className="border-t border-slate-800 pt-3">
              <h4 className="text-xs uppercase tracking-wider text-slate-500 mb-2">
                Sobreposições ({aoi.total_overlaps})
              </h4>
              <div className="space-y-1">
                {Object.entries(aoi.overlaps).map(([key, count]) => (
                  <div
                    key={key}
                    className={`flex justify-between px-2 py-1 rounded text-xs ${
                      count > 0
                        ? "bg-red-500/10 text-red-300"
                        : "bg-slate-800/50 text-slate-500"
                    }`}
                  >
                    <span>{key.replace(/_/g, " ")}</span>
                    <span className="font-semibold">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}

        {point && (
          <>
            <div className="flex justify-between">
              <span className="text-slate-400">Coordenada</span>
              <span className="text-xs text-slate-500 font-mono">
                {point.coordinates.lat.toFixed(4)}, {point.coordinates.lon.toFixed(4)}
              </span>
            </div>
            {point.municipio && (
              <div className="flex justify-between">
                <span className="text-slate-400">Município</span>
                <span className="text-slate-100">
                  {point.municipio.nome} / {point.municipio.uf}
                </span>
              </div>
            )}
            <div className="flex justify-between">
              <span className="text-slate-400">Risco</span>
              <span
                className={`uppercase text-xs font-semibold px-2 py-0.5 rounded ${
                  point.overall_risk === "critical"
                    ? "bg-red-500/20 text-red-300"
                    : point.overall_risk === "high"
                    ? "bg-orange-500/20 text-orange-300"
                    : point.overall_risk === "medium"
                    ? "bg-amber-500/20 text-amber-300"
                    : "bg-emerald-500/20 text-emerald-300"
                }`}
              >
                {point.overall_risk}
              </span>
            </div>

            <div className="border-t border-slate-800 pt-3">
              <h4 className="text-xs uppercase tracking-wider text-slate-500 mb-2">
                Flags
              </h4>
              <ul className="space-y-1">
                {point.risk_flags.map((flag, i) => (
                  <li
                    key={i}
                    className="text-xs text-slate-300 bg-slate-800/50 rounded px-2 py-1"
                  >
                    {flag}
                  </li>
                ))}
              </ul>
            </div>

            {point.overlaps.length > 0 && (
              <div className="border-t border-slate-800 pt-3">
                <h4 className="text-xs uppercase tracking-wider text-slate-500 mb-2">
                  Sobreposições no raio de 5km
                </h4>
                <ul className="space-y-1">
                  {point.overlaps.slice(0, 5).map((o, i) => (
                    <li
                      key={i}
                      className="text-xs text-slate-300 bg-red-500/10 border border-red-500/20 rounded px-2 py-1"
                    >
                      {o.type}: {o.name || "—"}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

// -----------------------------------------------------------------------
// Parser: GeoJSON ou KML → array de DrawnPolygon
// -----------------------------------------------------------------------
function parseFile(filename: string, text: string): DrawnPolygon[] {
  const lower = filename.toLowerCase();
  if (lower.endsWith(".kml") || lower.endsWith(".gml")) {
    return parseKML(text, filename);
  }
  return parseGeoJSON(text, filename);
}

function parseGeoJSON(text: string, filename: string): DrawnPolygon[] {
  const data = JSON.parse(text);
  const out: DrawnPolygon[] = [];
  const features =
    data.type === "FeatureCollection"
      ? data.features
      : data.type === "Feature"
      ? [data]
      : [{ type: "Feature", geometry: data, properties: {} }];
  for (const f of features) {
    if (!f?.geometry) continue;
    const g = f.geometry;
    if (g.type === "Polygon") {
      out.push({
        type: "Feature",
        geometry: { type: "Polygon", coordinates: g.coordinates },
        properties: {
          name:
            (f.properties?.name as string) ||
            filename.replace(/\.[^.]+$/, ""),
          source: "uploaded",
        },
      });
    } else if (g.type === "MultiPolygon") {
      for (let i = 0; i < g.coordinates.length; i++) {
        out.push({
          type: "Feature",
          geometry: { type: "Polygon", coordinates: g.coordinates[i] },
          properties: {
            name: `${f.properties?.name || filename.replace(/\.[^.]+$/, "")} #${i + 1}`,
            source: "uploaded",
          },
        });
      }
    }
  }
  return out;
}

function parseKML(text: string, filename: string): DrawnPolygon[] {
  const parser = new DOMParser();
  const doc = parser.parseFromString(text, "text/xml");
  const out: DrawnPolygon[] = [];
  const placemarks = Array.from(doc.getElementsByTagName("Placemark"));

  placemarks.forEach((pm, idx) => {
    const polygons = Array.from(pm.getElementsByTagName("Polygon"));
    polygons.forEach((poly, pIdx) => {
      const outer = poly.querySelector(
        "outerBoundaryIs coordinates, outerBoundaryIs LinearRing coordinates"
      );
      if (!outer?.textContent) return;
      const coords = outer.textContent
        .trim()
        .split(/\s+/)
        .map((pair) => {
          const [lon, lat] = pair.split(",").map(parseFloat);
          return [lon, lat];
        })
        .filter(([a, b]) => !isNaN(a) && !isNaN(b));
      if (coords.length < 3) return;
      // Fecha polígono se necessário
      if (
        coords[0][0] !== coords[coords.length - 1][0] ||
        coords[0][1] !== coords[coords.length - 1][1]
      ) {
        coords.push([coords[0][0], coords[0][1]]);
      }
      const name =
        pm.querySelector("name")?.textContent ||
        `${filename.replace(/\.[^.]+$/, "")} #${idx + 1}${
          pIdx > 0 ? `.${pIdx + 1}` : ""
        }`;
      out.push({
        type: "Feature",
        geometry: { type: "Polygon", coordinates: [coords] },
        properties: { name, source: "uploaded" },
      });
    });
  });

  return out;
}

// Exporta helpers para chamadas diretas
export async function analyzePoint(
  lat: number,
  lon: number,
  radiusKm = 5
): Promise<PointAnalysis> {
  const res = await fetchWithAuth(
    `/geo/analyze-point?lat=${lat}&lon=${lon}&radius_km=${radiusKm}`
  );
  return res.json();
}

export async function analyzeAOI(
  geometry: DrawnPolygon["geometry"],
  name?: string
): Promise<AOIAnalysis> {
  const res = await fetchWithAuth(`/geo/aoi/analyze`, {
    method: "POST",
    body: JSON.stringify({ geometry, name }),
  });
  return res.json();
}
