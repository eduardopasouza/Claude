/**
 * Smoke tests do TesesTab.
 */

import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { SWRConfig } from "swr";
import { TesesTab } from "./TesesTab";

const FAKE_TESES = {
  total: 2,
  teses: [
    {
      id: 1,
      slug: "nulidade-auto-ibama-falta-cient",
      titulo: "Nulidade do Auto de Infração IBAMA",
      area: "ambiental",
      situacao: "Auto com lavratura presencial viciada",
      sumula_propria: "O Auto de Infração Ambiental é ato administrativo vinculado.",
      publico_alvo: ["produtor_autuado", "advogado"],
      n_argumentos: 3,
      n_precedentes: 2,
    },
    {
      id: 2,
      slug: "usucapiao-rural",
      titulo: "Usucapião Rural",
      area: "fundiario",
      situacao: "Posse mansa e pacífica por 5+ anos",
      sumula_propria: "",
      publico_alvo: ["produtor"],
      n_argumentos: 4,
      n_precedentes: 1,
    },
  ],
};

function withSwr(ui: React.ReactElement) {
  return (
    <SWRConfig value={{ provider: () => new Map(), dedupingInterval: 0 }}>
      {ui}
    </SWRConfig>
  );
}

describe("TesesTab", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve(
          new Response(JSON.stringify(FAKE_TESES), {
            status: 200,
            headers: { "Content-Type": "application/json" },
          }),
        ),
      ),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renderiza os botões de filtro por área (7 áreas)", () => {
    render(withSwr(<TesesTab />));
    // Cada área vira um botão — aceita "todas" + 6 específicas
    expect(screen.getByRole("button", { name: /todas as áreas/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /ambiental/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /fundiário/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /trabalhista rural/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /tributário/i })).toBeInTheDocument();
  });

  it("mostra contador de teses após fetch", async () => {
    render(withSwr(<TesesTab />));
    await waitFor(() => {
      expect(screen.getByText(/2 tese\(s\)/i)).toBeInTheDocument();
    });
  });

  it("após fetch, agrupa por área", async () => {
    render(withSwr(<TesesTab />));
    await waitFor(() => {
      // Título aparece como heading de grupo + como botão de filtro
      const ambientalElements = screen.getAllByText(/ambiental/i);
      expect(ambientalElements.length).toBeGreaterThanOrEqual(2);
    });
  });

  it("mostra accordion com títulos das teses", async () => {
    render(withSwr(<TesesTab />));
    await waitFor(() => {
      expect(
        screen.getByText(/nulidade do auto de infração ibama/i),
      ).toBeInTheDocument();
    });
    expect(screen.getByText(/usucapião rural/i)).toBeInTheDocument();
  });
});
