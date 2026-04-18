/**
 * Testes unit do Zustand map-store.
 *
 * Foco:
 *   - Actions (toggleLayer, setOpacity com clamp, drill reset em cascata)
 *   - stateToQueryString (serializa apenas o que diverge do default)
 *   - queryStringToPartial (parse robusto — inputs mal-formados são ignorados)
 *   - Round-trip: state → qs → state preserva campos relevantes
 */

import { describe, expect, it, beforeEach } from "vitest";
import {
  useMapStore,
  stateToQueryString,
  queryStringToPartial,
  type MapState,
} from "./map-store";

function freshState(): MapState {
  return useMapStore.getState();
}

describe("useMapStore — actions", () => {
  beforeEach(() => {
    useMapStore.getState().reset();
  });

  it("reset volta pra valores iniciais", () => {
    useMapStore.getState().setActiveLayers(["a", "b"]);
    useMapStore.getState().setBasemap("satellite");
    useMapStore.getState().reset();
    const s = freshState();
    expect(s.activeLayers).toEqual([]);
    expect(s.basemap).toBe("dark");
  });

  it("setActiveLayers substitui a lista inteira", () => {
    useMapStore.getState().setActiveLayers(["a", "b", "c"]);
    expect(freshState().activeLayers).toEqual(["a", "b", "c"]);
  });

  it("toggleLayer adiciona quando ausente", () => {
    useMapStore.getState().toggleLayer("ceis");
    expect(freshState().activeLayers).toContain("ceis");
  });

  it("toggleLayer remove quando presente", () => {
    useMapStore.getState().toggleLayer("ceis");
    useMapStore.getState().toggleLayer("ceis");
    expect(freshState().activeLayers).not.toContain("ceis");
  });

  it("setOpacity clampa em [0, 1]", () => {
    useMapStore.getState().setOpacity("deter", 2.5);
    expect(freshState().opacityByLayer["deter"]).toBe(1);

    useMapStore.getState().setOpacity("deter", -0.3);
    expect(freshState().opacityByLayer["deter"]).toBe(0);

    useMapStore.getState().setOpacity("deter", 0.5);
    expect(freshState().opacityByLayer["deter"]).toBe(0.5);
  });

  it("setDrillUF com null limpa também o município", () => {
    useMapStore.getState().setDrillUF("MA");
    useMapStore.getState().setDrillMunicipio("2111300");
    expect(freshState().drill).toEqual({ uf: "MA", municipio: "2111300" });

    useMapStore.getState().setDrillUF(null);
    expect(freshState().drill).toEqual({ uf: null, municipio: null });
  });

  it("setDrillUF muda UF mas mantém município", () => {
    useMapStore.getState().setDrillUF("MA");
    useMapStore.getState().setDrillMunicipio("2111300");
    useMapStore.getState().setDrillUF("SP");
    expect(freshState().drill).toEqual({ uf: "SP", municipio: "2111300" });
  });

  it("hydrate faz merge parcial sem zerar outros campos", () => {
    useMapStore.getState().setActiveLayers(["a"]);
    useMapStore.getState().hydrate({ basemap: "satellite" });
    const s = freshState();
    expect(s.basemap).toBe("satellite");
    expect(s.activeLayers).toEqual(["a"]);  // preservado
  });
});

describe("stateToQueryString — serializa só o que diverge do default", () => {
  beforeEach(() => {
    useMapStore.getState().reset();
  });

  it("estado default retorna query string vazia", () => {
    expect(stateToQueryString(freshState())).toBe("");
  });

  it("activeLayers vira CSV", () => {
    useMapStore.getState().setActiveLayers(["deter", "prodes"]);
    const qs = stateToQueryString(freshState());
    expect(new URLSearchParams(qs).get("layers")).toBe("deter,prodes");
  });

  it("opacidade 1.0 não aparece (é default)", () => {
    useMapStore.getState().setOpacity("x", 1.0);
    const qs = stateToQueryString(freshState());
    expect(new URLSearchParams(qs).get("opacity")).toBeNull();
  });

  it("opacidade diferente de 1 vira JSON", () => {
    useMapStore.getState().setOpacity("deter", 0.5);
    const qs = stateToQueryString(freshState());
    const op = new URLSearchParams(qs).get("opacity");
    expect(op).toBeTruthy();
    expect(JSON.parse(op!)).toEqual({ deter: 0.5 });
  });

  it("basemap 'dark' (default) não aparece; outro basemap aparece", () => {
    useMapStore.getState().setBasemap("dark");
    expect(new URLSearchParams(stateToQueryString(freshState())).get("basemap")).toBeNull();

    useMapStore.getState().setBasemap("satellite");
    expect(
      new URLSearchParams(stateToQueryString(freshState())).get("basemap"),
    ).toBe("satellite");
  });

  it("drill UF e município são incluídos", () => {
    useMapStore.getState().setDrillUF("MA");
    useMapStore.getState().setDrillMunicipio("2111300");
    const qs = new URLSearchParams(stateToQueryString(freshState()));
    expect(qs.get("uf")).toBe("MA");
    expect(qs.get("mun")).toBe("2111300");
  });

  it("temporal start e end como t0/t1", () => {
    useMapStore.getState().setTemporal({ start: "2024-01", end: "2024-12" });
    const qs = new URLSearchParams(stateToQueryString(freshState()));
    expect(qs.get("t0")).toBe("2024-01");
    expect(qs.get("t1")).toBe("2024-12");
  });

  it("center default NÃO aparece; center customizado aparece", () => {
    // Default: lat=-12.4411, lng=-55.221, zoom=5
    expect(new URLSearchParams(stateToQueryString(freshState())).get("c")).toBeNull();

    useMapStore.getState().setCenter(-23.5, -46.6, 10);
    expect(
      new URLSearchParams(stateToQueryString(freshState())).get("c"),
    ).toBe("-23.5000,-46.6000,10");
  });
});

