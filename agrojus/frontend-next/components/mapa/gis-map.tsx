"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import {
  MapContainer,
  TileLayer,
  LayersControl,
  GeoJSON,
  useMap,
  ZoomControl,
} from "react-leaflet";
import type { FeatureCollection } from "geojson";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { apiGet } from "@/lib/api";
import { Layers, Search, AlertTriangle, MapPin } from "lucide-react";
import { cn } from "@/lib/utils";

/* ──────────── Camadas de Tile ──────────── */
const TILES = {
  dark: {
    url: "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    attribution: "&copy; CARTO",
  },
  satellite: {
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attribution: "&copy; Esri",
  },
  osm: {
    url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attribution: "&copy; OSM contributors",
  },
};

/* ──────────── Painel de Camadas ──────────── */
interface LayerToggle {
  id: string;
  label: string;
  color: string;
  active: boolean;
  source: string;
}

const DEFAULT_LAYERS: LayerToggle[] = [
  { id: "embargos", label: "Embargos IBAMA", color: "#EF4444", active: true, source: "PostGIS" },
  { id: "parcelas", label: "Parcelas de Financiamento", color: "#3B82F6", active: false, source: "PostGIS" },
  { id: "terras_indigenas", label: "Terras Indígenas", color: "#F59E0B", active: false, source: "FUNAI WFS" },
  { id: "desmatamento", label: "Alertas Desmatamento", color: "#EF4444", active: false, source: "INPE DETER" },
  { id: "car", label: "CAR / SICAR", color: "#10B981", active: false, source: "SICAR" },
];

/* ──────────── Estilos de GeoJSON ──────────── */
function getLayerStyle(layerId: string) {
  const styles: Record<string, L.PathOptions> = {
    embargos: { color: "#EF4444", weight: 2, fillOpacity: 0.3, fillColor: "#EF4444" },
    parcelas: { color: "#3B82F6", weight: 1.5, fillOpacity: 0.2, fillColor: "#3B82F6" },
    terras_indigenas: { color: "#F59E0B", weight: 2, fillOpacity: 0.2, fillColor: "#F59E0B" },
    desmatamento: { color: "#F97316", weight: 2, fillOpacity: 0.4, fillColor: "#F97316" },
    car: { color: "#10B981", weight: 1, fillOpacity: 0.15, fillColor: "#10B981" },
  };
  return styles[layerId] || { color: "#10B981", weight: 1, fillOpacity: 0.2 };
}

