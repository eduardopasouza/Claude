"use client";

import useSWR from "swr";
import {
  Truck,
  Loader2,
  Warehouse,
  Ship,
  Beef,
  Train,
  Route,
} from "lucide-react";
import { swrFetcher } from "@/lib/api";
import type { PropertyData } from "../PropertyHeader";

type NeighborItem = {
  tipo: string;
  nome?: string;
  lat?: number;
  lon?: number;
  distancia_km: number | null;
};

type NeighborsResponse = {
  car_code: string;
  centroid?: { lat: number; lon: number };
  neighbors: {
    armazens_silos?: NeighborItem[];
    frigorificos?: NeighborItem[];
    portos?: NeighborItem[];
    rodovia_federal?: NeighborItem[];
    ferrovia?: NeighborItem[];
  };
  error?: string;
};

export function LogisticaTab({ property }: { property: PropertyData }) {
  const { data, isLoading, error } = useSWR<NeighborsResponse>(
    `/property/${property.car_code}/neighbors?limit_each=5`,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  if (isLoading) {
    return (
      <div className="p-12 flex items-center justify-center text-slate-400">
        <Loader2 className="w-5 h-5 animate-spin mr-2" />
        Calculando distâncias (PostGIS KNN)…
      </div>
    );
  }

  if (error || data?.error) {
    return (
      <div className="p-6 text-red-300">
        Erro: {data?.error || "falha ao consultar logística"}
      </div>
    );
  }

  const n = data?.neighbors || {};

  return (
    <div className="p-6 space-y-5">
      <header className="flex items-baseline justify-between">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <Truck className="w-5 h-5 text-emerald-400" />
          Logística & Escoamento
        </h2>
        <span className="text-xs text-slate-500">
          PostGIS KNN · ST_DistanceSphere
        </span>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <CategoryCard
          icon={Warehouse}
          title="Armazéns & Silos"
          subtitle="CONAB SICARM"
          items={n.armazens_silos || []}
          color="text-amber-400"
        />
        <CategoryCard
          icon={Beef}
          title="Frigoríficos"
          subtitle="MAPA SIF"
          items={n.frigorificos || []}
          color="text-red-400"
        />
        <CategoryCard
          icon={Ship}
          title="Portos"
          subtitle="ANTAQ"
          items={n.portos || []}
          color="text-sky-400"
        />
        <MinDistCard
          items={[
            {
              icon: Route,
              label: "Rodovia Federal",
              source: "DNIT",
              km: n.rodovia_federal?.[0]?.distancia_km,
              color: "text-yellow-400",
            },
            {
              icon: Train,
              label: "Ferrovia",
              source: "ANTT",
              km: n.ferrovia?.[0]?.distancia_km,
              color: "text-violet-400",
            },
          ]}
        />
      </div>

      <footer className="text-xs text-slate-500 pt-3 border-t border-slate-800">
        Distâncias calculadas do centróide do imóvel ({" "}
        {data?.centroid?.lat.toFixed(3)}, {data?.centroid?.lon.toFixed(3)}) em
        linha reta (haversine). Próximo sprint: distância por rodovia real
        (OSRM) + custo logístico estimado.
      </footer>
    </div>
  );
}

function CategoryCard({
  icon: Icon,
  title,
  subtitle,
  items,
  color,
}: {
  icon: typeof Truck;
  title: string;
  subtitle: string;
  items: NeighborItem[];
  color: string;
}) {
  return (
    <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-5">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Icon className={`w-4 h-4 ${color}`} />
          <h3 className="font-semibold text-slate-100">{title}</h3>
        </div>
        <span className="text-xs text-slate-500">{subtitle}</span>
      </div>
      {items.length === 0 ? (
        <div className="text-xs text-slate-500 py-4 text-center">
          Nenhum ponto encontrado num raio razoável.
        </div>
      ) : (
        <ol className="space-y-1.5">
          {items.map((it, i) => (
            <li
              key={i}
              className="flex items-baseline justify-between text-sm py-1.5 border-b border-slate-800/60 last:border-0"
            >
              <span className="text-slate-400">
                <span className="text-xs text-slate-600 mr-2 tabular-nums">
                  #{i + 1}
                </span>
                {it.nome || (
                  <span className="text-slate-500 italic">sem nome</span>
                )}
              </span>
              <span className="text-slate-100 font-semibold tabular-nums">
                {it.distancia_km != null
                  ? `${it.distancia_km.toFixed(1)} km`
                  : "—"}
              </span>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}

function MinDistCard({
  items,
}: {
  items: Array<{
    icon: typeof Route;
    label: string;
    source: string;
    km: number | null | undefined;
    color: string;
  }>;
}) {
  return (
    <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-5">
      <h3 className="font-semibold text-slate-100 mb-4 flex items-center gap-2">
        <Route className="w-4 h-4 text-emerald-400" />
        Acesso Rodo/Ferroviário
      </h3>
      <div className="space-y-3">
        {items.map((it, i) => {
          const Icon = it.icon;
          return (
            <div
              key={i}
              className="flex items-center justify-between py-2 border-b border-slate-800/60 last:border-0"
            >
              <div className="flex items-center gap-2">
                <Icon className={`w-4 h-4 ${it.color}`} />
                <div>
                  <div className="text-sm font-medium text-slate-100">
                    {it.label}
                  </div>
                  <div className="text-xs text-slate-500">{it.source}</div>
                </div>
              </div>
              <span className="text-lg font-semibold text-slate-100 tabular-nums">
                {it.km != null ? `${it.km.toFixed(1)} km` : "> 5 km"}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
