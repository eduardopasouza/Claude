/**
 * Testes de render do ContratosTab.
 *
 * Mocka GET /juridico/contratos com resposta fake para validar:
 *   - grid renderiza com seeds
 *   - filtros presentes
 *   - placeholder de busca correto
 */

import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { SWRConfig } from "swr";
import { ContratosTab } from "./ContratosTab";

const FAKE_CONTRATOS = {
  total: 2,
  contratos: [
    {
      id: 1,
      slug: "arrendamento-rural",
      titulo: "Arrendamento Rural (Estatuto da Terra)",
      categoria: "exploracao_rural",
      subcategoria: "arrendamento",
      sinopse: "Cessão onerosa de uso e gozo de imóvel rural por prazo determinado.",
      aplicacao: "Ambos",
      publico_alvo: ["produtor", "trading"],
      n_campos: 14,
      n_legislacao: 4,
      versao: "1.0",
    },
    {
      id: 2,
      slug: "comodato-rural",
      titulo: "Comodato Rural",
      categoria: "exploracao_rural",
      subcategoria: "comodato",
      sinopse: "Empréstimo gratuito de imóvel rural.",
      aplicacao: "Ambos",
      publico_alvo: ["produtor"],
      n_campos: 4,
      n_legislacao: 2,
      versao: "1.0",
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

describe("ContratosTab", () => {
  beforeEach(() => {
    // Mock global fetch — primeira chamada é GET /juridico/contratos
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve(
          new Response(JSON.stringify(FAKE_CONTRATOS), {
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

  it("renderiza sem crashar com loading inicial", () => {
    render(withSwr(<ContratosTab />));
    // Loading é exibido antes de qualquer dado
    expect(
      screen.getByText(/carregando contratos/i),
    ).toBeInTheDocument();
  });

  it("mostra os selects de categoria e público via labels", () => {
    render(withSwr(<ContratosTab />));
    // Labels são spans específicos com classe uppercase tracking
    expect(screen.getAllByText(/categoria/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/público/i).length).toBeGreaterThan(0);
  });

  it("mostra input de busca com placeholder", () => {
    render(withSwr(<ContratosTab />));
    expect(screen.getByPlaceholderText(/título, sinopse/i)).toBeInTheDocument();
  });

  it("após fetch, renderiza cards dos contratos", async () => {
    render(withSwr(<ContratosTab />));
    await waitFor(() => {
      expect(
        screen.getByText(/arrendamento rural \(estatuto da terra\)/i),
      ).toBeInTheDocument();
    });
    expect(screen.getByText(/comodato rural/i)).toBeInTheDocument();
  });

  it("contador 'N contrato(s)' reflete o total", async () => {
    render(withSwr(<ContratosTab />));
    await waitFor(() => {
      expect(screen.getByText(/2 contrato\(s\)/i)).toBeInTheDocument();
    });
  });
});
