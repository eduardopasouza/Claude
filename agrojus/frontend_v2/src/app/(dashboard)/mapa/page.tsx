"use client";

import dynamic from 'next/dynamic';

const MapComponent = dynamic(() => import('@/components/mapa/MapComponent'), {
  ssr: false,
});

export default function MapPage() {
  return (
    <div className="h-full w-full relative">
       <MapComponent />
    </div>
  );
}
