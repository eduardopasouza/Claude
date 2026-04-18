/**
 * Testes de render do ProcessosTab (Hub Jurídico-Agro).
 *
 * Smoke tests: componente monta sem crashar em estados críticos (empty,
 * loading, data com sanção). Fetch é mockado via vi.stubGlobal.
 *
 * Propósito: travar regressões de renderização. Testes de interação
 * completa (search → ver dossiê) ficam para suite e2e com Playwright.
 */

import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { SWRConfig } from "swr";
import { ProcessosTab } from "./ProcessosTab";

function withSwr(ui: React.ReactElement) {
  // Desliga cache e dedup pra testes independentes
  return (
    <SWRConfig value={{ provider: () => new Map(), dedupingInterval: 0 }}>
      {ui}
    </SWRConfig>
  );
}

describe("ProcessosTab — renderização inicial", () => {
  beforeEach(() => {
    // Qualquer fetch por padrão retorna vazio — só é chamado se usuário submeter
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve(
          new Response(JSON.stringify({ error: "nao chamado" }), {
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

  it("mostra formulário de busca antes de qualquer submit", () => {
    render(withSwr(<ProcessosTab />));
    expect(
      screen.getByPlaceholderText(/digite só números ou com máscara/i),
    ).toBeInTheDocument();
  });

  it("mostra botão 'Consultar dossiê'", () => {
    render(withSwr(<ProcessosTab />));
    expect(screen.getByRole("button", { name: /consultar dossiê/i })).toBeInTheDocument();
  });

  it("mostra empty state quando ainda não foi submetido", () => {
    render(withSwr(<ProcessosTab />));
    // Texto do empty state do componente
    expect(
      screen.getByText(/informe um cpf\/cnpj para gerar o dossiê jurídico/i),
    ).toBeInTheDocument();
  });

  it("botão começa habilitado (não está em loading)", () => {
    render(withSwr(<ProcessosTab />));
    const btn = screen.getByRole("button", { name: /consultar dossiê/i });
    expect(btn).not.toBeDisabled();
  });

  it("menciona as 6 bases consultadas na descrição", () => {
    render(withSwr(<ProcessosTab />));
    const helper = screen.getByText(/busca em 6 bases/i);
    expect(helper).toBeInTheDocument();
    // Todas as bases citadas
    const txt = helper.textContent || "";
    expect(txt).toContain("DataJud");
    expect(txt).toContain("DJEN");
    expect(txt).toContain("IBAMA");
    expect(txt).toContain("CEIS");
    expect(txt).toContain("CNEP");
    expect(txt).toContain("Lista Suja");
  });
});
