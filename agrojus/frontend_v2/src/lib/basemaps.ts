/**
 * Basemaps disponíveis para o mapa do AgroJus.
 *
 * 4 opções com atribuições corretas. Troca de basemap muda apenas a
 * TileLayer — as camadas sobrepostas permanecem.
 */

export type BasemapId = "dark" | "light" | "satellite" | "topo";

export type Basemap = {
  id: BasemapId;
  label: string;
  description: string;
  /** URL template Leaflet */
  url: string;
  attribution: string;
  /** Se o tema de fundo é claro ou escuro (afeta cor dos painéis overlay). */
  theme: "dark" | "light";
  maxZoom: number;
};

export const BASEMAPS: Basemap[] = [
  {
    id: "dark",
    label: "Escuro",
    description: "CARTO Dark Matter — ideal para destacar dados",
    url: "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    attribution: '&copy; <a href="https://carto.com/attributions">CARTO</a>',
    theme: "dark",
    maxZoom: 20,
  },
  {
    id: "light",
    label: "Claro",
    description: "CARTO Voyager — tons suaves e legíveis",
    url: "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
    attribution: '&copy; <a href="https://carto.com/attributions">CARTO</a>',
    theme: "light",
    maxZoom: 20,
  },
  {
    id: "satellite",
    label: "Satélite",
    description: "Esri World Imagery — imagens de satélite",
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attribution:
      'Tiles &copy; Esri — Source: Esri, Maxar, Earthstar Geographics',
    theme: "dark",
    maxZoom: 19,
  },
  {
    id: "topo",
    label: "Topográfico",
    description: "OpenTopoMap — relevo e curvas de nível",
    url: "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    attribution:
      'Map data: &copy; OpenStreetMap contributors, SRTM | &copy; <a href="https://opentopomap.org">OpenTopoMap</a>',
    theme: "light",
    maxZoom: 17,
  },
];

export function getBasemap(id: BasemapId): Basemap {
  return BASEMAPS.find((b) => b.id === id) ?? BASEMAPS[0];
}
