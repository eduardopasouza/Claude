"use client";

/**
 * AgroJus Map v2 — refatoração que amarra:
 *  - LayerTreePanel (árvore temática, esquerda)
 *  - BasemapSwitcher (dark/light/satélite/topo, canto superior direito)
 *  - LayerInspector (drawer direito, ao clicar em feature)
 *  - StatsDashboard (rodapé recolhível)
 *  - MapToolbar (régua, coord input, export — canto inferior direito)
 *  - PropertySearch (busca CAR + fly-to)
 *
 * Consumo de dados:
 *  - LAYERS com endpoint "postgis" → /api/v1/geo/postgis/{id}/geojson
 *  - LAYERS com endpoint "geo"     → /api/v1/geo/layers/{id}/geojson (legado)
 *  - LAYERS com endpoint "stub"    → não busca (comingSoon)
 */

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  CircleMarker,
  GeoJSON,
  MapContainer,
  Polyline,
  TileLayer,
  useMap,
  useMapEvents,
  ZoomControl,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { Crosshair, Loader2, Ruler } from "lucide-react";

import useSWR from "swr";
import { swrFetcher } from "@/lib/api";
import { getLayer, LAYERS, LayerConfig } from "@/lib/layers-catalog";
import { BASEMAPS, BasemapId, getBasemap } from "@/lib/basemaps";

import { BasemapSwitcher } from "./BasemapSwitcher";
import { LayerInspector, InspectorPayload } from "./LayerInspector";
import { LayerTreePanel } from "./LayerTreePanel";
import { StatsDashboard } from "./StatsDashboard";
import PropertySearch from "./PropertySearch";
import {
  MapTools,
  ToolMode,
  DrawnPolygon,
  PointAnalysis,
  AOIAnalysis,
  analyzePoint,
  analyzeAOI,
} from "./MapTools";

