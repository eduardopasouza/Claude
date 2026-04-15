"use client";

import { useState, useCallback } from 'react';
import { Search, MapPin, X, ChevronRight, AlertTriangle, Shield, Loader2 } from 'lucide-react';
import useSWR from 'swr';
import { swrFetcher } from '@/lib/api';

interface PropertyResult {
  car_code: string;
  municipio: string;
  uf: string;
  area_ha: number;
  status: string;
  tipo: string;
  modulos_fiscais: number;
  centroid: { lat: number; lon: number } | null;
}

interface OverlapFeature {
  type: string;
  properties: {
    layer: string;
    nome?: string;
    color: string;
    [key: string]: any;
  };
  geometry: any;
}

interface PropertyDetail {
  geojson: any;
  overlaps: {
    type: string;
    features: OverlapFeature[];
    metadata: {
      layers_found: string[];
      layers_checked: string[];
      total_features: number;
    };
  };
}

const LAYER_LABELS: Record<string, string> = {
  terra_indigena: 'Terra Indígena',
  unidade_conservacao: 'Unidade de Conservação',
  embargo_icmbio: 'Embargo ICMBio',
  prodes: 'Desmatamento PRODES',
  deter_amazonia: 'Alerta DETER Amazônia',
  deter_cerrado: 'Alerta DETER Cerrado',
  mapbiomas_alerta: 'Alerta MapBiomas',
  sigef: 'Parcela SIGEF',
};