describe("queryStringToPartial — parse robusto", () => {
  it("query vazia retorna objeto vazio", () => {
    expect(queryStringToPartial(new URLSearchParams())).toEqual({});
  });

  it("layers CSV é parseado em array", () => {
    const p = queryStringToPartial(new URLSearchParams("layers=a,b,c"));
    expect(p.activeLayers).toEqual(["a", "b", "c"]);
  });

  it("layers com strings vazias (a,,b) filtra vazias", () => {
    const p = queryStringToPartial(new URLSearchParams("layers=a,,b"));
    expect(p.activeLayers).toEqual(["a", "b"]);
  });

  it("opacity JSON válido é parseado", () => {
    const p = queryStringToPartial(
      new URLSearchParams(`opacity=${encodeURIComponent('{"deter":0.5}')}`),
    );
    expect(p.opacityByLayer).toEqual({ deter: 0.5 });
  });

  it("opacity JSON inválido é ignorado silenciosamente", () => {
    const p = queryStringToPartial(new URLSearchParams("opacity=not-json"));
    expect(p.opacityByLayer).toBeUndefined();
  });

  it("temporal com só t0 produz range parcial", () => {
    const p = queryStringToPartial(new URLSearchParams("t0=2024-01"));
    expect(p.temporal).toEqual({ start: "2024-01", end: null });
  });

  it("center válido é parseado", () => {
    const p = queryStringToPartial(new URLSearchParams("c=-12.5,-55.0,7"));
    expect(p.center).toEqual({ lat: -12.5, lng: -55.0, zoom: 7 });
  });

  it("center com valor inválido é ignorado", () => {
    const p = queryStringToPartial(new URLSearchParams("c=xyz,abc,def"));
    expect(p.center).toBeUndefined();
  });

  it("center com número de partes errado é ignorado", () => {
    const p = queryStringToPartial(new URLSearchParams("c=-12.5,-55.0"));
    expect(p.center).toBeUndefined();
  });

  it("drill UF e município", () => {
    const p = queryStringToPartial(new URLSearchParams("uf=MA&mun=2111300"));
    expect(p.drill).toEqual({ uf: "MA", municipio: "2111300" });
  });
});

describe("Round-trip state ↔ URL", () => {
  beforeEach(() => {
    useMapStore.getState().reset();
  });

  it("configuração complexa preserva campos após round-trip", () => {
    useMapStore.getState().setActiveLayers(["deter", "prodes"]);
    useMapStore.getState().setOpacity("deter", 0.3);
    useMapStore.getState().setBasemap("satellite");
    useMapStore.getState().setTemporal({ start: "2024-06", end: "2024-12" });
    useMapStore.getState().setDrillUF("MT");
    useMapStore.getState().setPriceLayer("preco_soja");
    useMapStore.getState().setCenter(-15.0, -55.0, 8);

    const qs = stateToQueryString(freshState());
    const parsed = queryStringToPartial(new URLSearchParams(qs));

    expect(parsed.activeLayers).toEqual(["deter", "prodes"]);
    expect(parsed.opacityByLayer).toEqual({ deter: 0.3 });
    expect(parsed.basemap).toBe("satellite");
    expect(parsed.temporal).toEqual({ start: "2024-06", end: "2024-12" });
    expect(parsed.drill).toEqual({ uf: "MT", municipio: null });
    expect(parsed.priceLayerId).toBe("preco_soja");
    expect(parsed.center).toEqual({ lat: -15.0, lng: -55.0, zoom: 8 });
  });
});