// ---------------------------------------------------------------------------
// Sub-componente: captura eventos de pan/zoom
// ---------------------------------------------------------------------------
function MapEvents({
  onMove,
}: {
  onMove: (bounds: string, zoom: number, center: L.LatLng) => void;
}) {
  const map = useMapEvents({
    moveend: () => onMove(map.getBounds().toBBoxString(), map.getZoom(), map.getCenter()),
  });
  useEffect(() => {
    onMove(map.getBounds().toBBoxString(), map.getZoom(), map.getCenter());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return null;
}

// ---------------------------------------------------------------------------
// Sub-componente: captura clicks (apenas quando modo de tool ativo)
// ---------------------------------------------------------------------------
function MapClickHandler({
  onClick,
  mode,
}: {
  onClick: (latlng: L.LatLng) => void;
  mode: ToolMode;
}) {
  useMapEvents({
    click: (e) => {
      if (mode === "point" || mode === "draw") {
        onClick(e.latlng);
      }
    },
  });
  return null;
}

// ---------------------------------------------------------------------------
// Sub-componente: fly-to animado ao selecionar CAR
// ---------------------------------------------------------------------------
function FlyToProperty({ center }: { center: [number, number] | null }) {
  const map = useMap();
  useEffect(() => {
    if (center) map.flyTo(center, 14, { duration: 1.2 });
  }, [center, map]);
  return null;
}

// ---------------------------------------------------------------------------
// Sub-componente: polígono do CAR selecionado + overlaps
// ---------------------------------------------------------------------------
function SelectedPropertyLayer({ carCode }: { carCode: string | null }) {
  const { data: geojson } = useSWR(
    carCode ? `/property/${carCode}/geojson` : null,
    swrFetcher,
    { revalidateOnFocus: false }
  );
  const { data: overlaps } = useSWR(
    carCode ? `/property/${carCode}/overlaps/geojson` : null,
    swrFetcher,
    { revalidateOnFocus: false }
  );
  if (!carCode) return null;
  return (
    <>
      {geojson?.type === "FeatureCollection" && (
        <GeoJSON
          key={`prop-${carCode}`}
          data={geojson}
          style={{
            color: "#10B981",
            weight: 3,
            fillColor: "#10B981",
            fillOpacity: 0.2,
            dashArray: "5,5",
          }}
        />
      )}
      {overlaps?.type === "FeatureCollection" && overlaps.features.length > 0 && (
        <GeoJSON
          key={`overlaps-${carCode}`}
          data={overlaps}
          style={(feature: unknown) => {
            const f = feature as { properties?: { color?: string } };
            return {
              color: f.properties?.color || "#FF0000",
              weight: 2,
              fillColor: f.properties?.color || "#FF0000",
              fillOpacity: 0.3,
            };
          }}
        />
      )}
    </>
  );
}

// ---------------------------------------------------------------------------
// Paletas sequenciais ColorBrewer-like para choropleth (5 stops)
// ---------------------------------------------------------------------------
const PALETTES: Record<string, string[]> = {
  YlGn: ["#ffffe5", "#c2e699", "#78c679", "#31a354", "#006837"],
  YlOrBr: ["#ffffe5", "#fee391", "#fe9929", "#d95f0e", "#993404"],
  YlGnBu: ["#ffffd9", "#c7e9b4", "#41b6c4", "#1d91c0", "#253494"],
  Greens: ["#edf8e9", "#bae4b3", "#74c476", "#31a354", "#006d2c"],
  Reds: ["#fee5d9", "#fcae91", "#fb6a4a", "#de2d26", "#a50f15"],
  Blues: ["#eff3ff", "#bdd7e7", "#6baed6", "#3182bd", "#08519c"],
  Greys: ["#f7f7f7", "#cccccc", "#969696", "#636363", "#252525"],
  Oranges: ["#feedde", "#fdbe85", "#fd8d3c", "#e6550d", "#a63603"],
  Purples: ["#f2f0f7", "#cbc9e2", "#9e9ac8", "#756bb1", "#54278f"],
  PuRd: ["#f1eef6", "#d7b5d8", "#df65b0", "#dd1c77", "#980043"],
  BuPu: ["#edf8fb", "#b3cde3", "#8c96c6", "#8856a7", "#810f7c"],
  BuGn: ["#edf8fb", "#b2e2e2", "#66c2a4", "#2ca25f", "#006d2c"],
  OrRd: ["#fef0d9", "#fdcc8a", "#fc8d59", "#e34a33", "#b30000"],
  viridis: ["#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"],
};

function interpolateColor(scheme: string, t: number): string {
  const palette = PALETTES[scheme] || PALETTES.YlGn;
  const n = palette.length;
  const idx = Math.max(0, Math.min(n - 1, Math.floor(t * n)));
  return palette[idx];
}

// ---------------------------------------------------------------------------
// Sub-componente: camada ativa com click handler → Inspector
// ---------------------------------------------------------------------------
function ActiveLayer({
  layer,
  bounds,
  onFeatureClick,
  onCountUpdate,
}: {
  layer: LayerConfig;
  bounds: string;
  onFeatureClick: (payload: InspectorPayload) => void;
  onCountUpdate: (layerId: string, count: number) => void;
}) {
  // Determina endpoint baseado no tipo
  const endpoint = useMemo(() => {
    if (!bounds) return null;
    const effectiveId = layer.endpointId ?? layer.id;
    const qs = `bbox=${bounds}&max_features=${layer.maxFeatures || 500}`;
    switch (layer.endpoint) {
      case "postgis":
        return `/geo/postgis/${effectiveId}/geojson?${qs}`;
      case "geo":
        return `/geo/layers/${effectiveId}/geojson?${qs}`;
      case "ibge_choropleth": {
        // choropleth municipal por métrica + ano
        const ano = layer.defaultYear ?? 2022;
        return `/geo/ibge/choropleth/${effectiveId}/${ano}`;
      }
      case "ibge_choropleth_uf": {
        // choropleth por UF — 27 polígonos, carrega rápido
        const ano = layer.defaultYear ?? 2022;
        // Se id começa com "preco_", usa endpoint Agrolink (preço atual)
        if (effectiveId.startsWith("preco_")) {
          const commodity = effectiveId.replace("preco_", "");
          return `/geo/ibge/choropleth/uf/preco/${commodity}`;
        }
        return `/geo/ibge/choropleth/uf/${effectiveId}/${ano}`;
      }
      case "stub":
      case "external":
      default:
        return null;
    }
  }, [layer, bounds]);

  const { data } = useSWR(endpoint, swrFetcher, {
    revalidateOnFocus: false,
    dedupingInterval: 60_000,
  });

  // Propaga contagem ao dashboard
  useEffect(() => {
    if (data?.features) onCountUpdate(layer.id, data.features.length);
    else onCountUpdate(layer.id, 0);
  }, [data, layer.id, onCountUpdate]);

  if (!data || data.type !== "FeatureCollection" || data.features.length === 0) {
    return null;
  }

  // Para choropleth: calcular quintis (quantile breaks)
  // Distribuições agrícolas são log-normais — escala LINEAR pinta 99% igual.
  // Quintis distribuem uniformemente: top 20% = cor mais escura, etc.
  const isChoropleth = layer.geometryType === "choropleth";
  let breaks: number[] = []; // 4 cortes = 5 buckets
  if (isChoropleth) {
    const values = (data.features as Array<{ properties: { value?: number | null } }>)
      .map((f) => f.properties?.value)
      .filter((v): v is number => typeof v === "number" && !isNaN(v) && v > 0)
      .sort((a, b) => a - b);
    if (values.length >= 5) {
      breaks = [
        values[Math.floor(values.length * 0.2)],
        values[Math.floor(values.length * 0.4)],
        values[Math.floor(values.length * 0.6)],
        values[Math.floor(values.length * 0.8)],
      ];
    } else if (values.length > 0) {
      const min = values[0];
      const max = values[values.length - 1];
      const step = (max - min) / 5;
      breaks = [min + step, min + 2 * step, min + 3 * step, min + 4 * step];
    }
  }

  // Estilo por tipo de geometria
  const style = (feature: unknown) => {
    if (isChoropleth) {
      const f = feature as { properties?: { value?: number | null } };
      const v = f?.properties?.value;
      if (v == null || isNaN(v) || v <= 0) {
        return {
          color: "#334155",
          weight: 0.3,
          fillColor: "#1e293b",
          fillOpacity: 0.1,
        };
      }
      // Acha bucket via quintil (0..4)
      let bucket = 0;
      for (const b of breaks) {
        if (v > b) bucket++;
        else break;
      }
      const palette =
        PALETTES[layer.colorScheme ?? "YlGn"] || PALETTES.YlGn;
      return {
        color: "#0f172a",
        weight: 0.3,
        fillColor: palette[Math.min(bucket, palette.length - 1)],
        fillOpacity: 0.85,
      };
    }
    if (layer.geometryType === "line") {
      return {
        color: layer.color,
        weight: 2,
        opacity: 0.9,
      };
    }
    if (layer.geometryType === "point") {
      return {
        color: layer.color,
        weight: 1,
        fillColor: layer.color,
        fillOpacity: 0.8,
      };
    }
    return {
      color: layer.color,
      weight: 1.5,
      fillColor: layer.color,
      fillOpacity: 0.18,
    };
  };

  return (
    <GeoJSON
      key={`active-${layer.id}-${bounds}`}
      data={data}
      style={style}
      pointToLayer={(feature, latlng) =>
        L.circleMarker(latlng, {
          radius: 5,
          color: layer.color,
          fillColor: layer.color,
          fillOpacity: 0.85,
          weight: 1,
        })
      }
      onEachFeature={(feature, leafletLayer) => {
        leafletLayer.on("click", (e: L.LeafletMouseEvent) => {
          onFeatureClick({
            layerId: layer.id,
            properties: (feature.properties as Record<string, unknown>) ?? {},
            latlng: { lat: e.latlng.lat, lng: e.latlng.lng },
          });
        });
      }}
    />
  );
}

// ---------------------------------------------------------------------------
// MAIN COMPONENT
// ---------------------------------------------------------------------------
export default function MapComponent() {
  const [mounted, setMounted] = useState(false);
  const [bounds, setBounds] = useState("");
  const [zoom, setZoom] = useState(5);
  const [center, setCenter] = useState<L.LatLng>(new L.LatLng(-12.4411, -55.221));

  const [activeLayers, setActiveLayers] = useState<string[]>([]);
  const [basemap, setBasemap] = useState<BasemapId>("dark");
  const [inspector, setInspector] = useState<InspectorPayload | null>(null);
  const [countsByLayer, setCountsByLayer] = useState<Record<string, number>>({});

  // CAR selecionado pelo PropertySearch
  const [selectedCar, setSelectedCar] = useState<string | null>(null);
  const [flyTarget, setFlyTarget] = useState<[number, number] | null>(null);

  // === Ferramentas do mapa (ponto / desenhar / upload) ===
  const [toolMode, setToolMode] = useState<ToolMode>("none");
  const [drawPoints, setDrawPoints] = useState<[number, number][]>([]);
  const [uploadedFeatures, setUploadedFeatures] = useState<DrawnPolygon[]>([]);
  const [pendingAnalysis, setPendingAnalysis] = useState<AOIAnalysis | null>(null);
  const [pendingPointAnalysis, setPendingPointAnalysis] = useState<PointAnalysis | null>(null);
  const [pointMarker, setPointMarker] = useState<[number, number] | null>(null);

  const handleMapClick = useCallback(
    async (latlng: L.LatLng) => {
      if (toolMode === "point") {
        setPointMarker([latlng.lat, latlng.lng]);
        try {
          const res = await analyzePoint(latlng.lat, latlng.lng, 5);
          setPendingPointAnalysis(res);
          setPendingAnalysis(null);
        } catch (e) {
          console.error("analyzePoint failed:", e);
        }
      } else if (toolMode === "draw") {
        setDrawPoints((prev) => [...prev, [latlng.lat, latlng.lng]]);
      }
    },
    [toolMode]
  );

  const handleDrawCancel = useCallback(() => {
    setDrawPoints([]);
    setToolMode("none");
  }, []);

  const handleDrawFinish = useCallback(async () => {
    if (drawPoints.length < 3) return;
    const coords = drawPoints.map(([lat, lon]) => [lon, lat]);
    coords.push([coords[0][0], coords[0][1]]); // fecha
    const geometry = {
      type: "Polygon" as const,
      coordinates: [coords],
    };
    try {
      const res = await analyzeAOI(geometry, "Polígono desenhado");
      setPendingAnalysis(res);
      setPendingPointAnalysis(null);
      // salva como uploaded feature pra aparecer no mapa
      setUploadedFeatures((prev) => [
        ...prev,
        {
          type: "Feature",
          geometry,
          properties: { name: "Desenho manual", source: "drawn" },
        },
      ]);
    } catch (e) {
      console.error("analyzeAOI failed:", e);
    } finally {
      setDrawPoints([]);
      setToolMode("none");
    }
  }, [drawPoints]);

  const handleUpload = useCallback(async (features: DrawnPolygon[]) => {
    setUploadedFeatures((prev) => [...prev, ...features]);
    // Analisa o primeiro feature automaticamente
    if (features.length > 0) {
      try {
        const res = await analyzeAOI(features[0].geometry, features[0].properties.name);
        setPendingAnalysis(res);
        setPendingPointAnalysis(null);
      } catch (e) {
        console.error("analyzeAOI failed:", e);
      }
    }
  }, []);

  const clearAnalysis = useCallback(() => {
    setPendingAnalysis(null);
    setPendingPointAnalysis(null);
    setPointMarker(null);
  }, []);

  // Leaflet icons fix
  useEffect(() => {
    setMounted(true);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    delete (L.Icon.Default.prototype as any)._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
      iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
      shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
    });
  }, []);

  // Toggle layer (respeitando comingSoon e minZoom)
  const toggleLayer = useCallback(
    (id: string) => {
      const cfg = getLayer(id);
      if (!cfg || cfg.comingSoon) return;
      if (zoom < cfg.minZoom) return;
      setActiveLayers((prev) =>
        prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
      );
    },
    [zoom]
  );

  // Auto-desativa camadas que perderam zoom mínimo ao pan
  useEffect(() => {
    setActiveLayers((prev) =>
      prev.filter((id) => {
        const cfg = getLayer(id);
        return cfg && zoom >= cfg.minZoom;
      })
    );
  }, [zoom]);

  const handleFeatureClick = useCallback((payload: InspectorPayload) => {
    setInspector(payload);
  }, []);

  const handleCountUpdate = useCallback((layerId: string, count: number) => {
    setCountsByLayer((prev) => ({ ...prev, [layerId]: count }));
  }, []);

  const activeConfigs = useMemo(
    () => activeLayers.map((id) => getLayer(id)).filter(Boolean) as LayerConfig[],
    [activeLayers]
  );

  const totalFeatures = useMemo(
    () =>
      activeLayers.reduce((sum, id) => sum + (countsByLayer[id] ?? 0), 0),
    [activeLayers, countsByLayer]
  );

  const currentBasemap = getBasemap(basemap);
  const isLightBasemap = currentBasemap.theme === "light";

  if (!mounted) {
    return (
      <div className="h-[calc(100vh-4rem)] w-full flex items-center justify-center bg-black">
        <div className="flex items-center gap-3 text-primary font-mono">
          <Loader2 className="h-5 w-5 animate-spin" /> Inicializando AgroJus Map v2...
        </div>
      </div>
    );
  }

  return (
    <div
      className={`relative w-full h-[calc(100vh-4rem)] ${
        isLightBasemap ? "bg-neutral-100" : "bg-black"
      }`}
    >
      <MapContainer
        center={[-12.4411, -55.221]}
        zoom={zoom}
        zoomControl={false}
        className="w-full h-full z-0"
      >
        <MapEvents
          onMove={(b, z, c) => {
            setBounds(b);
            setZoom(z);
            setCenter(c);
          }}
        />
        <MapClickHandler onClick={handleMapClick} mode={toolMode} />

        {/* Basemap dinâmico */}
        <TileLayer
          key={currentBasemap.id}
          attribution={currentBasemap.attribution}
          url={currentBasemap.url}
          maxZoom={currentBasemap.maxZoom}
        />

        {/* Camadas ativas */}
        {activeConfigs.map((cfg) => (
          <ActiveLayer
            key={`layer-${cfg.id}`}
            layer={cfg}
            bounds={bounds}
            onFeatureClick={handleFeatureClick}
            onCountUpdate={handleCountUpdate}
          />
        ))}

        {/* CAR selecionado + overlaps */}
        <SelectedPropertyLayer carCode={selectedCar} />
        <FlyToProperty center={flyTarget} />

        {/* Polígonos desenhados/upados */}
        {uploadedFeatures.map((f, i) => (
          <GeoJSON
            key={`upload-${i}-${f.properties.name}`}
            data={f}
            style={{
              color: f.properties.source === "uploaded" ? "#F59E0B" : "#10B981",
              weight: 3,
              fillColor: f.properties.source === "uploaded" ? "#F59E0B" : "#10B981",
              fillOpacity: 0.2,
              dashArray: "6,4",
            }}
          />
        ))}

        {/* Linha temporária enquanto desenha */}
        {toolMode === "draw" && drawPoints.length >= 2 && (
          <Polyline
            positions={drawPoints}
            pathOptions={{ color: "#F59E0B", weight: 2, dashArray: "4,4" }}
          />
        )}

        {/* Vértices do polígono em desenho */}
        {toolMode === "draw" &&
          drawPoints.map((p, i) => (
            <CircleMarker
              key={`vertex-${i}`}
              center={p}
              radius={4}
              pathOptions={{
                color: "#F59E0B",
                fillColor: "#F59E0B",
                fillOpacity: 1,
                weight: 2,
              }}
            />
          ))}

        {/* Marker de ponto analisado */}
        {pointMarker && (
          <CircleMarker
            center={pointMarker}
            radius={8}
            pathOptions={{
              color: "#10B981",
              fillColor: "#10B981",
              fillOpacity: 0.6,
              weight: 3,
            }}
          />
        )}

        <ZoomControl position="bottomleft" />
      </MapContainer>

      {/* Ferramentas (ponto/desenhar/upload) */}
      <MapTools
        mode={toolMode}
        onModeChange={setToolMode}
        onUpload={handleUpload}
        drawPoints={drawPoints}
        onDrawCancel={handleDrawCancel}
        onDrawFinish={handleDrawFinish}
        pendingAnalysis={pendingAnalysis}
        pendingPointAnalysis={pendingPointAnalysis}
        onClearAnalysis={clearAnalysis}
      />

      {/* === HUD OVERLAYS === */}

      {/* Painel de camadas (esquerda) */}
      <LayerTreePanel activeLayers={activeLayers} onToggle={toggleLayer} zoom={zoom} />

      {/* Toolbar superior direita: busca CAR + basemap */}
      <div className="absolute top-6 right-6 z-[850] flex flex-col items-end gap-3">
        <div className="flex items-center gap-3">
          <BasemapSwitcher value={basemap} onChange={setBasemap} />
        </div>
        {!inspector && (
          <PropertySearch
            onSelectProperty={(car, c) => {
              setSelectedCar(car);
              setFlyTarget(c);
            }}
            onClearProperty={() => {
              setSelectedCar(null);
              setFlyTarget(null);
            }}
            selectedCar={selectedCar}
          />
        )}
      </div>

      {/* Inspector (drawer direito) — aparece ao clicar em feature */}
      <LayerInspector data={inspector} onClose={() => setInspector(null)} />

      {/* Coordinate HUD (inferior direito) */}
      <div className="absolute bottom-20 right-6 z-[700] pointer-events-none">
        <div className="bg-background/85 backdrop-blur-xl border border-border rounded-xl px-3 py-2 flex items-center gap-3 text-[11px] font-mono shadow-lg">
          <Crosshair className="h-3.5 w-3.5 text-primary" />
          <span>
            {center.lat.toFixed(5)}, {center.lng.toFixed(5)}
          </span>
          <span className="text-muted-foreground">Z{zoom}</span>
        </div>
      </div>

      {/* Dashboard inferior */}
      <StatsDashboard
        activeLayers={activeLayers}
        countsByLayer={countsByLayer}
        zoom={zoom}
        totalFeatures={totalFeatures}
      />

      {/* Attribution ou créditos (inferior esquerdo além do ZoomControl) */}
      <div className="absolute bottom-1 left-[90px] z-[600] text-[9px] text-muted-foreground/70 font-mono pointer-events-none">
        AgroJus Map v2 · {LAYERS.length} camadas catalogadas · {activeLayers.length} ativas
      </div>
    </div>
  );
}