export default function PropertySearch({
  onSelectProperty,
  onClearProperty,
  selectedCar,
}: {
  onSelectProperty: (car: string, center: [number, number]) => void;
  onClearProperty: () => void;
  selectedCar: string | null;
}) {
  const [query, setQuery] = useState('');
  const [searchUf, setSearchUf] = useState('MA');

  // Search results
  const searchEndpoint = query.length >= 3
    ? `/property/search?q=${encodeURIComponent(query)}&uf=${searchUf}&page_size=8`
    : null;
  const { data: searchData, isLoading: searching } = useSWR(searchEndpoint, swrFetcher, {
    revalidateOnFocus: false,
    dedupingInterval: 500,
  });

  // Selected property detail
  const { data: propertyGeoJson } = useSWR(
    selectedCar ? `/property/${selectedCar}/geojson` : null,
    swrFetcher,
    { revalidateOnFocus: false }
  );
  const { data: overlapsData } = useSWR(
    selectedCar ? `/property/${selectedCar}/overlaps/geojson` : null,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  const handleSelect = useCallback((r: PropertyResult) => {
    if (r.centroid) {
      onSelectProperty(r.car_code, [r.centroid.lat, r.centroid.lon]);
    }
    setQuery('');
  }, [onSelectProperty]);

  const results: PropertyResult[] = searchData?.results || [];
  const overlapFeatures: OverlapFeature[] = overlapsData?.features || [];
  const layersFound: string[] = overlapsData?.metadata?.layers_found || [];

  // Group overlaps by layer
  const groupedOverlaps: Record<string, OverlapFeature[]> = {};
  for (const f of overlapFeatures) {
    const layer = f.properties.layer;
    if (!groupedOverlaps[layer]) groupedOverlaps[layer] = [];
    groupedOverlaps[layer].push(f);
  }

  return (
    <div className="absolute top-6 right-6 z-10 w-[360px] flex flex-col gap-3 max-h-[calc(100vh-8rem)]">
      {/* Search box */}
      <div className="bg-background/85 backdrop-blur-2xl border border-border rounded-2xl p-4 shadow-[0_0_40px_-10px_rgba(0,0,0,0.9)]">
        <div className="flex items-center gap-2 mb-3">
          <Search className="h-4 w-4 text-primary shrink-0" />
          <input
            type="text"
            placeholder="Buscar CAR, município..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 bg-transparent text-white text-sm placeholder:text-muted-foreground outline-none"
          />
          <select
            value={searchUf}
            onChange={(e) => setSearchUf(e.target.value)}
            className="bg-muted border border-border text-white text-xs rounded px-1.5 py-1 outline-none"
          >
            {['MA','MT','PA','GO','TO','MS','BA','MG','SP','PR','RO','AC','AM','AP','RR','PI','CE','RN','PB','PE','AL','SE','ES','RJ','SC','RS','DF'].map(uf => (
              <option key={uf} value={uf}>{uf}</option>
            ))}
          </select>
        </div>

        {/* Search results */}
        {searching && (
          <div className="flex items-center gap-2 text-muted-foreground text-xs py-2">
            <Loader2 className="h-3 w-3 animate-spin" /> Buscando...
          </div>
        )}
        {results.length > 0 && (
          <div className="space-y-1 max-h-[240px] overflow-y-auto">
            {results.map((r) => (
              <button
                key={r.car_code}
                onClick={() => handleSelect(r)}
                className="w-full text-left px-3 py-2 rounded-lg hover:bg-primary/10 border border-transparent hover:border-primary/30 transition-all group"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-primary truncate max-w-[200px]">
                    {r.car_code.substring(0, 30)}...
                  </span>
                  <ChevronRight className="h-3 w-3 text-muted-foreground group-hover:text-primary" />
                </div>
                <div className="flex items-center gap-2 mt-0.5">
                  <span className="text-[10px] text-muted-foreground">
                    {r.municipio || r.uf} · {r.area_ha.toFixed(1)} ha
                  </span>
                  <span className={`text-[9px] px-1 rounded ${r.status === 'AT' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>
                    {r.status}
                  </span>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Property detail panel */}
      {selectedCar && (
        <div className="bg-background/85 backdrop-blur-2xl border border-border rounded-2xl p-4 shadow-[0_0_40px_-10px_rgba(0,0,0,0.9)] overflow-y-auto max-h-[50vh]">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4 text-primary" />
              <span className="text-sm font-bold text-white">Imóvel Selecionado</span>
            </div>
            <button onClick={onClearProperty} className="text-muted-foreground hover:text-white">
              <X className="h-4 w-4" />
            </button>
          </div>

          <div className="text-[10px] font-mono text-primary/80 mb-3 break-all">{selectedCar}</div>

          {propertyGeoJson?.features?.[0] && (
            <div className="grid grid-cols-2 gap-2 mb-4 text-xs">
              <div className="bg-muted/50 rounded-lg p-2">
                <div className="text-muted-foreground text-[10px]">Área</div>
                <div className="text-white font-bold">{propertyGeoJson.features[0].properties.area_ha?.toFixed(1)} ha</div>
              </div>
              <div className="bg-muted/50 rounded-lg p-2">
                <div className="text-muted-foreground text-[10px]">Status</div>
                <div className="text-white font-bold">{propertyGeoJson.features[0].properties.status}</div>
              </div>
              <div className="bg-muted/50 rounded-lg p-2">
                <div className="text-muted-foreground text-[10px]">Município</div>
                <div className="text-white font-bold">{propertyGeoJson.features[0].properties.municipio || propertyGeoJson.features[0].properties.uf}</div>
              </div>
              <div className="bg-muted/50 rounded-lg p-2">
                <div className="text-muted-foreground text-[10px]">Módulos Fiscais</div>
                <div className="text-white font-bold">{propertyGeoJson.features[0].properties.modulos_fiscais?.toFixed(2)}</div>
              </div>
            </div>
          )}

          {/* Overlaps */}
          <div className="border-t border-border/50 pt-3">
            <div className="flex items-center gap-2 mb-2">
              {overlapFeatures.length > 0 ? (
                <AlertTriangle className="h-3.5 w-3.5 text-amber-400" />
              ) : (
                <Shield className="h-3.5 w-3.5 text-emerald-400" />
              )}
              <span className="text-xs font-bold text-white">
                {overlapFeatures.length > 0
                  ? `${overlapFeatures.length} sobreposição(ões)`
                  : 'Sem sobreposições detectadas'}
              </span>
            </div>

            {Object.entries(groupedOverlaps).map(([layer, features]) => (
              <div key={layer} className="mb-2">
                <div className="flex items-center gap-2 mb-1">
                  <div className="w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: features[0]?.properties.color || '#888' }} />
                  <span className="text-[11px] text-muted-foreground font-semibold">
                    {LAYER_LABELS[layer] || layer} ({features.length})
                  </span>
                </div>
                {features.slice(0, 3).map((f, i) => (
                  <div key={i} className="ml-5 text-[10px] text-muted-foreground">
                    {f.properties.nome || f.properties.bioma || f.properties.classe || f.properties.ano || '—'}
                  </div>
                ))}
                {features.length > 3 && (
                  <div className="ml-5 text-[10px] text-primary/60">+{features.length - 3} mais</div>
                )}
              </div>
            ))}

            {overlapsData?.metadata && (
              <div className="text-[9px] text-muted-foreground mt-2">
                {overlapsData.metadata.layers_checked.length} camadas verificadas
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
