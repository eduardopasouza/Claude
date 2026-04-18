"use client";

/**
 * Zustand store do /mapa — estado global serializável em URL.
 *
 * Campos persistíveis em query string:
 *   layers   → CSV dos layer ids ativos         (?layers=deter_amazonia,prodes)
 *   opacity  → JSON opacidade por camada        (?opacity={"deter_amazonia":0.5})
 *   basemap  → id do basemap                    (?basemap=dark)
 *   t0,t1    → range temporal YYYY-MM           (?t0=2023-01&t1=2024-12)
 *   uf      → drill-down UF                    (?uf=MA)
 *   mun     → drill-down município IBGE        (?mun=2111300)
 *   c       → center lat,lng,zoom              (?c=-12.4,-55.2,5)
 *   price   → camada de preço ativa            (?price=preco_soja)
 *
 * O hook `useMapUrlSync` abaixo amarra este store a `useSearchParams`
 * via router.replace — navegação bookmark-friendly.
 */

import { create } from "zustand";

export type TemporalRange = { start: string | null; end: string | null };
export type DrillDown = { uf: string | null; municipio: string | null };

export interface MapState {
  activeLayers: string[];
  opacityByLayer: Record<string, number>; // 0..1 por layer id
  basemap: string;
  temporal: TemporalRange;
  drill: DrillDown;
  priceLayerId: string | null;
  center: { lat: number; lng: number; zoom: number };

  setActiveLayers: (v: string[]) => void;
  toggleLayer: (id: string) => void;
  setOpacity: (id: string, v: number) => void;
  setBasemap: (b: string) => void;
  setTemporal: (r: TemporalRange) => void;
  setDrillUF: (uf: string | null) => void;
  setDrillMunicipio: (m: string | null) => void;
  setPriceLayer: (id: string | null) => void;
  setCenter: (lat: number, lng: number, zoom: number) => void;
  hydrate: (partial: Partial<MapState>) => void;
  reset: () => void;
}

const INITIAL: Omit<
  MapState,
  | "setActiveLayers" | "toggleLayer" | "setOpacity" | "setBasemap"
  | "setTemporal" | "setDrillUF" | "setDrillMunicipio" | "setPriceLayer"
  | "setCenter" | "hydrate" | "reset"
> = {
  activeLayers: [],
  opacityByLayer: {},
  basemap: "dark",
  temporal: { start: null, end: null },
  drill: { uf: null, municipio: null },
  priceLayerId: null,
  center: { lat: -12.4411, lng: -55.221, zoom: 5 },
};

export const useMapStore = create<MapState>((set) => ({
  ...INITIAL,

  setActiveLayers: (v) => set({ activeLayers: v }),
  toggleLayer: (id) =>
    set((s) => ({
      activeLayers: s.activeLayers.includes(id)
        ? s.activeLayers.filter((x) => x !== id)
        : [...s.activeLayers, id],
    })),
  setOpacity: (id, v) =>
    set((s) => ({
      opacityByLayer: { ...s.opacityByLayer, [id]: Math.max(0, Math.min(1, v)) },
    })),
  setBasemap: (b) => set({ basemap: b }),
  setTemporal: (r) => set({ temporal: r }),
  setDrillUF: (uf) =>
    set((s) => ({ drill: { uf, municipio: uf ? s.drill.municipio : null } })),
  setDrillMunicipio: (municipio) =>
    set((s) => ({ drill: { ...s.drill, municipio } })),
  setPriceLayer: (id) => set({ priceLayerId: id }),
  setCenter: (lat, lng, zoom) => set({ center: { lat, lng, zoom } }),
  hydrate: (partial) => set((s) => ({ ...s, ...partial })),
  reset: () => set({ ...INITIAL }),
}));

// ---------------------------------------------------------------------------
// Serialização URL ↔ Store
// ---------------------------------------------------------------------------

export function stateToQueryString(s: MapState): string {
  const q = new URLSearchParams();
  if (s.activeLayers.length) q.set("layers", s.activeLayers.join(","));
  const opacities = Object.entries(s.opacityByLayer).filter(([, v]) => v !== 1);
  if (opacities.length) q.set("opacity", JSON.stringify(Object.fromEntries(opacities)));
  if (s.basemap && s.basemap !== "dark") q.set("basemap", s.basemap);
  if (s.temporal.start) q.set("t0", s.temporal.start);
  if (s.temporal.end) q.set("t1", s.temporal.end);
  if (s.drill.uf) q.set("uf", s.drill.uf);
  if (s.drill.municipio) q.set("mun", s.drill.municipio);
  if (s.priceLayerId) q.set("price", s.priceLayerId);
  const { lat, lng, zoom } = s.center;
  if (zoom !== 5 || Math.abs(lat + 12.4411) > 0.001 || Math.abs(lng + 55.221) > 0.001) {
    q.set("c", `${lat.toFixed(4)},${lng.toFixed(4)},${zoom}`);
  }
  return q.toString();
}

export function queryStringToPartial(qs: URLSearchParams): Partial<MapState> {
  const out: Partial<MapState> = {};
  const layers = qs.get("layers");
  if (layers) out.activeLayers = layers.split(",").filter(Boolean);
  const op = qs.get("opacity");
  if (op) {
    try {
      out.opacityByLayer = JSON.parse(op);
    } catch {
      /* ignore */
    }
  }
  const basemap = qs.get("basemap");
  if (basemap) out.basemap = basemap;
  const t0 = qs.get("t0");
  const t1 = qs.get("t1");
  if (t0 || t1) out.temporal = { start: t0 || null, end: t1 || null };
  const uf = qs.get("uf");
  const mun = qs.get("mun");
  if (uf || mun) out.drill = { uf, municipio: mun };
  const price = qs.get("price");
  if (price) out.priceLayerId = price;
  const c = qs.get("c");
  if (c) {
    const parts = c.split(",").map(Number);
    if (parts.length === 3 && parts.every((n) => !Number.isNaN(n))) {
      out.center = { lat: parts[0], lng: parts[1], zoom: parts[2] };
    }
  }
  return out;
}
