"use client";

import dynamic from "next/dynamic";
import useSWR from "swr";
import { swrFetcher } from "@/lib/api";

// react-leaflet só no client para evitar SSR issues
const MapContainer = dynamic(
  () => import("react-leaflet").then((m) => m.MapContainer),
  { ssr: false }
);
const TileLayer = dynamic(
  () => import("react-leaflet").then((m) => m.TileLayer),
  { ssr: false }
);
const GeoJSON = dynamic(
  () => import("react-leaflet").then((m) => m.GeoJSON),
  { ssr: false }
);

type GeoJSONResponse = {
  type: "FeatureCollection";
  features: Array<{
    type: "Feature";
    properties: Record<string, unknown>;
    geometry: unknown;
  }>;
};

export function MapPreview({
  carCode,
  centroid,
}: {
  carCode: string;
  centroid?: { lat: number; lon: number };
}) {
  const { data } = useSWR<GeoJSONResponse>(
    `/property/${carCode}/geojson`,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  if (!centroid) {
    return (
      <div className="h-40 w-full bg-slate-900/40 border border-slate-800 rounded-xl flex items-center justify-center text-slate-500 text-xs">
        Sem coordenadas para preview
      </div>
    );
  }

  return (
    <div className="h-40 w-full rounded-xl overflow-hidden border border-slate-800 relative">
      <MapContainer
        center={[centroid.lat, centroid.lon]}
        zoom={13}
        scrollWheelZoom={false}
        dragging={false}
        zoomControl={false}
        attributionControl={false}
        className="h-full w-full"
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png"
          attribution=""
        />
        {data?.type === "FeatureCollection" && (
          <GeoJSON
            data={data}
            style={{
              color: "#10B981",
              weight: 2,
              fillColor: "#10B981",
              fillOpacity: 0.25,
              dashArray: "4,4",
            }}
          />
        )}
      </MapContainer>
      <div className="absolute bottom-1 right-2 text-[10px] text-slate-500 font-mono bg-slate-950/60 px-1.5 py-0.5 rounded">
        {centroid.lat.toFixed(3)}, {centroid.lon.toFixed(3)}
      </div>
    </div>
  );
}
