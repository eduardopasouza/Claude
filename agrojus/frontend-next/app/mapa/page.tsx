"use client";

import dynamic from "next/dynamic";

// Leaflet precisa do DOM — carregamento dinâmico sem SSR
const GisMap = dynamic(() => import("@/components/mapa/gis-map"), {
  ssr: false,
  loading: () => (
    <div className="h-[calc(100vh-5rem)] flex items-center justify-center">
      <div className="flex flex-col items-center gap-3">
        <div className="w-8 h-8 border-2 border-agrojus-emerald border-t-transparent rounded-full animate-spin" />
        <span className="text-sm text-[var(--muted-foreground)]">
          Carregando motor geoespacial…
        </span>
      </div>
    </div>
  ),
});

export default function MapaPage() {
  return (
    <div className="-m-6">
      <GisMap />
    </div>
  );
}
