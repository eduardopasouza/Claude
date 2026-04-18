"use client";

/**
 * Sincroniza o Zustand MapStore com a URL (querystring).
 *
 * No mount:
 *   lê searchParams → hydrate no store
 *
 * Depois:
 *   subscribe em mudanças do store → router.replace com nova query
 *
 * Uso:
 *   function MapPage() {
 *     useMapUrlSync();
 *     return <MapComponent />;
 *   }
 */

import { useEffect, useRef } from "react";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import {
  useMapStore,
  queryStringToPartial,
  stateToQueryString,
} from "./map-store";

export function useMapUrlSync() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const hydratedRef = useRef(false);

  // Hidrata uma vez na montagem
  useEffect(() => {
    if (hydratedRef.current) return;
    const partial = queryStringToPartial(new URLSearchParams(searchParams.toString()));
    if (Object.keys(partial).length) {
      useMapStore.getState().hydrate(partial);
    }
    hydratedRef.current = true;
  }, [searchParams]);

  // Sincroniza mudanças do store para URL
  useEffect(() => {
    if (!hydratedRef.current) return;
    const unsub = useMapStore.subscribe((state) => {
      const qs = stateToQueryString(state);
      const currentQs = searchParams.toString();
      if (qs !== currentQs) {
        const url = qs ? `${pathname}?${qs}` : pathname;
        router.replace(url, { scroll: false });
      }
    });
    return () => unsub();
  }, [pathname, router, searchParams]);
}
