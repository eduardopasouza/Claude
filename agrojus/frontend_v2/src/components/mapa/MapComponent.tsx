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
  GeoJSON,
  MapContainer,
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

  // Estilo por tipo de geometria
  const style = () => {
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

        <ZoomControl position="bottomleft" />
      </MapContainer>

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