/* ──────────── Componente Localizador ──────────── */
function LocationSearch() {
  const map = useMap();
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);

  const handleSearch = useCallback(async () => {
    if (!query.trim()) return;
    try {
      const res = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&countrycodes=br&limit=1`
      );
      const data = await res.json();
      if (data.length > 0) {
        map.flyTo([parseFloat(data[0].lat), parseFloat(data[0].lon)], 12, { duration: 1.5 });
        setOpen(false);
      }
    } catch {
      /* silently fail */
    }
  }, [query, map]);

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="absolute top-4 right-4 z-[1000] glass rounded-lg p-2.5 hover:bg-agrojus-elevated transition-colors"
        title="Buscar localização"
      >
        <Search size={18} className="text-agrojus-emerald" />
      </button>
    );
  }

  return (
    <div className="absolute top-4 right-4 z-[1000] glass rounded-lg p-3 flex gap-2 items-center shadow-xl">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        placeholder="Município, estado ou coordenada…"
        className="bg-agrojus-body border border-[var(--border)] rounded-md px-3 py-1.5 text-sm text-foreground placeholder:text-[var(--muted-foreground)] w-72 focus:outline-none focus:ring-1 focus:ring-agrojus-emerald"
        autoFocus
      />
      <button
        onClick={handleSearch}
        className="bg-agrojus-emerald text-agrojus-body rounded-md px-3 py-1.5 text-sm font-medium hover:opacity-90 transition-opacity"
      >
        Ir
      </button>
      <button onClick={() => setOpen(false)} className="text-[var(--muted-foreground)] hover:text-foreground">
        ✕
      </button>
    </div>
  );
}

/* ──────────── Coordenadas do mouse ──────────── */
function CoordDisplay() {
  const map = useMap();
  const [coords, setCoords] = useState({ lat: 0, lng: 0 });

  useEffect(() => {
    const handler = (e: L.LeafletMouseEvent) => setCoords({ lat: e.latlng.lat, lng: e.latlng.lng });
    map.on("mousemove", handler);
    return () => { map.off("mousemove", handler); };
  }, [map]);

  return (
    <div className="absolute bottom-4 left-4 z-[1000] glass rounded-md px-3 py-1.5 text-xs font-mono text-[var(--muted-foreground)]">
      <MapPin size={12} className="inline mr-1 text-agrojus-emerald" />
      {coords.lat.toFixed(5)}, {coords.lng.toFixed(5)}
    </div>
  );
}

/* ──────────── Componente Principal ──────────── */
export default function GisMap() {
  const [layers, setLayers] = useState<LayerToggle[]>(DEFAULT_LAYERS);
  const [geoData, setGeoData] = useState<Record<string, FeatureCollection>>({});
  const [loading, setLoading] = useState<string | null>(null);
  const [panelOpen, setPanelOpen] = useState(true);
  const [basemap, setBasemap] = useState<"dark" | "satellite" | "osm">("dark");

  const toggleLayer = useCallback(async (id: string) => {
    setLayers((prev) =>
      prev.map((l) => (l.id === id ? { ...l, active: !l.active } : l))
    );

    // Se a camada nunca foi carregada, tenta buscar do backend
    const layer = layers.find((l) => l.id === id);
    if (layer && !layer.active && !geoData[id]) {
      setLoading(id);
      try {
        // Tenta buscar geo do backend PostGIS
        const { data } = await apiGet<FeatureCollection>(`/api/v1/geo/${id}`);
        if (data && data.features && data.features.length > 0) {
          setGeoData((prev) => ({ ...prev, [id]: data }));
        }
      } catch {
        // Layer não disponível ainda — normal durante desenvolvimento
      } finally {
        setLoading(null);
      }
    }
  }, [layers, geoData]);

  return (
    <div className="relative h-[calc(100vh-3.5rem)]">
      {/* ── Painel de Camadas ── */}
      <div
        className={cn(
          "absolute top-4 left-4 z-[1000] glass rounded-xl shadow-2xl transition-all duration-300",
          panelOpen ? "w-72 p-4" : "w-auto p-2"
        )}
      >
        <button
          onClick={() => setPanelOpen(!panelOpen)}
          className="flex items-center gap-2 text-sm font-medium text-foreground w-full"
        >
          <Layers size={16} className="text-agrojus-emerald shrink-0" />
          {panelOpen && <span>Camadas Geoespaciais</span>}
        </button>

        {panelOpen && (
          <div className="mt-3 space-y-1.5">
            {layers.map((layer) => (
              <label
                key={layer.id}
                className={cn(
                  "flex items-center gap-3 px-2 py-2 rounded-lg cursor-pointer transition-colors text-sm",
                  layer.active
                    ? "bg-agrojus-elevated text-foreground"
                    : "text-[var(--muted-foreground)] hover:bg-agrojus-elevated/50"
                )}
              >
                <input
                  type="checkbox"
                  checked={layer.active}
                  onChange={() => toggleLayer(layer.id)}
                  className="sr-only"
                />
                <span
                  className="w-3 h-3 rounded-sm shrink-0 border"
                  style={{
                    backgroundColor: layer.active ? layer.color : "transparent",
                    borderColor: layer.color,
                  }}
                />
                <div className="flex-1 min-w-0">
                  <div className="truncate font-medium">{layer.label}</div>
                  <div className="text-[10px] text-[var(--muted-foreground)]">
                    {layer.source}
                    {loading === layer.id && " • Carregando…"}
                  </div>
                </div>
              </label>
            ))}

            {/* Seletor de basemap */}
            <div className="pt-2 mt-2 border-t border-[var(--border)]">
              <p className="text-[10px] uppercase tracking-wider text-[var(--muted-foreground)] mb-1.5 px-2">
                Mapa base
              </p>
              <div className="flex gap-1.5 px-2">
                {(["dark", "satellite", "osm"] as const).map((key) => (
                  <button
                    key={key}
                    onClick={() => setBasemap(key)}
                    className={cn(
                      "px-2.5 py-1 rounded-md text-xs font-medium transition-colors",
                      basemap === key
                        ? "bg-agrojus-emerald text-agrojus-body"
                        : "text-[var(--muted-foreground)] hover:text-foreground hover:bg-agrojus-elevated"
                    )}
                  >
                    {key === "dark" ? "Escuro" : key === "satellite" ? "Satélite" : "Ruas"}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* ── Mapa Leaflet ── */}
      <MapContainer
        center={[-14.235, -51.925]}
        zoom={5}
        zoomControl={false}
        className="h-full w-full"
        style={{ background: "#0A0F0D" }}
      >
        <ZoomControl position="bottomright" />
        <TileLayer
          key={basemap}
          url={TILES[basemap].url}
          attribution={TILES[basemap].attribution}
        />
        <LocationSearch />
        <CoordDisplay />

        {/* Renderizar camadas ativas com dados */}
        {layers
          .filter((l) => l.active && geoData[l.id])
          .map((l) => (
            <GeoJSON
              key={l.id + JSON.stringify(geoData[l.id]).substring(0, 50)}
              data={geoData[l.id]}
              style={() => getLayerStyle(l.id)}
              onEachFeature={(feature, leafletLayer) => {
                const props = feature.properties || {};
                const rows = Object.entries(props)
                  .slice(0, 8)
                  .map(([k, v]) => `<tr><td class="font-medium pr-2">${k}</td><td>${v}</td></tr>`)
                  .join("");
                leafletLayer.bindPopup(
                  `<div style="font-family:Inter,sans-serif;font-size:12px;max-width:280px"><table>${rows}</table></div>`
                );
              }}
            />
          ))}
      </MapContainer>

      {/* ── Info overlay ── */}
      <div className="absolute bottom-4 right-16 z-[1000] glass rounded-md px-3 py-1.5 text-xs text-[var(--muted-foreground)] flex items-center gap-2">
        <AlertTriangle size={12} className="text-risk-medium" />
        <span>
          {layers.filter((l) => l.active).length} camada(s) ativa(s)
        </span>
      </div>
    </div>
  );
}
