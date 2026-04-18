/**
 * Testes unit de src/lib/basemaps.ts — catálogo de tiles do mapa.
 *
 * Basemap é configuração estática, mas é importante que a lista não quebre
 * contratos que MapComponent e BasemapSwitcher esperam.
 */

import { describe, expect, it } from "vitest";
import { BASEMAPS, type Basemap, type BasemapId } from "./basemaps";

describe("BASEMAPS — catálogo", () => {
  it("tem pelo menos 4 opções", () => {
    expect(BASEMAPS.length).toBeGreaterThanOrEqual(4);
  });

  it("inclui os 4 ids core: dark, light, satellite, topo", () => {
    const ids: BasemapId[] = BASEMAPS.map((b) => b.id);
    expect(ids).toEqual(expect.arrayContaining(["dark", "light", "satellite", "topo"]));
  });

  it("ids são únicos", () => {
    const ids = BASEMAPS.map((b) => b.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("cada basemap tem todos os campos obrigatórios", () => {
    BASEMAPS.forEach((b: Basemap) => {
      expect(b.id).toBeTruthy();
      expect(b.label).toBeTruthy();
      expect(b.description).toBeTruthy();
      expect(b.url).toMatch(/^https?:\/\//);
      expect(b.attribution).toBeTruthy();
      expect(b.theme).toMatch(/^(dark|light)$/);
      expect(b.maxZoom).toBeGreaterThanOrEqual(10);
    });
  });

  it("urls contêm tokens Leaflet {z}/{x}/{y}", () => {
    BASEMAPS.forEach((b) => {
      expect(b.url).toContain("{z}");
      expect(b.url).toContain("{x}");
      expect(b.url).toContain("{y}");
    });
  });

  it("attribution contém link com href (boas práticas)", () => {
    BASEMAPS.forEach((b) => {
      // Aceita HTML básico ou texto puro; se for HTML, deve ter href
      if (b.attribution.includes("<a")) {
        expect(b.attribution).toContain("href=");
      }
    });
  });

  it("basemap 'dark' tem theme dark (coerência visual)", () => {
    const dark = BASEMAPS.find((b) => b.id === "dark");
    expect(dark?.theme).toBe("dark");
  });

  it("basemap 'light' tem theme light", () => {
    const light = BASEMAPS.find((b) => b.id === "light");
    expect(light?.theme).toBe("light");
  });
});
