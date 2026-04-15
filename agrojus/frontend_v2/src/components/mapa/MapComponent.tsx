"use client";

import { useEffect, useState, useCallback } from 'react';
import { MapContainer, TileLayer, ZoomControl, useMapEvents, useMap, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { Layers, Crosshair, Download, RefreshCcw, Lock, Loader2 } from 'lucide-react';
import L from 'leaflet';

import useSWR from "swr";
import { swrFetcher } from "@/lib/api";
import PropertySearch from './PropertySearch';

/** 
 * Limites e Travas de Zoom (conforme contrato de API do Backend)
 * Usado para evitar travamento do navegador no fetch de GeoJSON não clipado.
 */
const LAYERS_CONFIG = [
  { id: 'desmatamento', name: 'DETER Alertas (Amazônia)', minZoom: 6, maxFeatures: 2000, color: '#F59E0B' },
  { id: 'desmatamento_cerrado', name: 'DETER Alertas (Cerrado)', minZoom: 6, maxFeatures: 2000, color: '#F97316' },
  { id: 'prodes', name: 'PRODES Acumulado', minZoom: 4, maxFeatures: 9999, color: '#7E22CE' },
  { id: 'embargos', name: 'Embargos IBAMA', minZoom: 6, maxFeatures: 5000, color: '#EF4444' },
  { id: 'embargos_mte', name: 'Lista Suja MTE', minZoom: 6, maxFeatures: 2000, color: '#F43F5E' },
  { id: 'geo_car', name: 'Imóveis Rurais', minZoom: 10, maxFeatures: 1000, color: '#10B981' },
  { id: 'parcelas_financiamento', name: 'Crédito Rural (SICOR)', minZoom: 12, maxFeatures: 500, color: '#3B82F6' },
  { id: 'terras_indigenas', name: 'Terras Indígenas', minZoom: 4, maxFeatures: null, color: '#3B82F6' },
  { id: 'municipios', name: 'Limites Municipais', minZoom: 4, maxFeatures: null, color: '#ffffff' },
];

function MapEvents({ onMove }: { onMove: (bounds: string, zoom: number, center: L.LatLng) => void }) {
  const map = useMapEvents({
    moveend: () => {
      onMove(map.getBounds().toBBoxString(), map.getZoom(), map.getCenter());
    },
  });
  // Fire on initial mount so bounds are set immediately
  useEffect(() => {
    onMove(map.getBounds().toBBoxString(), map.getZoom(), map.getCenter());
  }, []);
  return null;
}

function FlyToProperty({ carCode, center }: { carCode: string | null; center: [number, number] | null }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.flyTo(center, 14, { duration: 1.5 });
    }
  }, [carCode, center, map]);
  return null;
}

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
      {geojson?.type === 'FeatureCollection' && (
        <GeoJSON
          key={`prop-${carCode}`}
          data={geojson}
          style={{ color: '#10B981', weight: 3, fillColor: '#10B981', fillOpacity: 0.25, dashArray: '5,5' }}
        />
      )}
      {overlaps?.type === 'FeatureCollection' && overlaps.features.length > 0 && (
        <GeoJSON
          key={`overlaps-${carCode}`}
          data={overlaps}
          style={(feature: any) => ({
            color: feature?.properties?.color || '#FF0000',
            weight: 2,
            fillColor: feature?.properties?.color || '#FF0000',
            fillOpacity: 0.3,
          })}
        />
      )}
    </>
  );
}

function ActiveMapLayer({ layer, bounds }: { layer: typeof LAYERS_CONFIG[0], bounds: string }) {
  const endpoint = `/geo/layers/${layer.id}/geojson?bbox=${bounds}&max_features=${layer.maxFeatures || 1000}`;
  const { data } = useSWR(bounds ? endpoint : null, swrFetcher, {
     revalidateOnFocus: false, // Não revalidar em foco do mapa p/ não piscar tela 
     dedupingInterval: 60000 
  });

  if (!data || data.type !== 'FeatureCollection') return null;
  
  return (
     <GeoJSON 
       key={`${layer.id}-${bounds}`} 
       data={data} 
       style={{ color: layer.color, weight: 1.5, fillColor: layer.color, fillOpacity: 0.15 }}
     />
  );
}

export default function MapComponent() {
  const [mounted, setMounted] = useState(false);
  const [zoom, setZoom] = useState(5);
  const [center, setCenter] = useState<L.LatLng>(new L.LatLng(-12.4411, -55.2210));
  const [bounds, setBounds] = useState("");
  const [activeLayers, setActiveLayers] = useState<string[]>([]);
  const [selectedCar, setSelectedCar] = useState<string | null>(null);
  const [flyTarget, setFlyTarget] = useState<[number, number] | null>(null);

  const handleSelectProperty = useCallback((car: string, center: [number, number]) => {
    setSelectedCar(car);
    setFlyTarget(center);
  }, []);

  const handleClearProperty = useCallback(() => {
    setSelectedCar(null);
    setFlyTarget(null);
  }, []);

  useEffect(() => {
    setMounted(true);
    delete (L.Icon.Default.prototype as any)._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
      iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
      shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    });
  }, []);

  const toggleLayer = (layer: any) => {
    if (zoom < layer.minZoom) return; // Trava de performance
    setActiveLayers(prev => prev.includes(layer.id) ? prev.filter(l => l !== layer.id) : [...prev, layer.id]);
  };
  
  // Efeito para desligar camadas (fallback) caso o usuário dê zoom out drástico
  useEffect(() => {
     setActiveLayers(prev => prev.filter(id => {
       const l = LAYERS_CONFIG.find(c => c.id === id);
       return l && zoom >= l.minZoom;
     }));
  }, [zoom]);

  if (!mounted) {
    return (
      <div className="h-[calc(100vh-4rem)] w-full flex items-center justify-center p-8 bg-black">
        <div className="flex items-center gap-3 text-primary font-mono animate-pulse">
           <Loader2 className="h-5 w-5 animate-spin" />
           Iniciando Engine CARTO Dark Matter e Trava GeoJSON...
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-[calc(100vh-4rem)] bg-black">
      <MapContainer 
        center={[-12.4411, -55.2210]} 
        zoom={zoom} 
        zoomControl={false}
        className="w-full h-full z-0"
      >
        <MapEvents onMove={(b, z, c) => { setBounds(b); setZoom(z); setCenter(c); }} />
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />
        
        {/* Render Layers Dinamicamente */}
        {activeLayers.map(layerId => {
           const layerConfig = LAYERS_CONFIG.find(l => l.id === layerId);
           if (!layerConfig || zoom < layerConfig.minZoom) return null;
           return <ActiveMapLayer key={`active-${layerId}`} layer={layerConfig} bounds={bounds} />;
        })}

        {/* Selected property boundary + overlaps */}
        <SelectedPropertyLayer carCode={selectedCar} />
        <FlyToProperty carCode={selectedCar} center={flyTarget} />

        <ZoomControl position="bottomleft" />
      </MapContainer>

      {/* Glassmorphism HUD Overlay */}
      <div className="absolute top-6 left-6 z-10 w-[340px] animate-in slide-in-from-left fade-in duration-500">
         <div className="bg-background/85 backdrop-blur-2xl border border-border rounded-2xl p-6 shadow-[0_0_40px_-10px_rgba(0,0,0,0.9)]">
            <div className="flex items-center justify-between mb-5">
               <h3 className="font-heading font-bold text-lg text-white flex items-center gap-2">
                  <Layers className="h-5 w-5 text-primary" />
                  Painel de Camadas
               </h3>
               <span className="text-[10px] font-mono border border-border px-1.5 py-0.5 rounded text-muted-foreground bg-black/40">Z: {zoom}</span>
            </div>
            
            <div className="space-y-4 max-h-[45vh] overflow-y-auto pr-2 custom-scrollbar">
               {LAYERS_CONFIG.map((layer) => {
                 const isLocked = zoom < layer.minZoom;
                 const isActive = activeLayers.includes(layer.id) && !isLocked;
                 
                 return (
                 <div key={layer.id} className="flex justify-between items-center group">
                   <label className={`flex flex-1 items-center gap-3 transition-colors ${isLocked ? 'cursor-not-allowed opacity-40' : 'cursor-pointer'}`} onClick={() => toggleLayer(layer)}>
                     <div className={`relative flex items-center justify-center w-5 h-5 border rounded transition-colors ${isActive ? 'border-primary bg-primary/20' : 'bg-muted/50 border-border group-hover:border-primary/50'}`}>
                        {isActive && <div className="w-3 h-3 rounded-sm shadow-[0_0_10px_0_rgba(255,255,255,0.5)]" style={{ backgroundColor: layer.color }} />}
                     </div>
                     <span className={`text-sm transition-colors ${isActive ? 'text-white font-semibold' : 'text-muted-foreground group-hover:text-white/80'}`}>
                        {layer.name}
                     </span>
                   </label>
                   {isLocked && (
                     <div className="flex items-center gap-1.5 text-[10px] uppercase font-bold text-rose-500/80 bg-rose-500/10 px-1.5 py-0.5 rounded border border-rose-500/20" title={`Zoom Mínimo Exigido: ${layer.minZoom}`}>
                       <Lock className="h-3 w-3" /> Z{layer.minZoom}+
                     </div>
                   )}
                 </div>
               )})}
            </div>

            <div className="mt-8 pt-5 border-t border-border/50 flex gap-3">
               <button className="flex-1 bg-muted hover:bg-muted/80 text-white text-xs font-bold py-2.5 rounded-lg transition-colors border border-border flex items-center justify-center gap-1.5 focus:ring-2 focus:ring-border">
                  <RefreshCcw className="h-3.5 w-3.5" /> Forçar Recarga
               </button>
            </div>
         </div>
      </div>

      {/* Property search + detail panel */}
      <PropertySearch
        onSelectProperty={handleSelectProperty}
        onClearProperty={handleClearProperty}
        selectedCar={selectedCar}
      />

      {/* Lat/Lon Overlay */}
      <div className="absolute bottom-6 right-6 z-10 animate-in slide-in-from-bottom fade-in duration-700 delay-300">
         <div className="bg-background/80 backdrop-blur-md border border-border rounded-xl px-4 py-2.5 flex items-center gap-4 text-[11px] font-mono text-muted-foreground shadow-lg tracking-wider font-semibold pointer-events-none">
            <div className="flex items-center gap-1.5 text-primary">
               <Crosshair className="h-4 w-4" />
               LAT: {center.lat.toFixed(4)}
            </div>
            <div>LON: {center.lng.toFixed(4)}</div>
         </div>
      </div>

    </div>
  );
}
